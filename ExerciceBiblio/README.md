# ExerciceBiblio

Application de gestion de bibliothèque construite avec SQLAlchemy et SQL Server. Permet la gestion complète de livres, auteurs, genres et détails via une interface en ligne de commande.

## Prérequis

- Python 3.x
- SQL Server accessible à `GOSVDI208\TFTIC`
- Base de données `ExoBiblio` créée sur l'instance

## Installation

```bash
pip install -r requirements.txt
```

**Dépendances :**
- `SQLAlchemy==2.0.50` — ORM pour la gestion de la base de données
- `pyodbc==5.3.0` — Driver ODBC pour la connexion SQL Server

## Lancement

```bash
python main.py
```

Au démarrage, l'application :
1. Teste la connexion à la base de données
2. Crée les tables si elles n'existent pas
3. Insère des données initiales (seed)
4. Affiche le menu principal

## Structure du projet

```
ExerciceBiblio/
├── main.py                 # Point d'entrée — menu CLI et opérations CRUD
├── requirements.txt
└── dal/                    # Data Access Layer
    ├── database.py         # Moteur, session et test de connexion
    └── models/
        ├── base.py         # Base déclarative SQLAlchemy
        ├── auteur.py       # Modèle Auteur
        ├── livre.py        # Modèle Livre
        ├── details.py      # Modèle Détails
        ├── genres.py       # Modèle Genre
        └── __init__.py     # Imports et table d'association livres_genres
```

## Modèle de données

### Entités

| Entité | Table | Description |
|--------|-------|-------------|
| `Auteur` | `auteurs` | Auteur d'un livre |
| `Livre` | `livres` | Livre de la bibliothèque |
| `Details` | `details` | Résumé, nombre de pages et note d'un livre |
| `Genre` | `genres` | Genre littéraire |

### Schéma

```
Auteur (1) ──────< (N) Livre
                        │
                        ├── (1) Details     [One-to-One, cascade delete]
                        │
                        └── (N) Genre       [Many-to-Many via livres_genres]
```

### Détail des colonnes

**Auteur**
| Colonne      | Type        | Contraintes        |
|--------------|-------------|--------------------|
| `auteur_id`  | Integer     | PK, auto-increment |
| `nom`        | String(100) | NOT NULL           |
| `prenom`     | String(100) | NOT NULL           |
| `pays`       | String(50)  | nullable           |

**Livre**
| Colonne            | Type          | Contraintes            |
|--------------------|---------------|------------------------|
| `livre_id`         | Integer       | PK, auto-increment     |
| `titre`            | String(100)   | NOT NULL               |
| `date_publication` | Integer       | Année uniquement       |
| `prix`             | DECIMAL(10,2) | —                      |
| `auteur_id`        | Integer       | FK → auteurs, NOT NULL |

**Details**
| Colonne     | Type    | Contraintes      |
|-------------|---------|------------------|
| `livre_id`  | Integer | PK, FK → livres  |
| `resume`    | Text    | —                |
| `nbre_pages`| Integer | —                |
| `note`      | Integer | —                |

**Genre**
| Colonne    | Type       | Contraintes        |
|------------|------------|--------------------|
| `genre_id` | Integer    | PK, auto-increment |
| `nom`      | String(50) | —                  |

## Fonctionnalités

### Menu principal

| Option | Action |
|--------|--------|
| 1 | Lister tous les livres |
| 2 | Ajouter un livre |
| 3 | Modifier un livre |
| 4 | Supprimer un livre |
| 0 | Quitter |

### Opérations CRUD

- **Lister** — Affiche titre, auteur, prix, année et genres de chaque livre. Utilise `joinedload()` pour auteur/détails et `selectinload()` pour les genres afin d'éviter le problème N+1.
- **Créer** — Saisie interactive : informations du livre, sélection ou création d'un auteur, détails, genres.
- **Modifier** — Mise à jour sélective : appuyer sur Entrée conserve la valeur actuelle d'un champ.
- **Supprimer** — Suppression avec confirmation. La suppression d'un livre entraîne la suppression en cascade de ses détails.

## Points d'implémentation notables

- **Chargement eager** (`joinedload` / `selectinload`) pour optimiser les requêtes
- **Contrôle manuel des transactions** — `autocommit=False`, `autoflush=False`
- **Cascade delete** sur la relation `Livre → Details`
- **`Decimal`** pour les prix (évite les erreurs de virgule flottante)
- **Authentification Windows** pour la connexion SQL Server (pas de mot de passe stocké)
