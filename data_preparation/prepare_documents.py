from typing import List

from data_preparation.utils import (
    clone_github_repositories,
    download_document_from_urls,
    from_databricks_environment,
)


async def prepare_documents_from_urls(
    urls: List[str],
) -> bool:
    await download_document_from_urls(urls=urls)


async def prepare_documents_from_github(github_urls: List[str]) -> None:
    await clone_github_repositories(
        github_urls=github_urls,
    )


async def prepare_documents_from_databricks(show_errors: bool = False) -> None:
    await from_databricks_environment(show_errors=show_errors)
