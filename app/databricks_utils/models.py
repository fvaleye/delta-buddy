from typing import List

from pydantic import BaseModel


class ColumnDefinition(BaseModel):
    """
    Definition of a column of a Databricks table.
    """

    name: str
    type: str


class TableDefinition(BaseModel):
    """
    Definition of a Databricks table.
    """

    catalog_name: str
    schema_name: str
    name: str
    comment: str = ""
    columns: List[ColumnDefinition] = list()
    type: str = ""
    created_time: str = ""
    last_access: str = ""
    created_by: str = ""
    owner_name: str = ""
    properties: List[str] = list()
    location: str = ""
    storage_properties: List[str] = list()
