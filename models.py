from sqlalchemy import Table, Boolean, Column, Integer, String,DateTime
from database import Base

class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key= True, index=True)
        username = Column(String(50), unique=True)

class Post(Base):
        __tablename__ = 'posts'

        id = Column(Integer, primary_key=True, index=True)
        title =  Column(String(50))
        content = Column(String(100))
        user_Id = Column(Integer)

class Link(Base):
         __tablename__ = 'link'

         id = Column(Integer, primary_key=True, index=True)
         inf_id = Column(Integer)
         link = Column(String(50))
         link_description = Column(String(50))
         group_id = Column(Integer)
         link_tags = Column(String(50))
         #link_accessibility = Column(Integer)
         created_by = Column(Integer)
         created_datetime = Column(DateTime)
         updated_by = Column(Integer)
         updated_datetime = Column(DateTime)
         #accecibility = Column(Boolean)