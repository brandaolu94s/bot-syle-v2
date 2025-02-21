import asyncio
import uuid
import os
import psutil
import uvicorn
from config import Config
from database import get_pending_records, get_db
from logs import log_execution
from sqlalchemy.ext.asyncio import AsyncSession
from controller import app  # ✅ Import FastAPI app
import gc


e = Config()
semaphore = asyncio.Semaphore(2)  # Limit concurrency to 2 WebDrivers

@log_execution()
async def process_record(exec_id, guia_id, db: AsyncSession):
    """Handles processing for each record with controlled concurrency."""
    async with semaphore:  # ✅ Ensure only 2 WebDrivers run at a time
        print(f"Processing Guia ID: {guia_id} with Execution ID: {exec_id}")

        result = ["ok"]

        try:
            return {"status": "success", "message": "Operation completed", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e), "data": None}

async def main_processing():
    """Continuously fetch and process records with controlled concurrency."""
    print("Starting record processing loop...")

    async for db in get_db():
        try:
            while True:
                print("Fetching new records...")
                response = await get_pending_records(db)

                if not response.get("data"):
                    print("No valid records found. Retrying in 5 seconds...")
                    await asyncio.sleep(5)  # ✅ Add a small delay
                    continue

                execution_id = str(uuid.uuid4())
                print(f"Processing batch {execution_id} with {len(response['data'])} records.")

                tasks = [process_record(execution_id, record.get("idsydle", "unknown"), db) for record in response["data"]]
                await asyncio.gather(*tasks)

                await asyncio.sleep(300)  # ✅ Prevent instant looping

                gc.collect()  # ✅ Force garbage collection
        finally:
            await db.close()  # ✅ Ensure the DB connection is properly closed


async def run_fastapi():
    """Runs FastAPI server in the background."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info", workers=1)
    server = uvicorn.Server(config)
    await server.serve()

async def run_main():
    """Runs both FastAPI and the main processing loop concurrently."""
    await asyncio.gather(
        run_fastapi(),  # ✅ Run FastAPI API in the background
        main_processing()  # ✅ Run main processing function
    )

async def run_forever():
    """Ensures FastAPI and processing loop keep running indefinitely, restarting on failure."""
    while True:
        try:
            await run_main()
        except Exception as e:
            print(f"⚠️ Critical error: {e}")
            print("🔄 Restarting script in 30 seconds...")
            await asyncio.sleep(30)  # ✅ Prevent rapid crashes & CPU overload

if __name__ == "__main__":
    print("🚀 Starting the application...")
    asyncio.run(run_forever())  # ✅ Ensures the app runs forever, even after errors
