from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "mysql+mysqlconnector://root:mysql123@localhost:3306/linkshare"
#DB_URL = "mysql+mysqlconnector://root:mysql123@localhost:3306/linkshare"

engine = create_engine(URL_DATABASE, pool_size= 10, max_overflow= 30)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind= engine)

Base = declarative_base()