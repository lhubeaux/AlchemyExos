from dal.database import get_session, init_db, test_connexion
from datetime import *
from decimal import Decimal
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, update
from dal.database import get_session, init_db, test_connexion
from dal.models import Auteur, Livre, Genre, Details



def seed(session):
	#création des auteurs
	sanderson = Auteur(
		nom="Sanderson",
		prenom= "Brandon",
		pays="USA"
    )
	session.add(sanderson)
	
	tolkien = Auteur(
		nom="Tolkien",
		prenom= "J.R.R.",
		pays="Angleterre"
    )
	session.add(tolkien)
	
    #création des genres
	fantasy = Genre(nom="Fantasy")
	session.add(fantasy)
	
	sci_fi = Genre(nom="Science fiction")
	session.add(sci_fi)

	fiction = Genre(nom="Fiction")
	session.add(fiction)

	#création des livres
	lotr = Livre(titre="Le Seigneur des Anneaux",
			  date_publication=1955,
			  prix=50,
			  auteur=tolkien
			  )
	
	stormlight = Livre(titre="The Stormlight Archive",
			  date_publication=2010,
			  prix=30,
			  auteur=sanderson
			  )
	
	sunlit = Livre(titre="The Sunlit Man",
			  date_publication=2024,
			  prix=25,
			  auteur=sanderson
			  )
	
	#ajout des détails
	lotr.details = Details(resume="Un groupe de héros partent à l'aventure pour détruire l'anneau unique afin de défaire Sauron le seigneur des ténèbres.",
			nbre_pages=1237,
			note=20)
	
	stormlight.details = Details(resume="Plusieurs protagonistes essayent de survivre sur le monde de Roshar, ravagé par des tempêtes.",
			nbre_pages=1167,
			note=19)
	
	sunlit.details = Details(resume="Un mystérieux héros fuit de planète en planète un empire tyrannique jusqu'au jour où il découvre un peuple qu'il ne peut se résoudre à abandonner.",
			nbre_pages=380,
			note=14)
	
	#ajout des genres à chaque livre
	lotr.genres.append(fantasy)
	lotr.genres.append(fiction)

	stormlight.genres.append(fantasy)
	stormlight.genres.append(fiction)

	sunlit.genres.append(fiction)
	sunlit.genres.append(sci_fi)

	session.add_all([lotr, stormlight, sunlit])
	session.commit()

def liste_livres(session):
	livres = session.query(Livre).options(joinedload(Livre.auteur), joinedload(Livre.details),selectinload(Livre.genres)).all()

	for livre in livres:
		print(f"\n {livre.titre} (ID: {livre.livre_id})")
		print(f"Auteur : 	{livre.auteur.prenom + ' ' + livre.auteur.nom}")
		print(f"Prix : 		{livre.prix}€")
		print(f"Année : 	{livre.date_publication}")
		print(f"Genres : 	{', '.join([genre.nom for genre in livre.genres])}")

def creer_livre(session):
	print("\n" + "=" * 50)
	print("AJOUT D'UN LIVRE")
	print("=" * 50)

	#Ajout des infos de base du livre
	titre = input("Titre du livre: \n")
	date_publication = int(input("Année de publication du livre: \n"))
	prix = Decimal(input("Prix du livre : \n"))

	#Ajout de l'auteur
	print("\n === Auteurs déjà dans la base de données ===\n")
	auteurs = session.query(Auteur).all()
	for a in auteurs:
		print(f"ID : {a.auteur_id} - {a.prenom + ' ' + a.nom}")
	
	choix_auteur = input("\n Veuillez entrer l'ID d'un auteur existant ou appuyez sur n pour en créer un nouveau \n").lower()

	if choix_auteur == "n":
		#On crée un nouvel auteur
		nom_auteur = input("Nom du nouvel auteur : \n")
		prenom_auteur = input("Prénom du nouvel auteur : \n")
		pays_auteur = input("Pays d'origine du nouvel auteur : \n")
		new_auteur = Auteur(nom=nom_auteur, prenom=prenom_auteur, pays=pays_auteur)
		session.add(new_auteur)
		session.flush()
		print(f"\nNouvel auteur créé: \n {new_auteur.prenom + ' ' + new_auteur.nom} avec l'ID {new_auteur.auteur_id}")
	else:
		new_auteur = session.get(Auteur, int(choix_auteur))
	#Création de l'objet livre en lui même
	new_livre = Livre(titre=titre, date_publication=date_publication, prix=prix, auteur=new_auteur)

	#Ajout des détails
	print("\n=== Détails du nouveau livre ===\n")
	resume=input("Saisissez un cours résumé du nouveau livre: \n")
	nbre_pages=int(input("Saisissez le nombre de pages du nouveau livre: \n"))
	note=int(input("Saisissez la note obtenue par le livre : \n"))

	new_livre.details = Details(resume=resume, nbre_pages=nbre_pages, note=note)

	#Ajout des genres
	print("\n=== Genres déjà présents dans la DB ===\n")
	genres = session.query(Genre).all()
	for g in genres:
		print(f"{g.nom} - ID : {g.genre_id}")
	id_genres = input("Saisissez les ID des genres à ajouter à ce livre, séparés par une virgule. \nSaisissez n pour ajouter un nouveau genre : \n")
	
	if id_genres == "n":
		new_genre = input("Entrez le nouveau nom du genre à ajouter: \n")
		genre = Genre(nom=new_genre)
		session.add(genre)
		new_livre.genres.append(genre)

	else:
		for id in id_genres.split(","):
			genre = session.get(Genre, int(id.strip()))
			if genre:
				new_livre.genres.append(genre)
			else:
				print("Genre introuvable!")

	session.add(new_livre)
	session.commit()
	print(f"Le livre '{titre}' a été ajouté avec succès !")


