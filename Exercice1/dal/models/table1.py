from .base import Base
from sqlalchemy import Column, Integer, Text, String, Date, DECIMAL, Boolean, ForeignKey

class table1(Base):
    __tablename__ = "table1"

    table_id = Column(Integer, primary_key = True, autoincrement = True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    lieu_naissance = Column(String(50))
    