from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class BikeTripBase(BaseModel):
    tripduration: int
    start_time: datetime
    stop_time: datetime
    start_station_id: Optional[int] = None
    start_station_name: Optional[str] = None
    start_station_latitude: Optional[float] = None
    start_station_longitude: Optional[float] = None
    end_station_id: Optional[int] = None
    end_station_name: Optional[str] = None
    end_station_latitude: Optional[float] = None
    end_station_longitude: Optional[float] = None
    bike_id: Optional[int] = None
    user_type: Optional[str] = None
    birth_year: Optional[int] = None
    gender: Optional[int] = None

class BikeTripCreate(BikeTripBase):
    pass

class BikeTrip(BikeTripBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_records: int

class TopNResponse(BaseModel):
    records: List[BikeTrip]
    count: int