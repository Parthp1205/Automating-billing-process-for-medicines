from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import os.path
import os

# os.environ['KMP_DUPLICATE_LIB_OK']=True
# export KMP_DUPLICATE_LIB_OK=TRUE
#-------------------------------------
# import re
# import cv2
# import pandas as pd
# import difflib as diff
# import spacy
# from spacy.tokens import DocBin
# from tqdm import tqdm
# import pandas as pd

# Importing required methods for inference and visualization.
from paddleocr import PaddleOCR,draw_ocr

from medicine import finalFUNC

# Initializing OCR, OCR will automatically download PP-OCRv3 detector, recognizer and angle classifier.
ocr = PaddleOCR(use_angle_cls=True)
folder = './Uploads'
#-------------------------------------


app = Flask(__name__)



# products = [
#     {"name": "Product 1","batch": "12345", "expiry_date": "2023-05-01", "mfg_date":"2020-05-01", "price": "$10.99"},
#     {"name": "Product 2","batch": "12345", "expiry_date": "2022-12-31", "mfg_date":"2020-05-01", "price": "$24.99"},
#     {"name": "Product 3","batch": "12345", "expiry_date": "2024-06-15", "mfg_date":"2020-05-01", "price": "$4.99"},
# ]
# OCR function
# def ocr_core(filename):
#     print("3")
#     text = pytesseract.image_to_string(Image.open(filename))
#     print("--OUTPUT--->",text)
#     return text

# OCR function

# def paddle_ocr(filename):
#     print("4")
#     result = ocr.ocr(filename, cls=True)
#     myresult=''
#     for x in result:
#         myresult += ' '+x[1][0]
#     print("--OUTPUT--->",myresult)
#     return myresult

products = []
# Route for home page
@app.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        products.clear()
        return redirect(url_for("index"))
    else:
        return render_template('index.html')

# Route for products page
@app.route('/viewProducts', methods=['GET', 'POST'])
def viewProducts():
    if request.method == 'POST':
        if request.form.get('VIEW_PRODUCT') == 'VIEW_PRODUCT':
            total_amount = sum(product['price'] for product in products)
            total_amount = round(total_amount, 2)
            dis_per = 5
            discount = round((total_amount * dis_per)/100,2)
            final_amount = round(total_amount - discount,2)
            return render_template("products.html", products=products, total_amount=total_amount,
                                   discount=discount,final_amount=final_amount)
            
            
        

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Get uploaded file
    file = request.files['file']

    # Save the file to disk
    file_name = file.filename
    file_path = os.path.join(folder, file_name)
    file.save(file_path)

    # Get text from the uploaded image
    productName = finalFUNC(file_path,products)
    text = f'{productName} Added !!'

    # Render template with extracted text
    return render_template('index.html', text=text)

if __name__ == '__main__':
    app.run(debug=True,port=8000, host='0.0.0.0')
    # app.run(debug=True)