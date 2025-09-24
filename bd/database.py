import os
from sqlalchemy import create_engine  # coneccion con la base de datos
from sqlalchemy.orm import sessionmaker  # utilizar clases declarativas
from sqlalchemy.ext.declarative import declarative_base


sqliteName = 'movies.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
databaseUrl = f'sqlite:///{os.path.join(base_dir, sqliteName)}'

engine = create_engine(databaseUrl, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
