import asyncio
from app.config import PERSIST_DIRECTORY, PREPARATION_MODEL_NAME
from data_preparation.ingest_documents import ingest_documents_in_database
from data_preparation.prepare_documents import (
    prepare_documents_from_databricks,
    prepare_documents_from_github,
    prepare_documents_from_urls,
)
from data_preparation.utils import get_all_releases_notes_from_github_repository

if __name__ == "__main__":
    asyncio.run(
        prepare_documents_from_urls(
            urls=["https://www.vldb.org/pvldb/vol13/p3411-armbrust.pdf"]
        )
    )
    print("Preparation of the documents from URLs is done. ✅")
    asyncio.run(
        prepare_documents_from_github(
            github_urls=[
                "https://github.com/delta-io/delta",
                "https://github.com/delta-io/website",
                "https://github.com/delta-io/delta-docs",
            ],
        )
    )
    print("Preparation of the documents from the Github repositories is done. ✅")
    asyncio.run(
        get_all_releases_notes_from_github_repository(
            github_urls=[
                "https://github.com/delta-io/delta",
                "https://github.com/delta-io/delta-rs",
                "https://github.com/delta-io/delta-sharing",
                "https://github.com/delta-io/kafka-delta-ingest",
            ],
        )
    )
    print("Preparation of the documents from the Github releases notes is done. ✅")

    try:
        asyncio.run(prepare_documents_from_databricks(show_errors=False))
    except Exception:
        print("No Databricks connection configured, check the environments variables. ⚠️")
    print("Preparation of the documents from the Databricks environments is done. ✅")

    asyncio.run(
        ingest_documents_in_database(
            persist_directory=PERSIST_DIRECTORY,
            model_name=PREPARATION_MODEL_NAME,
        )
    )
    print(f"The documents have been ingested in the Chroma vectorized database in {PERSIST_DIRECTORY}. ✅")

