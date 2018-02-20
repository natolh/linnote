# linnote

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c9d4a74280bb4613963a53bfe1b80576)](https://www.codacy.com/app/natolh/linnote?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=natolh/linnote&amp;utm_campaign=Badge_Grade)

# Introduction

`linnote` est une application web pour gérer des notes et réaliser des classements d'épreuves. Elle a été développé pour le Tutorat Santé Lyon Sud afin de faciliter la création des classements aux épreuves blanches organisées pour les étudiants préparant le concours de la PACES.

L'application est utilisée en production depuis 2016 au sein du Tutorat Santé Lyon Sud. Jusqu'en novembre 2017 elle était disponible uniquement sour la forme d'un client en ligne de commande rendant son usage difficile et elle n'était pas mise en ligne. Depuis la version 1.5.0 il s'agit d'une application web et elle est disponible librement sur GitHub.

Le périmètre fonctionnel est restreint pour le moment, mais permet déjà une utilisation en production (au sein du Tutorat Santé Lyon Sud).
- Import de fichiers de notes (Excel pour le moment) avec possibilité de recalculer les notes sur un autre barème.
- Post-traitement des notes (modification des notes autre que le changement de barème). Impossible d'activer / désactiver la fonction, une seule méthode disponible (lissage), méthode appliquée à l'ensemble des participants de l'épreuve.
- Analyse univariée des notes et graphique de répartition des notes. Impossible d'activer / désactiver la fonction, paramètres statistiques calculés non modifiables (taille d'échantillon, maximale, minimale, médiane, moyenne), analyse en sous-groupe possible.
- Classement des étudiants. Impossible d'activer / désactiver la fonction, une seule méthode disponible, analyse en sous-groupe possible.

## Côté technique

Il s'agit d'une application web développée en [Python3](https://python.org) à l'aide du framework [Flask](http://flask.pocoo.org/).

Plusieurs dépendances sont utilisées pour faire tourner l'application.
- [SQLAlchemy](http://www.sqlalchemy.org/) : liaison à la base de données
- [alembic](http://alembic.zzzcomputing.com/en/latest/) : migrations de schéma de la base de données
- [pandas](https://pandas.pydata.org/) avec [xlrd](https://github.com/python-excel/xlrd) : import et manipulation des fichiers de tableurs
- [matplotlib](https://matplotlib.org/) : réalisation de graphiques
- [flask-login](https://flask-login.readthedocs.io/en/latest/) : gestion de l'authentification
- [flask-wtf](https://flask-wtf.readthedocs.io/en/stable/) : écriture des formulaires HTML.

## Côté développement

Le code a été principalement écrit sous [VSCode](https://code.visualstudio.com/) avec l'extension pour Python et [PyLint](https://www.pylint.org/) pour vérifier la qualité du code produit.


# Utilisation
À venir...

# Installation

À venir...
