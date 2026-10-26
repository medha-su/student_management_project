from sqlalchemy import Column, Date, Integer, String
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(254), nullable=True, unique=True, index=True)
    phone = Column(String(30), nullable=True)
    course = Column(String(120), nullable=True)
    address = Column(String(300), nullable=True)
    enrollment_date = Column(Date, nullable=True)
