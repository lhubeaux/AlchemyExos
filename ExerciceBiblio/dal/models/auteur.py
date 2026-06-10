from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Auteur(Base):
    __tablename__ = "auteurs"

    auteur_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    pays = Column(String(50))

    livres = relationship("Livre", back_populates="auteur")