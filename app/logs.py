from config import Config
from models import GuiaLogs
from database import get_db  # Import new session manager
import os
import datetime
import functools
import json
import pytz
from sqlalchemy.ext.asyncio import AsyncSession

e = Config()
log_table = e.LOG_TABLE

def log_execution():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(exec_id=None, id_GuiaExame=None, db: AsyncSession = None, *args, **kwargs):
            if db is None:
                async for session in get_db():  # ✅ Get DB session if not provided
                    db = session
                    break

            result = await func(exec_id, id_GuiaExame, db, *args, **kwargs)

            log_entry = GuiaLogs(
                execution_id=exec_id,
                id_GuiaExame=id_GuiaExame,
                file_name=os.path.basename(__file__),
                function_name=func.__name__,
                execution_time=datetime.datetime.now(pytz.timezone('America/Sao_Paulo')),
                status=result.get("status", ""),
                message=result.get("message", ""),
                return_data=str(result) if result else None
            )

            await _log_to_db(log_entry)  # ✅ Uses a separate DB session
            return result
        return wrapper
    return decorator

async def _log_to_db(log_entry):
    """Executes the log insertion using a separate session to avoid transaction conflicts."""
    async for db in get_db():  # ✅ Get a fresh session for logging
        try:
            db.add(log_entry)  # ✅ Use the new session
            await db.commit()  # ✅ Commit separately from the main transaction
        except Exception as e:
            print(f"⚠️ Logging failed: {e}")  # Handle errors properly
        finally:
            await db.close()  # ✅ Ensure the session is closed properly
        break  # ✅ Exit after using a single session
