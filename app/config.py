import os
from dotenv import load_dotenv
load_dotenv()

class Config:

    # SOC credentials
    SOC_URL = os.getenv('SOC_URL')
    SOC_USER = os.getenv('SOC_USER')
    SOC_PASSWORD = os.getenv('SOC_PASSWORD')
    USER_ID = os.getenv('USER_ID')

    # FILE PATHS
    DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')

    # DB credentials
    DB_DRIVER = os.getenv('DB_DRIVER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    DB_TABLE = os.getenv('DB_TABLE')
    LOG_TABLE = os.getenv('LOG_TABLE')
    CONNECTION_STRING = (
                        f"DRIVER={DB_DRIVER};"
                        f"SERVER={DB_HOST},{DB_PORT};"
                        f"DATABASE={DB_NAME};"
                        f"UID={DB_USER};PWD={DB_PASSWORD};"
                        f"Encrypt=yes;TrustServerCertificate=yes;"
                        )
    # INSTANCES
    INSTANCES = os.getenv('INSTANCES')

    # SELENIUM CONFIG
    HEADLESS = os.getenv('HEADLESS')
