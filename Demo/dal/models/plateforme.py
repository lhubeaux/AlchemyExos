from .base import Base
from sqlalchemy import Column, Integer, Text, String, Date, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Plateforme(Base):
	__tablename__ = "plateformes"

	plateforme_id = Column(Integer, primary_key=True, autoincrement=True)
	nom = Column(String(50), nullable=False, unique=True)
	fabricant = Column(String(50))

	jeux = relationship("Jeu", secondary="jeux_plateformes", back_populates="plateformes")
