"""
Définition de la classe Base pour tout les modèles.

C'est la clasee de base que tout les modèles vont hériter.

SqlAlchemy l'utilise pour créer les tables et gérer les mappings.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()