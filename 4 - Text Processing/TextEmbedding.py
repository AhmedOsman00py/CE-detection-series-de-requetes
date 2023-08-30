from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()


def get_tf_idf(data, text_column_name="text", test_set=None):
    """
    TF-IDF Matrix
    :param text_column_name: name of the column that contains the text in the dataframe
    :param data: all data or training data if test_set is given
    :param test_set: test dataframe if available
    :return: tf-idf matrix
    """

    tf_idf_train = vectorizer.fit_transform(data[text_column_name].values)

    if test_set is not None:
        # documents = data['text'].to_list()
        print(f"Training set shape : {tf_idf_train.shape}")

        tf_idf_test = vectorizer.transform(test_set[text_column_name].values)
        print(f"Validation set shape : {tf_idf_test.shape}\n")

        return {"train_set": tf_idf_train, "test_set": tf_idf_test}

    else:
        # in this case tf_idf_train is the tf_idf of all the dataset
        return tf_idf_train
