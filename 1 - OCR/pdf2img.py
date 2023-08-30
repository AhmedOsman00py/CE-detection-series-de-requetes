# install poppler.exe
import os
import sys
from PIL.Image import DecompressionBombError

from pathlib import Path
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


# --- PDF to IMG

pdf_folder = sys.argv[1]  # pdf_folder = r"data/requetes_pdf"
img_folder = sys.argv[2]  # img_folder = r"data/requetes_img"

pdf_files = os.listdir(pdf_folder)

decompression_error = 0
for file_name in pdf_files:
    
    file = os.path.abspath(pdf_folder + '/' + file_name)
    file_name = os.path.splitext(file_name)[0]

    try:
        os.mkdir(os.path.abspath(img_folder + '/' + file_name))
        print(f"{os.path.splitext(img_folder + '/' + file_name)[0:2]}  : file created.")
    except:
        print(f"{os.path.splitext(img_folder + '/' + file_name)[0:2]}  : file already exists.")
        continue

    try:
        pages = convert_from_path(file, 300)
    except DecompressionBombError:
        print(f"-----\n\n{file_name} - Image size exceeds limit of 178956970 pixels\n\n-----")
        os.rmdir(os.path.abspath(img_folder + '/' + file_name))
        decompression_error += 1
        continue

    i = 1
    for page in pages:
        image_name = "Page_" + str(i) + ".jpg"
        page.save(img_folder + '/' + file_name + '/' + image_name, "JPEG")
        i = i + 1

print(f"Decompression Bomb Error -->  {decompression_error} files.")
