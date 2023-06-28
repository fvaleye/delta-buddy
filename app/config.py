import logging
import os
from enum import Enum

from chromadb.config import Settings
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

found_dotenv = find_dotenv(".env")
if not found_dotenv:
    raise ValueError(
        "The .env file has not been found."
        "Please create it based on the .env.sample file and configure the environment variables."
    )

load_dotenv()


class ExecutionContext(Enum):
    """
    Define the execution context for the Delta-Buddy chatbot.
    """

    LOCAL = "local"
    DATABRICKS = "databricks"


class DatabricksServingMode(Enum):
    """
    Define the serving mode for the Delta-Buddy chatbot running in Databricks.
    """

    LOCAL = "local"
    NOTEBOOK_HOSTED_API = "notebook_hosted_api"
    NOTEBOOK_API = "notebook_api"


class Config(BaseModel):
    EXECUTION_CONTEXT: ExecutionContext = ExecutionContext[
        os.environ.get("EXECUTION_CONTEXT", "local").upper()
    ]
    SOURCE_DOCUMENTS_DIRECTORY: str = os.environ["SOURCE_DOCUMENTS_DIRECTORY"]
    PERSIST_DIRECTORY: str = os.environ["PERSIST_DIRECTORY"]
    SOURCE_DOCUMENTS_MAX_COUNT: int = int(os.environ["SOURCE_DOCUMENTS_MAX_COUNT"])
    PREPARATION_MODEL_NAME: str = os.environ["PREPARATION_MODEL_NAME"]
    DATABRICKS_MODEL_NAME: str = os.environ["DATABRICKS_MODEL_NAME"]
    DATABRICKS_CLUSTER_ID: str = os.environ.get("DATABRICKS_CLUSTER_ID", "")
    DATABRICKS_TEXT_TO_SQL_MODEL: str = os.environ.get(
        "DATABRICKS_TEXT_TO_SQL_MODEL", ""
    )
    DATABRICKS_NOTEBOOK_PATH: str = os.environ.get("DATABRICKS_NOTEBOOK_PATH", "")
    DATABRICKS_SERVER_HOSTNAME: str = os.environ.get("DATABRICKS_SERVER_HOSTNAME", "")
    DATABRICKS_LLM_PORT: int = int(os.environ.get("DATABRICKS_LLM_PORT", "0"))
    DATABRICKS_SERVING_MODE: DatabricksServingMode = DatabricksServingMode[
        os.environ.get("DATABRICKS_SERVING_MODE", "local").upper()
    ]
    DATABRICKS_HTTP_PATH = os.environ.get("DATABRICKS_HTTP_PATH", "")
    DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")


config = Config()

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=config.PERSIST_DIRECTORY,
    anonymized_telemetry=False,
)
