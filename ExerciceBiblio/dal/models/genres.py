from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Genre(Base):

    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(50))

    livres = relationship("Livre", back_populates="genres", secondary="livres_genres")