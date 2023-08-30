import os
from pathlib import Path

from PIL import Image
import pytesseract


img_folder = r".\data\requetes_img3"
txt_folder = r".\data\requetes_txt3"

req_folders = os.listdir(img_folder)

for req_folder in req_folders:

    text_file = txt_folder / Path(req_folder + ".txt")
    image_file_list = os.listdir(img_folder + '/' + req_folder)

    if os.path.exists(text_file):
        print("txt file: ", text_file, "already exists.")
    else:
        with open(text_file, "w+", encoding='utf-8') as output_file:

            for image_file in image_file_list:
                image_file = os.path.abspath(img_folder + '/' + req_folder + '/' + image_file)
                # --- récupération du texte
                text = str((pytesseract.image_to_string(Image.open(image_file), lang='fra')))

                output_file.write(text)
        print(req_folder, "--to txt--> done")