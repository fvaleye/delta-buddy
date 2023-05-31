import glob
from os.path import isfile
from typing import List

import aiofiles
from aiofiles.os import os
from aiohttp import ClientSession
from git import Repo

from app.config import DATABRICKS_SERVER_HOSTNAME, SOURCE_DOCUMENTS_DIRECTORY
from app.databricks_utils.manager import DatabricksManager
from app.databricks_utils.sql_client import DatabricksSQL
from data_preparation.ingest_documents import LOADER_MAPPING


async def download_document_from_urls(
    urls: List[str],
    method: str = "GET",
    timeout_in_seconds: int = 300,
    chunks: int = 1024,
) -> List[str]:
    async with ClientSession() as session:
        for url in urls:
            filename = url.split("/")[-1]
            if not os.path.exists(f"{SOURCE_DOCUMENTS_DIRECTORY}/{filename}"):
                response = await session.request(
                    method=method, url=url, timeout=timeout_in_seconds
                )
                async for data in response.content.iter_chunked(chunks):
                    async with aiofiles.open(
                        f"{SOURCE_DOCUMENTS_DIRECTORY}/{filename}", "ba"
                    ) as file:
                        await file.write(data)
        return urls


async def keep_only_valid_files_for_ingestion(
    path: str, mapping: List[str] = LOADER_MAPPING.keys()
):
    file_list = glob.glob(f"{path}/**", recursive=True)
    for file in [f for f in file_list if isfile(f) and not f.endswith(tuple(mapping))]:
        os.remove(file)


async def clone_github_repositories(github_urls: List[str]) -> List[str]:
    github_repository_names = []
    for github_url in github_urls:
        repository_name = github_url.split("/")[-1]
        github_repository_names.append(repository_name)
        path = f"{SOURCE_DOCUMENTS_DIRECTORY}/github_repositories/{repository_name}"
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            Repo.clone_from(github_url, path)
            await keep_only_valid_files_for_ingestion(path=path)


async def get_all_releases_notes_from_github_repository(
    github_urls: List[str], method: str = "GET"
) -> None:
    """
    Get all releases notes from a Github repository and save them in a file.

    :param directory:
    :param github_urls:
    :param method:
    :return:
    """
    async with ClientSession() as session:
        for github_url in github_urls:
            repository_name = github_url.split("/")[-1]
            os.makedirs(
                f"{SOURCE_DOCUMENTS_DIRECTORY}/github_repositories",
                exist_ok=True,
            )
            path = (
                f"{SOURCE_DOCUMENTS_DIRECTORY}/github_repositories/"
                f"{repository_name}_releases.txt"
            )
            if not os.path.exists(path):
                github_repository = github_url.split("/")[-2] + "/" + repository_name
                response = await session.request(
                    method=method,
                    url=f"https://api.github.com/repos/"
                    f"{github_repository}/releases?per_page=1000",
                )
                content = await response.json()
                if content:
                    async with aiofiles.open(
                        path,
                        "w",
                    ) as file:
                        releases = [
                            (
                                f'Release Notes: This is the Github Release version {str(t["tag_name"])}'
                                f' of {repository_name}, with url {t["url"]}, by the author {t["author"]["login"]},'
                                f' published on Github at {t["published_at"]} with the following content: \n',
                                f'{os.linesep.join([s for s in str(t["body"]).strip().splitlines() if s])} \n\n',
                            )
                            for t in content
                        ][::-1]
                        for release in releases:
                            for item in release:
                                if item:
                                    await file.write(item)


async def write_line_document(
    file_name: str, item: str, extension: str = "txt", mode: str = "w"
) -> None:
    async with aiofiles.open(
        f"{SOURCE_DOCUMENTS_DIRECTORY}/{file_name}.{extension}",
        mode,
    ) as file:
        await file.write(item)


async def from_databricks_environment(
    databricks_sql: DatabricksSQL = DatabricksSQL(),
    databricks_manager: DatabricksManager = DatabricksManager(),
    show_errors: bool = False,
) -> None:
    file_name = "databricks_alerts"
    for alert in databricks_manager.list_alerts():
        await write_line_document(file_name=file_name, item="", mode="w")
        await write_line_document(
            file_name=file_name,
            item=f"This is an alert definition of the "
            f"Databricks[{DATABRICKS_SERVER_HOSTNAME}] account:\n{alert}\n",
            mode="a",
        )
    file_name = "databricks_unity_catalog"
    for table in databricks_manager.list_catalog(show_errors=show_errors):
        await write_line_document(file_name=file_name, item="", mode="w")
        await write_line_document(
            file_name=file_name,
            item=f"This is a table definition from "
            f"Databricks[{DATABRICKS_SERVER_HOSTNAME}] Unity catalog of the "
            f"Databricks account:\n{table}\n",
            mode="a",
        )
    file_name = "databricks_clusters"
    for cluster in databricks_manager.list_clusters():
        await write_line_document(file_name=file_name, item="", mode="w")
        await write_line_document(
            file_name=file_name,
            item=f"This is a cluster definition of the "
            f"Databricks[{DATABRICKS_SERVER_HOSTNAME}] account:\n{cluster}\n",
            mode="a",
        )
    file_name = "databricks_ml_models"
    for model in databricks_manager.list_models():
        await write_line_document(file_name=file_name, item="", mode="w")
        await write_line_document(
            file_name=file_name,
            item=f"This is a ML model definition of the "
            f"Databricks[{DATABRICKS_SERVER_HOSTNAME}] account:\n{model}\n",
            mode="a",
        )

    file_name = "databricks_tables"
    for table in databricks_sql.generate_tables_definition_asynchronously(
        show_errors=show_errors
    ):
        await write_line_document(file_name=file_name, item="", mode="w")
        await write_line_document(
            file_name=file_name,
            item=f"This is a table definition of the "
            f"Databricks account catalog:\n{table.json()}\n",
            mode="a",
        )
