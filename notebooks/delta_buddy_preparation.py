# Databricks notebook source
# MAGIC %md
# MAGIC #Databricks preparation notebook

# COMMAND ----------

# MAGIC %pip install -r ../requirements.txt
# MAGIC dbutils.library.restartPython()
# MAGIC print("Python dependencies are installed ✅")

# COMMAND ----------

dbutils.widgets.dropdown(
    "databricks_clean",
    "False",
    ["True", "False"],
    "Clean the Chromadb and documents directory.",
)
dbutils.widgets.dropdown(
    "databricks_metadata",
    "False",
    ["True", "False"],
    "Generate Databricks Metadata.",
)

# COMMAND ----------

from app.config import (
    PERSIST_DIRECTORY,
    PREPARATION_MODEL_NAME,
    SOURCE_DOCUMENTS_DIRECTORY,
)


def prepare_os() -> None:
    import os
    import shutil

    if dbutils.widgets.get("databricks_clean") == "True":
        shutil.rmtree(f"/{SOURCE_DOCUMENTS_DIRECTORY}", ignore_errors=True)

    os.makedirs(f"/{SOURCE_DOCUMENTS_DIRECTORY}", exist_ok=True)


prepare_os()
print("Os is prepared ✅")

# COMMAND ----------

from app.config import (
    PERSIST_DIRECTORY,
    PREPARATION_MODEL_NAME,
    SOURCE_DOCUMENTS_DIRECTORY,
)
from data_preparation.ingest_documents import ingest_documents_in_database
from data_preparation.prepare_documents import (
    prepare_documents_from_databricks,
    prepare_documents_from_github,
    prepare_documents_from_urls,
)
from data_preparation.utils import get_all_releases_notes_from_github_repository

await prepare_documents_from_urls(
    urls=[
        "https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf",
    ]
)
print("Preparation of the documents from URLs is done. ✅")

await prepare_documents_from_github(
    github_urls=[
        "https://github.com/delta-io/delta",
        "https://github.com/delta-io/website",
        "https://github.com/delta-io/delta-docs",
    ],
)
print("Preparation of the documents from the Github repositories is done. ✅")

await get_all_releases_notes_from_github_repository(
    github_urls=[
        "https://github.com/delta-io/delta",
        "https://github.com/delta-io/delta-rs",
        "https://github.com/delta-io/delta-sharing",
        "https://github.com/delta-io/kafka-delta-ingest",
    ],
)
print("Preparation of the documents from the Github releases notes is done. ✅")

# COMMAND ----------

if dbutils.widgets.get("databricks_metadata") == "True":
    await prepare_documents_from_databricks()
    print("Preparation of the documents from the Databricks environments is done. ✅")

# COMMAND ----------

await ingest_documents_in_database(
    persist_directory=PERSIST_DIRECTORY,
    model_name=PREPARATION_MODEL_NAME,
)
print("The documents have been ingested in the Chroma vectorized database. ✅")
