# 6 - Stratégie de division des données

Nous utilisons [StratifiedShuffleSplit de Scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html).

La stratégie de division des données `StratifiedShuffleSplit` est une technique de validation croisée qui vise à préserver la répartition des classes dans les ensembles d'entraînement et de test. Concrètement, elle garantit que la proportion de chaque classe reste constante dans les deux ensembles, ce qui est particulièrement important lorsque les classes sont déséquilibrées.

L'algorithme fonctionne en mélangeant les données de manière aléatoire, puis en divisant l'ensemble en train et test tout en maintenant les proportions des classes.