def modifier_livre(session):
	print("\n" + "=" * 50)
	print("MODIFICATION D'UN LIVRE")
	print("=" * 50)
	
	liste_livres(session)

	a_modifier = int(input("Veuillez entrer l'ID du livre à modifier : \n"))
	livre = session.query(Livre).get(a_modifier)

	if not livre:
		print("❗ Impossible de trouver ce livre!")
		return
	
	print(f"Modification du livre '{livre.titre}' ID : {livre.livre_id}")
	print(f"Appuyez sur entrée pour garder les détails actuels.")

	#Modification des attributs du livre en lui-même
	nouveau_titre = input("Veuillez entrer le nouveau titre : \n")
	if nouveau_titre:
		livre.titre = nouveau_titre
	
	nouvelle_date = (input("Veuillez entrer la nouvelle date : \n"))
	if nouvelle_date:
		livre.date_publication = int(nouvelle_date)

	nouveau_prix = (input("Veuillez entrer le nouveau prix : \n"))
	if nouveau_prix:
		livre.prix = Decimal(nouveau_prix)

	#Modification des détails
	if livre.details:
		print("\n === Détails actuel du livre ===\n")
		nouveau_resume = input(f"Nouveau résumé du livre {livre.titre} : \n")
		if nouveau_resume:
			livre.details.resume = nouveau_resume

		nouveau_nbr = (input("Nouveau nombre de pages: \n"))
		if nouveau_nbr:
			livre.details.nbre_pages = int(nouveau_nbr)

		nouvelle_note = (input("Nouvelle note : \n"))
		if nouvelle_note:
			livre.details.note = int(nouvelle_note)

	session.commit()
	print(f"Détails du livre '{livre.titre}' modifiés avec succès!")

def supprimer_livre(session):
	liste_livres(session)
	a_supprimer = int(input("Veuillez entrer l'ID du livre à supprimer : \n"))
	livre = session.get(Livre, a_supprimer)
	if livre:
		choix = input(f"Voulez vous supprimer le livre {livre.titre}? y/n\n")
		if choix == "y":
			session.delete(livre)
			session.commit()
			print("Livre supprimé avec succès!")
		elif choix == "n":
			print("Très bien, ce livre ne sera pas supprimé")
	else:
		print("Ce livre n'existe pas!")






def main():
	if not test_connexion():
		return
	
	init_db(delete=True)
	session = get_session()
	seed(session)


	retry = True
	while retry:
		print("\n" + "*" * 50)

		print("MENU CRUD")
		print( "*" * 30)
		print("[1] Lister tous les livres")
		print("[2] Créer un nouveau livre")
		print("[3] Modifier un livre existant")
		print("[4] Supprimer un livre")
		print("[5] Reset (drop + create)")
		print("[0] Quitter")
		print( "*" * 30)

		choix = int(input("\nVotre choix :\n"))

		if choix == 1:
			liste_livres(session)
		elif choix == 2 :
			creer_livre(session)
		elif choix == 3 :
			modifier_livre(session)
		elif choix == 4:
			supprimer_livre(session)
		elif choix == 5:
			validation = input("Reinitilialiser toutes les tables ? (o/n) : ").lower()
			if validation == 'o':
				init_db(delete=True)
				seed(session)
		elif choix == 0:
			print("Bye bye !!!")
			retry = False
		else:
			print("Choix invalide")


if __name__ == "__main__":
	main()