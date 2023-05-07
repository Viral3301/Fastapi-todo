from database import Base
from sqlalchemy import Column,Integer,String,Date,func
from datetime import datetime

class Post(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    task_title = Column(String)
    task_body = Column(String)
    creation_date = Column(Date, default=datetime.now())