import numpy as np
import cv2
import pandas as pd
import pytesseract
from math import ceil
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OCR on Tablular Image")
    parser.add_argument('--img-path', type=str, help='path to your image.')
    parser.add_argument('--roi-path', type=str, help='folder path to roi .npy files.')
    args = parser.parse_args()

    text_list_path = roi_path + '/output1.npy'
    # box_list_path = roi_path + '/output2.npy' # or '/output1.npy'

    text_list = np.load(text_list_path)
    # box_list = np.load(box_list_path)

    img = cv2.imread(img_path)

    text_list_sort = sorted(text_list[0], key = lambda x: (x[1], x[0]))

    ymin_prev = 0
    rows = []
    row = []
    row_count = []

    for i in text_list_sort:
        xmin, ymin, xmax, ymax = i[:-1]
        xmin = ceil(xmin)
        ymin = ceil(ymin)
        xmax = ceil(xmax)
        ymax = ceil(ymax)
        roi = img[ymin:ymax, xmin:xmax]
        config = ("-l eng --oem 3 --psm 8")
        text = pytesseract.image_to_string(roi, config=config)
        text_processed = [t for t in text if t not in ['\n', '\x0c']]
        text = ''.join(text_processed)

        if abs(ymin-ymin_prev)>5:
            rows.append(row)
            row_count.append(len(row))
            row = []  
            row.append(text)
        else:  
            row.append(text)        
            
        ymin_prev = ymin

    updated_text_rows = list()
    column_count = max(row_count)

    for row in rows:
        diff = column_count - len(row)
        for _ in range(diff):
            row.append(" ")
        updated_text_rows.append(row)

    # Creating a dataframe of the generated OCR list
    arr = np.array(updated_text_rows) 
    dataframe = pd.DataFrame(arr)
    dataframe.to_csv("output.csv", index=False)