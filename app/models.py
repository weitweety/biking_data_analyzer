from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from db import Base

class BikeTrip(Base):
    __tablename__ = "bike_trips"

    id = Column(Integer, primary_key=True, index=True)
    tripduration = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=False), nullable=False)
    stop_time = Column(DateTime(timezone=False), nullable=False)
    start_station_id = Column(Integer, nullable=True)
    start_station_name = Column(String(255), nullable=True)
    start_station_latitude = Column(Float, nullable=True)
    start_station_longitude = Column(Float, nullable=True)
    end_station_id = Column(Integer, nullable=True)
    end_station_name = Column(String(255), nullable=True)
    end_station_latitude = Column(Float, nullable=True)
    end_station_longitude = Column(Float, nullable=True)
    bike_id = Column(Integer, nullable=True)
    user_type = Column(String(50), nullable=True)
    birth_year = Column(Integer, nullable=True)
    gender = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return (
            f"<BikeTrip(id={self.id}, bike_id={self.bike_id}, start='{self.start_time}', "
            f"end='{self.stop_time}', duration={self.tripduration})>"
        )
