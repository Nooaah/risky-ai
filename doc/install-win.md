# Installation

- First get: Visual-Studio-code
  - module: python, c++, cmake-tools
- git-scm, cmake (with PATH modification), python3 (with PATH modification)
- MinGW (with Developper-toolkit, base-bin, gcc-g++ et msys-base-bin) > install > apply-chances et ajouter MinGW/bin dans le PATH...

redémarer la machine.

Puis dans le powershell de VSCode:

```sh
cd hackagames
cmake -G "MinGW Makefiles"
mingw32-make
```

Bon est la ça marche pas, problémes de dépendances sur la gestion du réseau. A voir avec Mosquitto si on peut pallier le probléme...




Old:


### Dépendance sous Window - Non recommandé:


**Configuration de MinGW**

1. Télécharger Minimalist GNU for Windows GCC tools' set ([MinGW](http://www.mingw.org/)) à partir de la page de [setup UI](https://osdn.net/projects/mingw/downloads/68260/mingw-get-setup.exe/) program.
2. Lancer l'exécutable, et sélectionner/laisser le dossier d'installation comme étant votre racine système (C:).
3. Une fois l'installation terminée, une nouvelle fenêtre s'ouvre (MinGW Installation Manager)
4. Repérez les packets ci-dessous, et pour chacun d'eux, faites un clic droit > `Mark for installation` :
```c
mingw-developer-toolkit-bin //(d'autres packages seront alors automatiquement sélectionnés)
mingw32-base-bin
mingw32-gcc-g++-bin
```
5. Ensuite, dans la barre de menu, faire : `Installation > Apply Changes > Apply`. Le manager installera automatiquement les packages sélectionnés précédemment.
6. Une fois les packages installés, **AJOUTER** sur une nouvelle ligne `C:\MinGW\bin` dans votre variable d'environnement **PATH**. Pour ce faire : `panneau de conifg. > système et securite > système > param. système avancé > variable d'env. > PATH > Modifier`. Cette variable regroupe l'ensemble des chemins absolus pour accéder aux ressources indiquées.

**Configuration de GIT**

Installer [Git for Windows](https://gitforwindows.org/). On utilisera notamment son invite de commande `git-bash` comme terminal.

**Configuration de Raylib**

Installer Raylib en version 3.0.0 sous Windows [[cf. raylib-wiki](https://github.com/raysan5/raylib)] en passant par la [release](https://github.com/raysan5/raylib/releases) pour MinGW :


1. Télécharger la version 3.0.0 de RayLib pour [Win32 mingw](https://github.com/raysan5/raylib/releases/download/3.0.0/raylib-3.0.0-Win32-mingw.zip) (même sur une machine 64bit).
2. Extraire et déplacer le contenu des repertoires `bin`, `include` et `lib` respectivement dans les répertoires `bin`, `include` et `lib` se trouvant dans `C:\MinGW` (Attention ! Ne pas remplacer les dossiers)
3. Copier `C:\MinGW\bin\libraylib.dll` dans `C:\MinGW\bin\`, et renommer la copie `raylib.dll`. 
4. Dans un terminal *git-bash* (pour l'ouvrir `Menu Démarrer > Git Bash`), taper la commande suivante :


```bash
cp C:/MinGW/bin/libraylib.dll C:/MinGW/bin/raylib.dll
```


(On aura aussi besoin du programme *make* qui permet d'automatiser le processus de construction d'un projet. Il est déjà installé, mais sous le nom de '*C:\MinGW\bin\mingw32-make.exe*')


5. Dans un terminal *git-bash* :


```bash
cp C:/MinGW/bin/mingw32-make.exe C:/MinGW/bin/make.exe
```

6. Rebooter la machine (pour notamment prendre en charge le nouveau *PATH*).


Ouf...


## Teste de l'installation


1. Récupérer l'[exemple](https://www.raylib.com/examples.html) basic de Raylib (le 1er encart) : copier le code dans un fichier `main-basic.c` sur votre machine.
2. Ouvrir votre terminal, et vous placer dans votre dossier de travail. Par exemple :
```bash
cd C:/Users/me/Documents #Windows
# OU
cd /home/me/Documents #Linux
```
3. Compiler à partir de votre terminal l'exemple :

```bash
gcc -o basic-raylib PATH/TO/main-basic.c -std=c99 -Wall -Wextra -lraylib
```

4. Un exécutable est normalement généré. Lancez le pour vous assurez que tout fonctionne bien.

```bash
./basic-raylib.exe
```


## Compiler NetWorld


Il n'y a plus qu'à cloner et compiler NetWorld :


```bash
git clone http://gvipers.imt-lille-douai.fr/fatus/networld.git NetWorld
cd NetWorld
make
```


Des exécutables sont générés au format *nw-xxxx*. Vous verrez également apparaître quelques *warnings* : n'en tenez pas compte.

Et voilà !

## Organisation du répertoire


Répertoire:


- *bin* : stocke de scripts pour automatiser des procédures utiles au projet.
- *.git* : répertoire de gestion de version propre à git.
- *src* : le code source du projet.
- *doc* : la documentation du projet.


Fichier à la racine:


- *.gitignore* : fichier de configuration git listant les ressources à ne pas versionner.
- *config* : Fichier de configuration pour le make (cf. *src/Makefile*).
- *config.default* : Fichier *config* utilisé à défaut (cf. *Makefile*).
- *Makefile* : Instruction de construction du projet pour *make*. Génère *config* et fait appel à *src/Makefile*.
- *projet-outline.md* : Un descriptif des composants logiciel réalisé et prévu.
- *nw-xxxx* : Les exécutables de NetWorld.
- *README,md* : Votre serviteur.

## Idée de jeux induits:

## Optimisation de routage dynamique (Pb. réseau)


Générer des robots et les déplacer pour couvrir au mieux un réseau.


- être résiliant aux pannes
- Réseau en constance augmentation
- Circonscrire les Zones défectueuses....


## WarBot


Des équipes de robots cherchent à s'entre-tuer.


## OpenDrive


Course de véhicule en environnement ouvert et dynamique. (Avec des aspects de dynamique des véhicules quasiment absents, mais la nécessité de prendre en compte aux mieux les autres véhicules pour optimiser sont choix de chemins).

## ...