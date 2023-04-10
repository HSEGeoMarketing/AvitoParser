from sqlalchemy import Column, Integer, String, Float, Boolean
from .base import Base

class AvitoAd(Base):
    __tablename__ = 'avito_ads'

    id = Column(Integer, primary_key=True)
    square = Column(Float)
    price = Column(Float)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    link = Column(String)
    parking_available = Column(Boolean, default=False)  # New column for parking availability

    def __repr__(self):
        return f'<AvitoAd(square={self.square}, price={self.price}, address={self.address}, ' \
               f'latitude={self.latitude}, longitude={self.longitude}, link={self.link}, ' \
               f'parking_available={self.parking_available})>'