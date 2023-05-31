import logging
import multiprocessing
from multiprocessing.dummy import Pool
from typing import Iterator, List

from databricks import sql

from app.config import (
    DATABRICKS_HTTP_PATH,
    DATABRICKS_SERVER_HOSTNAME,
    DATABRICKS_TOKEN,
)
from app.databricks_utils.models import ColumnDefinition, TableDefinition


class DatabricksSQL:
    def __init__(
        self,
        host: str = DATABRICKS_SERVER_HOSTNAME,
        http_path: str = DATABRICKS_HTTP_PATH,
        access_token: str = DATABRICKS_TOKEN,
    ) -> None:
        self.host = host
        self.http_path = http_path
        self.access_token = access_token
        self.connection = None

    def _get_connection(self):
        if not self.connection:
            self.connection = sql.connect(
                server_hostname=self.host,
                http_path=self.http_path,
                access_token=self.access_token,
            )
        return self.connection

    def get_all_catalogs(self) -> List[str]:
        with self._get_connection().cursor() as c:
            catalog_names = c.catalogs().fetchall()
            for catalog_name in catalog_names:
                yield catalog_name[0]

    def get_tables(self, catalog_name: str) -> Iterator[TableDefinition]:
        with self._get_connection().cursor() as c:
            table_names = c.tables(catalog_name=catalog_name).fetchall()
            for table in table_names:
                yield TableDefinition(
                    catalog_name=table["TABLE_CAT"],
                    schema_name=table["TABLE_SCHEM"],
                    name=table["TABLE_NAME"],
                )

    def set_columns_in_table(self, table: TableDefinition) -> TableDefinition:
        with self._get_connection().cursor() as c:
            columns = c.columns(
                catalog_name=table.catalog_name,
                schema_name=table.schema_name,
                table_name=table.name,
            ).fetchall()
            table.columns = [
                ColumnDefinition(name=c["COLUMN_NAME"], type=c["TYPE_NAME"])
                for c in columns
            ]
            return table

    def set_metadata_in_table(self, table: TableDefinition) -> TableDefinition:
        with self._get_connection().cursor() as c:
            table_metadata = c.execute(
                f"DESCRIBE TABLE EXTENDED {table.catalog_name}.{table.schema_name}.{table.name};"
            ).fetchall()
            for metadata in table_metadata:
                if metadata["col_name"] == "Type":
                    table.type = metadata["data_type"]
                elif metadata["col_name"] == "Comment":
                    table.comment = metadata["data_type"]
                elif metadata["col_name"] == "Location":
                    table.location = metadata["data_type"]
                elif metadata["col_name"] == "Last access":
                    table.last_access = metadata["data_type"]
                elif metadata["col_name"] == "Owner Name":
                    table.owner_name = metadata["data_type"]
                elif metadata["col_name"] == "Created Time":
                    table.created_time = metadata["data_type"]
                elif metadata["col_name"] == "Created By":
                    table.created_by = metadata["data_type"]
                elif metadata["col_name"] == "Properties":
                    table.properties = metadata["data_type"]
                elif metadata["col_name"] == "Storage Properties":
                    table.storage_properties = metadata["data_type"]
            return table

    def prepare_table(
        self, table: TableDefinition, show_errors: bool
    ) -> TableDefinition:
        try:
            self.set_columns_in_table(table=table)
            self.set_metadata_in_table(table=table)
        except Exception as e:
            if show_errors:
                logging.info(
                    f"Ignoring this table {table} because of an error with the following message: {e}"
                )
            pass
        finally:
            return table

    def generate_tables_definition_asynchronously(
        self,
        processes: int = multiprocessing.cpu_count(),
        show_errors: bool = False,
    ) -> List[TableDefinition]:
        """
        This method will generate the table definitions asynchronously from Databricks catalog.

        :param processes: number of processes to use
        :param show_errors: if True, it will show the errors
        :return: the tables definitions
        """
        catalogs = self.get_all_catalogs()
        futures = list()

        def on_success(table: TableDefinition) -> TableDefinition:
            return str(table)

        def error(ex: Exception):
            logging.error(f"Failure: {ex}")

        with Pool(processes=processes) as pool:
            for catalog_name in catalogs:
                tables = self.get_tables(catalog_name=catalog_name)
                for table in tables:
                    futures.append(
                        pool.apply_async(
                            self.prepare_table,
                            args=[table, show_errors],
                            callback=on_success,
                            error_callback=error,
                        )
                    )
            for future in futures:
                result = future.get()
                if result:
                    logging.debug(f"Table definition loaded: {result}")
                    yield result
