from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from datetime import *
from sqlalchemy.orm import relationship
from .base import Base

class Livre(Base):
    __tablename__ = "livres"
    
    livre_id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(100), nullable=False)
    date_publication = Column(Integer) #Je ne veux mettre que l'année pour la date de publication
    prix = Column(DECIMAL(10,2))
    auteur_id = Column(Integer, ForeignKey("auteurs.auteur_id"), nullable=False)

    auteur = relationship("Auteur", back_populates="livres")
    genres = relationship("Genre", back_populates="livres", secondary="livres_genres")
    details = relationship("Details", back_populates="livre", uselist=False, cascade="all, delete-orphan")