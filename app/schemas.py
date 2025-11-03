from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DataRecordBase(BaseModel):
    name: str
    category: str
    value: float
    description: Optional[str] = None

class DataRecordCreate(DataRecordBase):
    pass

class DataRecord(DataRecordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_records: int
    categories: dict
    average_value: float
    last_updated: Optional[datetime] = None

class TopNResponse(BaseModel):
    records: list[DataRecord]
    count: int
