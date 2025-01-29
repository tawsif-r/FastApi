from sqlalchemy import Column, Integer, String, DateTime,Boolean,Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50),unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(Float,nullable=True)
    is_active = Column(Boolean, default=True)

