from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///example.db')  # Replace with your database connection URL
Base = declarative_base()

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

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create a new Avito ad with parking availability
ad1 = AvitoAd(square=100.0, price=5000.0, address='123 Main St', latitude=55.12345,
              longitude=37.67890, link='https://example.com/ad1', parking_available=True)
session.add(ad1)
session.commit()

# Get a list of Avito ads
ads = session.query(AvitoAd).all()
print(ads)
