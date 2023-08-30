import optuna
from functools import partial

from sklearn.metrics import accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier


def objective(trial: optuna.Trial, X_train, y_train, X_test, y_test, algo="all") -> float:
    if algo == "all":
        clf_name = trial.suggest_categorical("classifier",
                                             ["RandomForest", "SVC", "KNeighbors", "AdaBoost",
                                              "GradientBoosting", "MLPClassifier"])
    else:
        clf_name = algo
        assert algo in ["RandomForest", "SVC", "KNeighbors", "AdaBoost", "GradientBoosting", "MLPClassifier"], \
            print(f'Error : {algo} is not recognized, maybe try these algorithms :\n'
                  f'["RandomForest", "SVC", "KNeighbors", "AdaBoost", "GradientBoosting", "MLPClassifier"]')

    if clf_name == "RandomForest":
        rf_kwargs = {
            "n_estimators": trial.suggest_int("n_estimators", 80, 120),
            "max_depth": trial.suggest_int("max_depth", 5, 20),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 5, 15),
            "bootstrap": True,
            "n_jobs": -1
        }
        clf = RandomForestClassifier(**rf_kwargs)

    elif clf_name == "GradientBoosting":
        gdb_kwargs = {
            "n_estimators": trial.suggest_int("n_estimators", 90, 140),
            # "learning_rate": trial.suggest_float("learning_rate", 0.0001, 0.2),
            "learning_rate": trial.suggest_float("learning_rate", 0.0001, 0.2, log=True),
            "subsample": trial.suggest_float("subsample", 0.01, 1, log=True),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 5, 15),
            "max_depth": trial.suggest_int("max_depth", 5, 20)
        }
        clf = GradientBoostingClassifier(**gdb_kwargs)

    elif clf_name == "SVC":
        # transformer le SVC en predict proba pour avoir un VotingClassifier "Soft"
        svc_kwargs = {
            "C": trial.suggest_float("C", 0.01, 100, log=True),
            "kernel": trial.suggest_categorical("kernel", ["rbf", "linear", "sigmoid", "poly"]),
            "gamma": trial.suggest_categorical("gamma", ["auto", "scale"]),
            # "probability": True
        }
        clf = SVC(**svc_kwargs)

    elif clf_name == "KNeighbors":
        knn_kwargs = {
            "n_neighbors": trial.suggest_int("n_neighbors", 1, 10),
            "weights": trial.suggest_categorical("weights", ["uniform", "distance"]),
            "n_jobs": -1
        }
        clf = KNeighborsClassifier(**knn_kwargs)

    elif clf_name == "AdaBoost":
        ada_kwargs = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 200),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1, log=True),
            "algorithm": "SAMME.R"
        }
        clf = AdaBoostClassifier(**ada_kwargs)

    else:  # MLP Classifier
        mlp_kwargs = {
            "hidden_layer_sizes": trial.suggest_categorical("hidden_layer_sizes", [(64,), (128,), (32, 64), (64, 128)]),
            "activation": trial.suggest_categorical("activation", ["relu", "logistic", "tanh"]),
            "alpha": trial.suggest_float("alpha", 1e-5, 0.1, log=True)
        }
        clf = MLPClassifier(**mlp_kwargs)

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # score = accuracy_score(y_test, y_pred)
    score = f1_score(y_test, y_pred, average="weighted")

    return score


def fine_tune_algo(X_train, y_train, X_test, y_test, algo="all", n_trials=50):
    objective_partial = partial(objective, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, algo=algo)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective_partial, n_trials=n_trials, n_jobs=-1, show_progress_bar=True)

    best_params = study.best_params
    best_score = study.best_value

    print("===================================================")
    print(f"Best score for {algo} : {best_score}")
    print(f"Best params for {algo} : {best_params}\n")
    print("===================================================")

    return best_score, best_params
