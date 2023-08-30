import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
import umap

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# pourquoi t-SNE n'a pas de .transform :
# https://stackoverflow.com/questions/59214232/python-tsne-transform-does-not-exist


def reduce_tf_idf_dimensions(tf_idf_matrix, test_set=None, dimension=2, random_state=42):
    """
    Function that reduce the dimension of tf-idf matrix
    :param tf_idf_matrix: embeddings
    :param test_set: test embeddings if available
    :param dimension: number of dimensions
    :param random_state: random seed
    :return: a dictionary with the embeddings after reducing the dimensions
    """

    svd = TruncatedSVD(n_components=dimension, random_state=random_state)
    umap_ = umap.UMAP(n_components=dimension, n_epochs=100, n_neighbors=25, random_state=random_state)
    if dimension < 4:
        tsne = TSNE(n_components=dimension, random_state=random_state)
    else:
        tsne = TSNE(n_components=dimension, method="exact", random_state=random_state)

    if test_set is not None:
        # SVD
        embeddings_train = svd.fit_transform(tf_idf_matrix)
        embeddings_train = scaler.fit_transform(embeddings_train)

        embeddings_test = svd.transform(test_set)
        embeddings_test = scaler.transform(embeddings_test)

        print(f"embeddings train shape: {embeddings_train.shape}\t test shape: {embeddings_test.shape}")
        print(f"embeddings train and test type: {type(embeddings_train)}")

        # t-SNE
        embeddings = np.concatenate((embeddings_train, embeddings_test), axis=0)
        embeddings_tsne = tsne.fit_transform(embeddings)
        embeddings_tsne = scaler.fit_transform(embeddings_tsne)

        embeddings_tsne_train = embeddings_tsne[:embeddings_train.shape[0]]
        embeddings_tsne_test = embeddings_tsne[embeddings_train.shape[0]:]

        # UMAP
        embeddings_umap_train = umap_.fit_transform(embeddings_train)
        embeddings_umap_train = scaler.fit_transform(embeddings_umap_train)

        embeddings_umap_test = umap_.transform(embeddings_test)
        embeddings_umap_test = scaler.transform(embeddings_umap_test)

        return {"SVD": (embeddings_train, embeddings_test),
                "t-SNE": (embeddings_tsne_train, embeddings_tsne_test),
                "UMAP": (embeddings_umap_train, embeddings_umap_test)}

    else:
        # SVD
        embeddings = svd.fit_transform(tf_idf_matrix)
        embeddings = scaler.fit_transform(embeddings)

        print(f"embeddings shape: {embeddings.shape}")
        print(f"embeddings type: {type(embeddings)}")

        # t-SNE
        embeddings_tsne = tsne.fit_transform(embeddings)
        embeddings_tsne = scaler.fit_transform(embeddings_tsne)

        # UMAP
        embeddings_umap = umap_.fit_transform(embeddings)
        embeddings_umap = scaler.fit_transform(embeddings_umap)

        return {"SVD": embeddings,
                "t-SNE": embeddings_tsne,
                "UMAP": embeddings_umap}
