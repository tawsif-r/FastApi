from sqlalchemy import Column, Integer, String, DateTime,Boolean,Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime,timezone

Base = declarative_base()

class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50),unique=True, nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(Float,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

class Exclusion(Base):
    __tablename__ = 'exclusions'

    id = Column(Integer,primary_key=True,index=True)
    description = Column(String(300),nullable=True)
    price_deduct = Column(Float,nullable=True)
    is_active = Column(Boolean,default=True)
    updated_at = Column(DateTime,default=lambda:datetime.now(timezone.utc),nullable=True)