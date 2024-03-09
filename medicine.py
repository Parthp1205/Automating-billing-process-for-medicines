import re
import cv2
import pandas as pd
import difflib as diff
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import pandas as pd
import pandas as pd
from difflib import SequenceMatcher

# Importing required methods for inference and visualization.
from paddleocr import PaddleOCR,draw_ocr

# Initializing OCR, OCR will automatically download PP-OCRv3 detector, recognizer and angle classifier.
ocr = PaddleOCR(use_angle_cls=True)
nlp = spacy.blank("en") # load a new spacy model
db = DocBin() # create a DocBin object
nlp_ner_2 = spacy.load("./Model/model-best_2")


# inv_df = pd.DataFrame(columns=[])

'''
IMG_0962.jpg
IMG_0961.jpg
IMG_0951.jpg
img_5.jpeg
'''

# OCR function
def finalFUNC(filename,products):
    Product=""
    print("4")
    result = ocr.ocr(filename, cls=True)
    myresult=''
    for x in result:
        myresult += ' '+x[1][0]
    print("--OUTPUT--->",myresult)
    
    #REGEX
    batch_number = re.search(r'(BatchNo,|BatchNo|Batch No.:|Batch No\.|BatchNo\.|Batch|B\.No\.|B\.NO\.|B\.No|BNo.|B.N|N0:|No.)\s*(\w+)', myresult)
    bno=""
    if batch_number:
        bno = batch_number.group(2)
        print("Batch number:", batch_number.group(2))
    else:
        print("Batch number not found in the text.")

    
    #SPACY
    doc_2 = nlp_ner_2(myresult)
    # spacy.displacy.render(doc_2, style="ent", jupyter=True) # display in Jupyter

    for ent in doc_2.ents:
        if ent.label_ == 'BATCH':
            bno = ent.text
            print('1. Bno: = ',bno)

    pattern = 'B.NO|BNO|batch no|batch. no|B.N0|BN0.|BatchNo.|B.N|'
    bno = re.sub(pattern.casefold(), '',bno.casefold()).replace('.','')

    print('2. Bno: = ',bno)

    #SIMILARITY

    df = pd.read_csv('./Dataset/Medicine_Data.csv')
    text_column = df['Batch']
    #text = "2KN2J002"

    similarity_ratios = []
    for i in text_column:
        ratio = SequenceMatcher(None, i.casefold(), bno).ratio()
        similarity_ratios.append(ratio)

    # Find the maximum similarity ratio
    max_similarity = max(similarity_ratios)
    df['Ratio']=similarity_ratios
    # Print the maximum similarity ratio
    print("Maximum similarity ratio:", max_similarity)

    # saving the dataframe
    df.to_csv('./Dataset/Similarity_Ratio.csv')

    df = pd.read_csv('./Dataset/Similarity_Ratio.csv')
    # create a new empty dataframe

    max_similarity = max(df['Ratio'])
    for index, row in df.iterrows():
        if row['Ratio'] == max_similarity and max_similarity >0.5:
            #print(row['Company'],row['Name'],row['Batch'],row['MRP'],row['Mfg_dt'],row['Exp_dt'])
            print(row[1:7],"\n")
            Product=row['Name']
            BatchNo=row['Batch']
            Expiry_Date=row['Exp_dt']
            Mfg_dt=row['Mfg_dt']
            Price=row['MRP']
            
            # inv_df = inv_df.append({'Product': Product,
            #                 'Batch': BatchNo,
            #                 'Expiry': Expiry_Date,
            #                 'Mfg': Mfg_dt,
            #                 'Price': Price}, ignore_index=True)
            new_product = {"name": Product, "batch": BatchNo, "expiry_date": Expiry_Date, "mfg_date":Mfg_dt, "price": Price}
            products.append(new_product)
            break
    status = Product
    if status:
        return status
    else:
        status = "Not"
        return status