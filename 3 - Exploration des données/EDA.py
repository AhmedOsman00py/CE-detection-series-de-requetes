import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


data = pd.read_csv("data_labeled.csv", sep=";")

series = data.groupby(["N° Série"], as_index=False).size()
series = series[series["size"] >= 30]
series.columns = ["N° Série", "Nombre de requêtes"]

data = data[data["N° Série"].isin(series["N° Série"].values)]
data.reset_index(drop=True, inplace=True)

# --- Répartition des classes
fig = px.bar(series, x="N° Série", y="Nombre de requêtes",
              text_auto=".s",
              title="Répartition des classes existantes", color='Nombre de requêtes', template="plotly_white")
fig.update_coloraxes(showscale=False)
fig.show()
fig.write_html("rep_classes.html")

# --- Répartition des requêtes selon leurs dates d'enregistrement
date_df = data.copy()
date_df["Date enregistrement"] = date_df["Date enregistrement"].str.split("-", expand=True)[0]
date_df = date_df.groupby(["Date enregistrement"], as_index=False).size()
date_df.columns = ["Date enregistrement", "Nombre de requêtes"]

fig_date = px.bar(date_df, x="Nombre de requêtes", y="Date enregistrement",
                  color="Date enregistrement", template="plotly_dark",
                  color_discrete_sequence=["#7A4C74", "#7A4C74", "#7A4C74"],
                  title="Nombre de requêtes par date d'enregistrement")
fig_date.update_layout(showlegend=False)
fig_date.show()

# --- Répartition des requêtes selon leurs nombres de pages
sns.set_theme(style="darkgrid")
fig_req, ax = plt.subplots(figsize=(20, 10))

barcharts = data.groupby('number_of_pages').count()
barcharts = pd.DataFrame({"number_of_pages": barcharts.index, "count": barcharts.file_name})
sns.barplot(barcharts, x="number_of_pages", y="count")
fig_req.show()
