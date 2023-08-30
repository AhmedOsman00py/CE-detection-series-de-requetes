# 9 - Évaluation des performances avec différentes dimensions d'embeddings

Après avoir abouti à notre modèle final, optimisé grâce au processus de fine-tuning, qui a été entraîné en utilisant les embeddings TF-IDF avec un nombre spécifique de dimensions, nous avons élargi notre analyse en variant la dimensionnalité des embeddings.

Nous avons ainsi obtenu les résultats suivants en utilisant les embeddings générés par les algorithmes t-SNE :

<img src="img/tsne scores.png" width="60%" height="60%">

Dans la ligne 5, sous la colonne "dimension", l'individu "16_sansSVC" signifie que nous avons exclu l'algorithme SVC de notre Voting Classifier pour observer toute variation de performances. Dans le cas spécifique de t-SNE, nous constatons que le F1-score n'a pas été affecté par cette exclusion.

Si le score est affiché en rouge, cela indique qu'il représente la valeur maximale de la colonne. En revanche, si une ligne est entièrement colorée en vert, cela signifie que la combinaison de ces algorithmes dans notre Voting Classifier a produit le meilleur F1-score parmi toutes les autres configurations testées. Dans notre cas, le score du Voting Classifier représente notre F1-score final.

<img src="img/tsne graph.png" width="60%" height="60%">

De même, en utilisant les embeddings générés par l'algorithme UMAP, nous avons obtenu les résultats suivants :

<img src="img/umap scores.png" width="60%" height="60%">

Dans le cas d'UMAP, une observation importante est que lorsque nous avons retiré le SVC du Voting Classifier pour le troisième individu, noté "8_sansSVC", le F1-score du Voting Classifier a montré une diminution par rapport à la configuration où le SVC était inclus, comme le montre la ligne précédente.

<img src="img/umap graph.png" width="60%" height="60%">

Malgré les performances légèrement supérieures obtenues avec l'algorithme t-SNE par rapport à UMAP, nous avons choisi d'opter pour UMAP en raison de sa vitesse de traitement nettement plus élevée. t-SNE peut être extrêmement lent, surtout lorsque les dimensions sont élevées, contrairement à UMAP. Bien que la différence de performance ne soit pas significativement grande entre les deux, la rapidité de traitement d'UMAP s'est avérée être un facteur déterminant dans notre choix.