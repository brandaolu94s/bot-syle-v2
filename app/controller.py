from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
import psutil
import os
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database import get_db
from models import GuiaLogs

app = FastAPI()  # ✅ Create FastAPI app here

app.mount("/frontend", StaticFiles(directory=r"C:\Users\Lenovo\Documents\GitHub\bot-syle-v2\app\frontend"), name="frontend")

process = psutil.Process(os.getpid())  # ✅ Cache the process info

def get_memory_usage():
    """Returns the current process memory usage in MB."""
    mem_info = process.memory_info()
    return round(mem_info.rss / (1024 * 1024), 2)  # Convert bytes to MB

@app.get("/system/memory")
async def memory_usage():
    """Endpoint to check memory usage in MB."""
    return {"memory_usage_mb": get_memory_usage()}

@app.get("/system/stats")
async def system_stats():
    """Returns CPU and Memory usage."""
    return {
        "memory_usage_mb": get_memory_usage(),
        "cpu_usage_percent": psutil.cpu_percent()
    }

# ✅ Fix: Middleware must manually handle database sessions
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)

    async for db in get_db():  # ✅ Open a session manually
        try:
            log_entry = GuiaLogs(
                execution_id=str(datetime.now().timestamp()),  # Dummy exec ID
                id_GuiaExame="API",  # Identifier for API logs
                file_name="HTTP Request",
                function_name=f"{request.method} {request.url.path}",
                execution_time=datetime.now(),
                status=str(response.status_code),
                message="API Request Logged",
                return_data=f"Request: {request.url.path}"
            )
            db.add(log_entry)
            await db.commit()
        except Exception as e:
            logging.error(f"Error logging HTTP request: {e}")
        finally:
            await db.close()  # ✅ Ensure the session is closed

    return response

# ✅ Fetch API Logs from `GuiaLogs`
@app.get("/logs/api")
async def get_api_logs(db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(text(
            "SELECT TOP 10 execution_time, function_name, status FROM GuiaLogs ORDER BY execution_time DESC "
            )
        )
        logs = [{"time": row[0], "method": row[1], "status": row[2]} for row in result.fetchall()]
        return {"logs": logs}

# ✅ Fetch Bot Logs from `GuiaLogs`
@app.get("/logs/bot")
async def get_bot_logs(db: AsyncSession = Depends(get_db)):
    async with db as session:
        result = await session.execute(text(
            "SELECT TOP 10 execution_time, function_name, message FROM GuiaLogs ORDER BY execution_time DESC"
            )
        )
        logs = [{"time": row[0], "action": row[1], "message": row[2]} for row in result.fetchall()]
        return {"logs": logs}
