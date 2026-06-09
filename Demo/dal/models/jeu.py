from .base import Base
from sqlalchemy import Column, Integer, Text, String, Date, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Jeu(Base):
	__tablename__ = "jeux"

	jeu_id = Column(Integer, primary_key=True, autoincrement=True)
	titre = Column(String(200), nullable=False)
	date_sortie = Column(Date)
	prix = Column(DECIMAL(10,2))

	developpeur_id = Column(Integer, ForeignKey("developpeurs.developpeur_id"), nullable=False)

	# Relation 1 : One To One avec DetailsJeu
	# useList => Pour préciser que nous sommes en 1:1 et non en 1:N
	details = relationship("DetailJeu", back_populates="jeu", uselist=False, cascade="all, delete-orphan")

	# One-to-many : inverse
	developpeur = relationship("Developpeur", back_populates="jeux")

	plateformes = relationship("Plateforme", secondary="jeux_plateformes", back_populates="jeux")

	# plateformes