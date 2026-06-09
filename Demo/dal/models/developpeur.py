"""

Modèle developpeur

Relation : One-to-Many

un véveloppeur peut créer plusieurs jeux.
un je n'a qu'un seul développeur

En SQL Alchemy:
- Coté "1" Dev : on utilise relationship() avec une liste
- Coté "N" Jeu : on utilise relationship() + ForeignKey
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Developpeur(Base):
	__tablename__ = "developpeurs"

	developpeur_id = Column(Integer, primary_key=True, autoincrement=True)
	nom = Column(String(100), nullable=False, unique=True)
	pays = Column(String(50))

	# back_populates => Permet d'établir la relation en sens inverse et d'y accéder depuis l'aitre coté (jeu.developpeur)
	jeux = relationship("Jeu", back_populates="developpeur")