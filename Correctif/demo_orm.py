def creer_jeux(session):
    """
    Fonction pour créer un nouveau jeu de manière interactive.
    On demande à l'utilisateur toutes les infos nécessaires (titre, date, prix, développeur, détails, plateformes).
    On crée les objets et on les lie entre eux grâce aux relations SQLAlchemy.
    """
    print("\n" + "=" * 50)
    print("CRÉATION D'UN NOUVEAU JEU")
    print("=" * 50)

    # === 1. Récupération des infos de base du jeu ===
    titre = input("Titre du jeu : ").strip()
    date_str = input("Date de sortie (format AAAA-MM-JJ) : ").strip()
    date_sortie = date.fromisoformat(date_str)          # Conversion string → objet date
    prix = Decimal(input("Prix du jeu (ex: 59.99) : ").strip())

    # === 2. Choix ou création du développeur ===
    print("\n--- Développeurs existants ---")
    developpeurs = session.query(Developpeur).all()
    for dev in developpeurs:
        print(f"  {dev.developpeur_id} - {dev.nom} ({dev.pays})")

    choix_dev = input("\nID du développeur existant ou tape 'n' pour en créer un nouveau : ").strip().lower()

    if choix_dev == "n":
        # Création d'un nouveau développeur
        nom_dev = input("Nom du développeur : ").strip()
        pays_dev = input("Pays du développeur : ").strip()
        developpeur = Developpeur(nom=nom_dev, pays=pays_dev)
        session.add(developpeur)
        session.flush()   # On flush pour avoir l'ID tout de suite
        print(f"Nouveau développeur créé avec l'ID {developpeur.developpeur_id}")
    else:
        # Récupération du développeur existant
        developpeur = session.query(Developpeur).get(int(choix_dev))

    # === 3. Création de l'objet Jeu ===
    nouveau_jeu = Jeu(
        titre=titre,
        date_sortie=date_sortie,
        prix=prix,
        developpeur=developpeur   # On lie directement le développeur grâce à la relation
    )

    # === 4. Ajout des détails du jeu (relation One-to-One) ===
    print("\n--- Détails du jeu ---")
    description = input("Description du jeu : ").strip()
    note_metacritic = int(input("Note Metacritic (0-100) : ").strip())
    multijoueur = input("Multijoueur ? (o/n) : ").strip().lower() == "o"

    nouveau_jeu.details = DetailJeu(
        description=description,
        note_metacritic=note_metacritic,
        multijoueur=multijoueur
    )

    # === 5. Ajout des plateformes (relation Many-to-Many) ===
    print("\n--- Plateformes existantes ---")
    plateformes = session.query(Plateforme).all()
    for plat in plateformes:
        print(f"  {plat.plateforme_id} - {plat.nom} ({plat.fabricant})")

    ids_plateformes = input("\nIDs des plateformes à ajouter (séparés par des virgules, ex: 1,3) : ").strip()

    if ids_plateformes:
        for pid in ids_plateformes.split(","):
            pid = pid.strip()
            if pid:
                plateforme = session.query(Plateforme).get(int(pid))
                if plateforme:
                    nouveau_jeu.plateformes.append(plateforme)   # On ajoute via la relation Many-to-Many

    # === 6. Sauvegarde en base ===
    session.add(nouveau_jeu)
    session.commit()
    print(f"\n✅ Jeu '{titre}' créé avec succès ! (ID: {nouveau_jeu.jeu_id})")


def mettre_a_jour(session):
    """
    Fonction pour modifier un jeu existant.
    On affiche d'abord la liste, on demande l'ID, puis on propose de modifier les champs un par un.
    On met à jour directement les attributs de l'objet.
    """
    print("\n" + "=" * 50)
    print("MODIFICATION D'UN JEU")
    print("=" * 50)

    # On réutilise la fonction lire_jeux pour afficher la liste
    lire_jeux(session)

    jeu_id = int(input("\nID du jeu à modifier : ").strip())
    jeu = session.query(Jeu).get(jeu_id)

    if not jeu:
        print("❌ Jeu non trouvé !")
        return

    print(f"\nModification du jeu : {jeu.titre} (ID: {jeu.jeu_id})")
    print("(Appuie sur Entrée pour garder la valeur actuelle)")

    # === Modification des champs de base ===
    nouveau_titre = input(f"Nouveau titre [{jeu.titre}] : ").strip()
    if nouveau_titre:
        jeu.titre = nouveau_titre

    nouvelle_date = input(f"Nouvelle date de sortie [{jeu.date_sortie}] (AAAA-MM-JJ) : ").strip()
    if nouvelle_date:
        jeu.date_sortie = date.fromisoformat(nouvelle_date)

    nouveau_prix = input(f"Nouveau prix [{jeu.prix}] : ").strip()
    if nouveau_prix:
        jeu.prix = Decimal(nouveau_prix)

    # === Modification des détails (si le jeu en a) ===
    if jeu.details:
        print("\n--- Détails actuels ---")
        nouvelle_desc = input(f"Nouvelle description [{jeu.details.description}] : ").strip()
        if nouvelle_desc:
            jeu.details.description = nouvelle_desc

        nouvelle_note = input(f"Nouvelle note Metacritic [{jeu.details.note_metacritic}] : ").strip()
        if nouvelle_note:
            jeu.details.note_metacritic = int(nouvelle_note)

        nouveau_multi = input(f"Multijoueur ? (o/n) [{ 'o' if jeu.details.multijoueur else 'n' }] : ").strip().lower()
        if nouveau_multi in ["o", "n"]:
            jeu.details.multijoueur = (nouveau_multi == "o")

    # === Sauvegarde des modifications ===
    session.commit()
    print(f"\n✅ Jeu ID {jeu_id} mis à jour avec succès !")


def supprimer(session):
    """
    Fonction pour supprimer un jeu.
    On affiche la liste, on demande l'ID, on demande confirmation,
    puis on utilise session.delete() qui supprime aussi les détails et les liaisons
    grâce aux cascades qu'on a configurées dans les modèles.
    """
    print("\n" + "=" * 50)
    print("SUPPRESSION D'UN JEU")
    print("=" * 50)

    # On affiche la liste des jeux
    lire_jeux(session)

    jeu_id = int(input("\nID du jeu à supprimer : ").strip())
    jeu = session.query(Jeu).get(jeu_id)

    if not jeu:
        print("❌ Jeu non trouvé !")
        return

    # Demande de confirmation
    confirmation = input(f"\n⚠️  Tu es sûr de vouloir supprimer '{jeu.titre}' ? (o/n) : ").strip().lower()

    if confirmation == "o":
        # Suppression de l'objet (les détails et les liaisons Many-to-Many sont supprimés automatiquement grâce aux cascades)
        session.delete(jeu)
        session.commit()
        print(f"✅ Jeu '{jeu.titre}' (ID: {jeu_id}) supprimé avec succès !")
    else:
        print("Suppression annulée.")