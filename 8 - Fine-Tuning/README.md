# Fine-Tuning

Dans cette étape cruciale, nous affinons les performances de nos algorithmes de classification grâce au fine-tuning. Pour faciliter cette tâche, nous avons créé un fichier `FineTunedAlgos.py` contenant des fonctions spécifiques pour chaque algorithme.

L'utilisation de ces fonctions est simple et efficace :

```python
import FineTunedAlgos

# --- Fine-Tuning Classification Algorithms
best_score_rf, best_params_rf = FineTunedAlgos.fine_tune_algo(X_train, y_train, X_test, y_test, algo="RandomForest")
best_score_svc, best_params_svc = FineTunedAlgos.fine_tune_algo(X_train, y_train, X_test, y_test, algo="SVC")
best_score_knn, best_params_knn = FineTunedAlgos.fine_tune_algo(X_train, y_train, X_test, y_test, algo="KNeighbors")
best_score_gdb, best_params_gdb = FineTunedAlgos.fine_tune_algo(X_train, y_train, X_test, y_test, algo="GradientBoosting")
best_score_mlp, best_params_mlp = FineTunedAlgos.fine_tune_algo(X_train, y_train, X_test, y_test, algo="MLPClassifier")
```

Une fois que nous avons affiné les performances individuelles de chaque algorithme, nous les agrégeons dans un Voting Classifier. Cet ensemble d'algorithmes constitue un mécanisme puissant pour améliorer la précision de nos prédictions finales.

```python
# --- Voting Classifier
voting_clf = FineTunedAlgos.VotingClassifier(
    estimators=[('rf', FineTunedAlgos.RandomForestClassifier(**best_params_rf)),
                ('svc', FineTunedAlgos.SVC(**best_params_svc)),
                ('knn', FineTunedAlgos.KNeighborsClassifier(**best_params_knn)),
                ('mlp', FineTunedAlgos.MLPClassifier(**best_params_mlp)),
                ('gdb', FineTunedAlgos.GradientBoostingClassifier(**best_params_gdb))]
)

voting_clf.voting = "soft"
voting_clf.named_estimators["svc"].probability = True

voting_clf.fit(X_train, y_train)
voting_clf.predict_proba(X_test)

print("Voting Classifier score on test data :", round(voting_clf.score(X_test, y_test), 5))
print("Voting classifiers estimators :", voting_clf.estimators_)
```

- Output obtenu : 
```
Voting Classifier score on test data : 0.97024
Voting classifiers estimators : [RandomForestClassifier(max_depth=20, min_samples_leaf=6, n_estimators=82), KNeighborsClassifier(n_neighbors=4, weights='distance'), MLPClassifier(alpha=0.0166356999699944, hidden_layer_sizes=(64,)), GradientBoostingClassifier(learning_rate=0.09107090914992075, max_depth=17,
                           min_samples_leaf=12, n_estimators=102,
                           subsample=0.3571111033662477)]
F1 score Stratified K-Fold CV : 96.26462 %
```