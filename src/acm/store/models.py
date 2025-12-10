from pydantic import BaseModel


class Record(BaseModel):
    uuid: str
    alias: str
    path: str
    hash: str
    content: bytes
    created_at: int
    updated_at: int


class Store(BaseModel):
    records: dict[str, Record]
    current_uuid: str
    version: int
