import logging
import os
from enum import Enum

from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


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


# Define the folder for storing database
EXECUTION_CONTEXT = ExecutionContext[
    os.environ.get("EXECUTION_CONTEXT", "local").upper()
]
SOURCE_DOCUMENTS_DIRECTORY = os.environ["SOURCE_DOCUMENTS_DIRECTORY"]
PERSIST_DIRECTORY = os.environ["PERSIST_DIRECTORY"]
SOURCE_DOCUMENTS_MAX_COUNT = os.environ["SOURCE_DOCUMENTS_MAX_COUNT"]
PREPARATION_MODEL_NAME = os.environ["PREPARATION_MODEL_NAME"]
DATABRICKS_MODEL_NAME = os.environ["DATABRICKS_MODEL_NAME"]
DATABRICKS_CLUSTER_ID = os.environ.get("DATABRICKS_CLUSTER_ID", "")
DATABRICKS_TEXT_TO_SQL_MODEL = os.environ.get("DATABRICKS_TEXT_TO_SQL_MODEL", "")
DATABRICKS_NOTEBOOK_PATH = os.environ.get("DATABRICKS_NOTEBOOK_PATH", "")
DATABRICKS_SERVER_HOSTNAME = os.environ.get("DATABRICKS_SERVER_HOSTNAME", "")
DATABRICKS_HTTP_PATH = os.environ.get("DATABRICKS_HTTP_PATH", "")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
DATABRICKS_LLM_PORT = os.environ.get("DATABRICKS_LLM_PORT", 8888)
DATABRICKS_SERVING_MODE = DatabricksServingMode[
    os.environ.get("DATABRICKS_SERVING_MODE", "notebook_hosted_api").upper()
]

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=PERSIST_DIRECTORY,
    anonymized_telemetry=False,
)
