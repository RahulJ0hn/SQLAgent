from pydantic import BaseModel


class ColumnMetadata(BaseModel):
    name: str
    data_type: str
    is_nullable: str
    description: str = ""


class TableMetadata(BaseModel):
    table_name: str
    description: str
    columns: list[ColumnMetadata]
