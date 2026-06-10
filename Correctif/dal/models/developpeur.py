from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

if TYPE_CHECKING:
    from .jeu import Jeu

class Developpeur(Base):
    __tablename__ = "developpeurs"

    developpeur_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False, unique=True)
    pays = Column(String(50))

    jeux = relationship("Jeu", back_populates="developpeur")

    jeux = relationship(lambda: Jeu.__name__, back_populates="developpeur")