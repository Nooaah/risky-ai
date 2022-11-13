# Risky Game (Team Blue)

![](resources/blue_logo.png)

### 🔵 The Team Blue

- Development of the Q-learning AI:
  * **Pierre Calon** - ([Github](https://github.com/PierreCalon))
    - Q-Learning Lead Developer
  * **Noah Châtelain** - ([Github](https://github.com/Nooaah))
    - Secondary Q-Learning Developer
    - Git Master
- Development of the Monte-Carlo and optimization:
  * **Tom Maillard** - ([Github](https://github.com/wipcamael))
    - Monte-Carlo Lead Developer
  * **Marvin Bonnet** - ([Github](https://github.com/AastroLePetitRobot))
    - Secondary Monte-Carlo Developer
#### Contributors

- Permanent contributor:
  * **Guillaume LOZENGUEZ** - [guillaume.lozenguez@imt-nord-europe.fr](mailto:guillaume.lozenguez@imt-nord-europe.fr)

### Quelques explications de notre projet
___
#### Première version

Notre première version du Risky était basée sur un Q-Learning.
- Dernière version disponible au commit [6e91f01](https://github.com/Nooaah/risky-ai/tree/6e91f01a3da53ff941a874350bd369a5c05ae89b)

Nous avons décidé de remplir le JSON de notre Q-Learning avec tout l'état du board actuel, afin de pouvoir jouer des millions d'entraînements par la suite, et d'avoir un Q-Learning très performant. Mais le nombre d'états possibles était beaucoup trop grand, et le temps d'entraînement de notre Q-Learning aurait été beaucoup trop long. Nous avons donc décidé par la suite de réduire les nos différents états, afin de réduire la taille de notre JSON.

#### Ajout d'un algorithme de Monte-Carlo

Nous avons ensuite décidé de créer un Monte-Carlo, qui se chargera par la suite d'insérer des valeurs correctes dans le JSON de notre Q-Learning.
- Dernière version du MCTS disponible sur la branche [mcts-latest](https://github.com/Nooaah/risky-ai/tree/mcts-latest)

#### Résultats

Les résultats de notre Monte-Carlo n'étant pas les résultats attendus, le temps des entraînements étaient beaucoup trop longs (Environ 5 secondes par parties) et il était donc quasiement impossible de remplir le JSON de notre Q-Learning, car les valeurs de nos différents états réapparaissent très rarement, voire jamais.

#### Dernier recours

Notre projet, avec nos algorithmes de Q-Learning et de Monte-Carlo, étant tous deux fonctionnels, mais n'apportant pas de résultats assez satisfaisants lors du dernier jour du projet, nous avons donc décidé de réaliser notre propre algorithme de dernière minute, qui suit notre propre stratégie de jeu, afin d'avoir au moins une IA fonctionnelle, pouvant battre l'IA random, l'IA prof, et quelques IA des autres teams.
- Dernière version du projet sur la branche [main](https://github.com/Nooaah/risky-ai/tree/main)
