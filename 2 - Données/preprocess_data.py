import os
import re
import pandas as pd


def get_data_as_df(txt_folder_path, img_folder_path):
    files = os.listdir(txt_folder_path)

    files_name = []
    files_text = []
    num_of_pages = []
    for file in files:
        files_name.append(os.path.splitext(file)[0])
        num_of_pages.append(len(os.listdir(fr"{img_folder_path}\{file[:-4]}")))
        with open(fr"{txt_folder_path}\{file}", "r", encoding="utf-8") as file_text:
            text = file_text.read()
            files_text.append(text)
        print(file, "done")

    return pd.DataFrame(
        {"file_id": range(1, len(files_name) + 1), "file_name": files_name, "number_of_pages": num_of_pages,
         "text": files_text})


def find_id(string):
    file_id = re.findall(r'\d+', string)
    for id in file_id:
        if len(str(id)) == 7:
            return id
    return file_id


if __name__ == "__main__":

    data = get_data_as_df(r"data\requetes_txt", r"data\requetes_img")
    data["file_id"] = data.file_name.apply(find_id)
    data = data.drop_duplicates(["text"])

    data.to_csv("data_labeled_updated.csv", sep=";", index=False)
