from .base import Base
from .jeu import Jeu
from .detail_jeu import DetailJeu
from .developpeur import Developpeur
from .plateforme import Plateforme

from sqlalchemy import Column, Integer, String, Table, ForeignKey

jeux_plateformes = Table(
	"jeux_plateformes",
	Base.metadata,
	Column("jeu_id", Integer, ForeignKey("jeux.jeu_id"), primary_key=True),
	Column("plateforme_id", Integer, ForeignKey("plateformes.plateforme_id"), primary_key=True)
)