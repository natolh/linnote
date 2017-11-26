# linnote

## Fonctionnalités

- [X] Mise en page automatique des rapports de classement
- [ ] Export PDF des rapports de classement
- [X] Statistiques descriptives des notes de l'épreuve
- [X] Graphique de distribution des notes de l'épreuve
- [X] Analyse en sous-groupes des notes de l'épreuve
- [X] Classement sur un aggrégat d'épreuves (interclassement)
- [X] Conversion des notes
- [ ] Post-traitement des notes de l'épreuve (uniquement lissage pour le moment)

## Pré-requis

Que vous soyez sur mac ou windows, `linnote` est une application en ligne de commande il faudra donc vous familiariser avec le `Terminal` ou l'`Invité de commandes` respectivement.

Afin d'utiliser `linnote`, il faut surtout maitriser la commande `cd`. Cette commande permet de se déplacer dans les différents dossiers de l'ordinateur. Pour l'utiliser il suffit d'exécuter `cd chemin/vers/lequel/vous/voulez/aller`.

## Installation

### macOS

1. Ouvrir l'application `Terminal`.

2. Installer [homebrew](https://brew.sh/index_fr.html) en suivant les instructions situées sur le site. Homebrew est un gestionnaire de paquets, il permet d'installer "proprement" des outils sur votre système.

3. Installer la dernière version de [python3](https://python.org) en exécutant la commande : `brew install python3` dans le `Terminal`. Python est un langage de programmation, c'est le langage dans lequel est écrit `linnote` votre ordinateur en aura donc besoin pour comprendre le programme et le faire fonctionner.

4. Télécharger la dernière version de [linnote](https://github.com/natolh/linnote/releases) depuis votre navigateur internet. Décompresser l'archive où vous souhaitez utiliser `linnote`. Il est possible de déplacer le dossier ultérieurement.

5. Dans le `Terminal` déplacer vous à l'aide de la commande `cd` vers le répertoire de `linnote`.

6. Installer les dépendances de `linnote` en exécutant la commande `sudo python3 -m pip install -r requirements.txt` dans le `Terminal`. Le `Terminal` va vous demander votre mot de passe pour débuter l'installation.

7. Patienter pendant l'installation...

8. Fin. Pour savoir comment utiliser `linnote`, lire le paragraphe "Utilisation".

### Windows

1. Télécharger depuis votre navigateur la dernière version de [python3](https://python.org/downloads) et installer la.

2. Ouvrir l'application `Invité de commandes` en mode Administrateur (clic droit et exécuter en tant qu'administrateur).

3. Télécharger la dernière version de [linnote](https://github.com/natolh/linnote/releases) depuis votre navigateur internet. Décompresser l'archive où vous souhaitez utiliser `linnote`. Il est possible de déplacer le dossier ultérieurement.

4. Dans l'`Invité de commandes` déplacer vous à l'aide de la commande `cd` vers le répertoire de `linnote`.

5. Installer les dépendances de `linnote` en exécutant en exécutant dans l'`Invité de commandes` la commande `py -m pip install -r requirements.txt`.

6. Patienter pendant l'installation...

7. Fin. Pour savoir comment utiliser `linnote`, lire le paragraphe "Utilisation".

## Mise à jour

L'installation des mises à jour n'est pas automatique.

### macOS

1. Télécharger le nouveau code de [linnote](https://github.com/natolh/linnote/releases) avec votre navigateur, décompresser l'archive et écraser l'ancien dossier.

2. Ouvrir l'application `Terminal`.

3. Dans le `Terminal` déplacer vous à l'aide de la commande `cd` vers le répertoire de `linnote`.

3. Mettre à jour les dépendances de `linnote` en exécutant la commande `sudo python3 -m pip install -r requirements.txt` dans le `Terminal`. Le `Terminal` va vous demander votre mot de passe pour débuter l'installation.

4. Patienter pendant l'installation...

5. Fin.

### Windows

1. Télécharger le nouveau code de [linnote](https://github.com/natolh/linnote/releases) avec votre navigateur, décompresser l'archive et écraser l'ancien dossier.

2. Ouvrir l'application `Invité de commandes` en mode Administrateur (clic droit et exécuter en tant qu'administrateur).

3. Dans l'`Invité de commandes` déplacer vous à l'aide de la commande `cd` vers le répertoire de `linnote`.

4. Mettre à jour les dépendances de `linnote` en exécutant dans l'`Invité de commandes` la commande `py -m pip install -r requirements.txt`.

5. Patienter pendant l'installation...

6. Fin.

## Utilisation

### Pré-requis

L'application dispose de trois dossiers que vous devez connaître : `groups`, `rankings`, `results`.

Le dossier `groups` doit contenir les groupes d'étudiants que vous ne souhaitez classer distinctement même s'ils participent à la même épreuve. Pour créer un groupe, déposer dans le dossier `groups` un fichier Excel au format `xlsx` contenant dans la première colonne de la première feuille la liste des identifiants des étudiants du groupe. Le nom du groupe sera équivalent au nom du fichier Excel. Vous pouvez créer plusieurs groupes.

Le dossier `rankings` contiendra les rapports de classement créé par l'application.

Le dossier `results` doit contenir les résultats de la (ou des) épreuve(s) que vous souhaitez analyser. Un fichier de résultat est un fichier Excel au format `xlsx` contenant dans la première colonne les identifiants des étudiants ayant participé à l'épreuve et dans la deuxième colonne les notes des étudiants ayant participé à l'épreuve.

### macOS

1. Ouvrir l'application `Terminal`.

2. Dans le `Terminal` déplacer vous à l'aide de la commande `cd` vers le répertoire de `linnote`.

3. Dans le `Terminal` exécuter la commande `python3 -m linnote` pour démarrer l'application.

4. Suivre les instructions.

5. Fin.

### Windows

1. Ouvrir l'application `Invité de commandes`.

2. Dans l'`Invité de commandes` déplacer vous à l'aide de la commande `cd` vers le répertoire de `linnote`.

2. Dans l'`Invité de commandes` exécuter la commande `py -m linnote` pour démarrer l'application.

3. Suivre les instructions.

4. Fin.
