import os
import re

import numpy as np
import pandas as pd

import PreprocessingOptimized

# --- métadonnées
df = pd.read_excel("data/juradinfo_TA.xlsx", usecols=range(0, 8))

df["TA"] = df["TA"].str.strip()
df["N° Série"] = df["N° Série"].str.strip()
df["Nom serie"] = df["Nom serie"].str.strip()
df["Matiere dossier"] = df["Matiere dossier"].str.strip()
df["Titre"] = df["Titre"].str.strip()
df["Tete de serie"] = df["Tete de serie"].map({'                 ': "NA", 0: "0", 1: "1"})
df["file_id_TA"] = df.apply(lambda row: str(row["N° Dossier"]) + "_" + str(row["TA"]), axis=1)

# --- données
txt_folder = r"data/requetes_txt"
img_folder = r"data/requetes_img"


def get_data_as_df(txt_folder_path, img_folder_path):

    files = os.listdir(txt_folder_path)

    files_name = []
    files_text = []
    num_of_pages = []
    for file in files:
        files_name.append(os.path.splitext(file)[0])
        num_of_pages.append(len(os.listdir(f"{img_folder_path}/{file[:-4]}")))
        with open(f"{txt_folder_path}/{file}", "r", encoding="utf-8") as file_text:
            text = file_text.read()
            files_text.append(text)
        print(file, "done")

    return pd.DataFrame({"file_id": range(1, len(files_name)+1),
                         "file_name": files_name, "number_of_pages": num_of_pages, "text": files_text})


data = get_data_as_df(txt_folder, img_folder)

# --- fichier nomenclature TA
nomenclature = pd.read_excel("data/Nomenclature_decision.xlsx",
                             header=1, usecols=(4, 5), names=["Num_TA", "Nom_TA"])


def find_TA(string):
    string_list = string.split("_")
    if string_list[0][0] == "T" and len(string_list[0]) > 1:
        # print(string_list[0])
        try:
            nom_TA = nomenclature[nomenclature.Num_TA == int(string_list[0][1:])]["Nom_TA"].item().upper()
        except ValueError:
            nom_TA = string_list[0]
        return nom_TA
    elif "TA" in string_list:
        string_array = np.array(string_list)
        return string_array[np.argmax(string_array == "TA") + 1]
    else:
        print("TA not found in", string)
        return None


def find_id(string):
    file_id = re.findall(r'\d+', string)
    for id in file_id:
        if len(str(id)) == 7:
            return id
    return file_id


data["file_id"] = data.file_name.apply(find_id)
data["TA"] = data.file_name.apply(find_TA)
data = data[data.file_id.apply(lambda x: type(x) == str)]
data.file_id = data.file_id.astype("int")
data["file_id_TA"] = data.apply(lambda row: str(row["file_id"]) + "_" + str(row["TA"]), axis=1)
data.drop_duplicates("file_id_TA", inplace=True)

# --- Jointure

data_labeled = data.merge(df, how="inner", left_on="file_id_TA", right_on="file_id_TA", )
data_labeled.drop(["TA_y",], axis=1, inplace=True)
data_labeled.rename(columns={"TA_x": "TA"}, inplace=True)
# on enlève les requêtes qui ont plus de 60 pages
data_labeled = data_labeled[data_labeled["number_of_pages"] <= 60]

data_labeled['text'] = data_labeled['text'].apply(lambda x:
                                                  PreprocessingOptimized.nlp(x, disable="spellcheck_SpellChecker").text)
data_labeled.reset_index(drop=True, inplace=True)

# --- enregistrement du fichier
data_labeled.to_csv(r"data/data_labeled_updated.csv", index=False, sep=";")
