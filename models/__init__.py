from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
from .avito_ad import AvitoAd
from .base import Base


class Database:
    def __init__(
        self,
        db_url,
        pool_size=10,
        max_overflow=20,
    ):
        self.engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
