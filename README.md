CHESS MANAGER

Installation

1. Importez dans un dossier le programme depuis github

2. Créez un environnement virtuel:
    - virtualenv doit être insallé sur votre pc, si ce n'est pas le cas, installez-le:
        ouvrez une console et tapez:
            pip install virtualenv
    - créez un environnement virtuel
        onvrez une console à la racine du programme (le dossier qui contient le fichier requirements.txt)
        que vous venez d'importer, et tapez:
            python3 -m venv env

3. Activez l'environnement virtuel
    toujours dans une console à la racine du programme , tapez:
        source env/bin/activate

    remarque: pour quitter l'environnement virtuel, tapez simplement en console:
        deactivate

4. Importez les dépendances:
    avec l'environnement virtuel activé, à la racine du programme tapez:
        pip install -r requirements.txt

5. Lancez le programme
    Maintenant que votre environnemnt virtuel est activé et que les dépendances sont chargées, vous pouvez lancer
    le programme avec la commande:
        ./chess_manager.py

____________________________________________________________________________________________________________________

Raports Flake8-html (avec l'environnement virtuel activé):

Pour vérifier la conformité du code avec la PEP8, tapez dans le répertoire racine:

flake8 --format=html --htmldir=flake-report prg

Un rapport au format html sera généré dans un dossier "flake-report" à la racine du projet.


Vous pouvez vérifier également le lanceur de la même façon, en entrant en console:

flake8 --format=html --htmldir=flake-report chess_manager.py

