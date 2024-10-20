# TP-Flask
complété par Clermont Shanka et Richard Baptiste

## Lancement Flask
- se placer dans le répertoire principal
- instaurer la base de donnée avec : flask loaddb ./data.yml    (ou d'autre modèle de donnée compatible)
- pour créer un utilisateur : flask newuser _username_ _motdepasse_
- maintenant que les bases sont prête vous pouvez lancer le site avec : flask run

## Commandes Flask
- loaddb _cheminversdata_  ->  charge la base de donnée
- newuser _username_ _motdepasse_  ->  crée un utilisateur avec un mot de passe
- passwd _username_ _motdepasse_  ->  change le mot de passe de l'utilisateur indiqué
- syncdb  ->  met à jour la base de donnée
- newgenre _nomgenre_  -> crée un genre de livre
- ajoutgenretolivre _nomgenre_ _islivre_  ->  ajoute un livre à un genre

## Navigation sur le site
Pour se connecter/deco :
- Aller sur le bouton login
- Rentrer ses identifiants
- Pour se déconnecter, cliquer sur le "bouton de sortie" à gauche de la barre de navigation

Pour rechercher un livre :
- la barre de recherche permet une recherche par nom de livre
- la page "recherche avancée" permet de faire une recherche par auteur, nom livre avec un prix max

Favori :
- Vous pouvez ajouter un favori ou le supprimer sur la page d'un livre avec le bouton en coeur
- Puis vous pouvez regarder vos favori sur la page vos favori

Modifications :
- Possibilité de crée/modifier/supprimer un auteur
- Possibilité de modifier/supprimer un livre
