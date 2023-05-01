import csv
from sqlalchemy import create_engine, Table, Column, Float, Integer, MetaData, String
from alembic import op

# Подключение к базе данных
engine = create_engine('postgresql://student:@46.148.230.201:5432/geo_marketing')

# Определение структуры таблицы
metadata = MetaData()
commercial_premises = Table('commercial_premises', metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('price', Float),
    Column('square', Float),
    Column('address', String),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('link', String)
)

def upgrade():
    op.execute("""
        CREATE TABLE commercial_premises (
            id SERIAL PRIMARY KEY,
            title VARCHAR NOT NULL,
            price FLOAT NOT NULL,
            square FLOAT NOT NULL,
            address VARCHAR NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            link VARCHAR NOT NULL
        )
    """)

    # Чтение данных из CSV файла и вставка их в таблицу
    with open('path/to/commercial_premises.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # пропуск заголовочной строки
        for row in reader:
            stmt = commercial_premises.insert().values(
                title=row[0],
                price=float(row[1]),
                square=float(row[2]),
                address=row[3],
                latitude=float(row[4]),
                longitude=float(row[5]),
                link=row[6]
            )
            engine.execute(stmt)

def downgrade():
    op.execute("DROP TABLE commercial_premises")
