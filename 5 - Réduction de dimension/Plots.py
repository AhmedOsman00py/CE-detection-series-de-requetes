from sklearn import preprocessing
import plotly.graph_objects as go

label_encoder = preprocessing.LabelEncoder()


def plot_embeddings(fig, embeddings, name, dataframe, color="N° Série", row=-1, col=-1):
    """
    function to plot the embeddings with plotly
    :param fig: figure object
    :param embeddings: embeddings 2D
    :param name: name of the plot
    :param dataframe: data
    :param color: color of the data points
    :param row: row index in the subplot
    :param col: column index in the subplot
    :return: figure object
    """

    # color = pd.factorize(dataframe[color])[0]
    color = label_encoder.fit_transform(dataframe[color])
    dataframe["color"] = color
    color_list = dataframe.color.apply(lambda x: x if x != -1 else "grey")

    go_scatter_kwargs = {
        "x": embeddings[:, 0],
        "y": embeddings[:, 1],
        "mode": "markers",
        "name": name,
        "marker": dict(color=color_list),
        "hovertext": [f"<b>N° Dossier : {row['file_id']}<br>"
                      f"TA : {row['TA']}<br>"
                      f"N° Série : {row['N° Série']}<br>"
                      f"Nom Série: {row['Nom serie']}<br><br></b>"
                      f"Matière dossier: {row['Matiere dossier']}<br>"
                      f"Tête de série : {row['Tete de serie']}<br>"
                      f"Nombre de pages : {row['number_of_pages']}<br>"
                      f"code couleur : {row['color']}" for i, row in dataframe.iterrows()]
    }

    # Plot in 2D
    if embeddings.shape[1] == 2:

        if row == -1 and col == -1:
            return fig.add_trace(
                go.Scatter(**go_scatter_kwargs),
                row=1, col=1
            )
        else:
            return fig.add_trace(
                go.Scatter(**go_scatter_kwargs),
                row=row, col=col
            )
    # Plot in 3D
    else:
        go_scatter_kwargs["marker"] = dict(color=color_list, size=7, opacity=0.8)
        return go.Figure(go.Scatter3d(z=embeddings[:, 2], **go_scatter_kwargs))

        # fig.write_html(f"results_juradinfo/3Dembbeddings.html")


def plot_test_embeddings(fig, embeddings, name, dataframe, y_test_pred=None, row=-1, col=-1):
    """
        function to plot the testing embeddings set with plotly
        https://stackoverflow.com/questions/31720527/convert-categorial-variables-into-integers-using-pandas
        :param fig: figure object
        :param embeddings: embeddings 2D
        :param name: name of the plot
        :param dataframe: data
        :param y_test_pred: y_test or y_pred to get the labels and the same colors
        :param row: row index in the subplot
        :param col: column index in the subplot
        :return: figure object
        """
    if y_test_pred:
        color_list = label_encoder.transform(y_test_pred[:, 0])
    else:
        color_list = ["grey"] * dataframe.shape[0]

    return fig.add_trace(
        go.Scatter(x=embeddings[:, 0], y=embeddings[:, 1],
                   mode="markers", name=name,
                   marker=dict(color=color_list),
                   hovertext=[f"<b>N° Dossier : {row['file_id']}<br>"
                              f"TA : {row['TA']}<br>"
                              # f"N° Série : {row['N° Série']}<br>"
                              # f"Nom Série: {row['Nom serie']}<br><br></b>"
                              # f"Matière dossier: {row['Matiere dossier']}<br>"
                              # f"Tête de série : {row['Tete de serie']}<br>"
                              f"Nombre de pages : {row['number_of_pages']}<br>"
                              # f"code couleur : {row['color'] if row['color'] != -1 else 'grey'}"
                              for i, row in dataframe.iterrows()]),
        row=row, col=col
    )
