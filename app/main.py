import asyncio
import uuid
import os
import psutil
import uvicorn
from config import Config
from database import get_pending_records, get_db, update_table
from logs import log_execution
from sqlalchemy.ext.asyncio import AsyncSession
from controller import app  # ✅ Import FastAPI app
import gc
from web_driver import criar_guia

e = Config()
semaphore = asyncio.Semaphore(2)  # Limit concurrency to 2 WebDrivers

user_data = {
    "SOC_USER" : e.SOC_USER,
    "SOC_PASSWORD" : e.SOC_PASSWORD,
    "SOC_ID" : e.USER_ID
}


@log_execution()
async def process_record(exec_id, guia_id, db: AsyncSession, record: dict):
    """Handles processing for each record with controlled concurrency."""
    async with semaphore:  # ✅ Ensure only 2 WebDrivers run at a time
        print(f"Processing Guia ID: {guia_id} with Execution ID: {exec_id}")

        resultado = criar_guia(record, user_data, exec_id, db)

        data = record
        if data['status'] == "success":
            print('uhu')
        else:
            print('aaah')

        try:
            return {"status": "success", "message": "Operation completed", "data": data}
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

                tasks = [process_record(execution_id, record.get("idsydle", "unknown"), db, record) for record in response["data"]]
                await asyncio.gather(*tasks)

                await asyncio.sleep(300)  # ✅ Prevent instant looping

                gc.collect()  # ✅ Force garbage collection
        finally:
            await db.close()  # ✅ Ensure the DB connection is properly closed


async def run_fastapi():
    """Runs FastAPI server in the background."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8888, log_level="info", workers=1)
    server = uvicorn.Server(config)
    await server.serve()

async def run_main():
    """Runs both FastAPI and the main processing loop concurrently."""
    await asyncio.gather(
        main_processing()  # ✅ Run main processing function
    )        #run_fastapi(),# ✅ Run FastAPI API in the background

async def run_forever():
    """Ensures FastAPI and processing loop keep running indefinitely, restarting on failure."""
    while True:
        try:
            await run_main()
        except Exception as e:
            print(f"⚠️ Critical error: {e}")
            print("🔄 Restarting script in 30 seconds...")
            await asyncio.sleep(5)  # ✅ Prevent rapid crashes & CPU overload

if __name__ == "__main__":
    print("🚀 Starting the application...")
    #asyncio.run(run_fastapi())
    asyncio.run(run_forever())  # ✅ Ensures the app runs forever, even after errors