import cv2
import numpy as np
import pandas as pd
import random
from imutils import contours
import argparse
import pytesseract
from math import ceil

def preprocessing_non_tabular(path):
    img = cv2.imread(path)

    # ----Grayscaling Image----
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- performing Otsu threshold ---
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    cv2.imwrite("processed_image/threshold.png", thresh1)
    # cv2.imshow('thresh1', thresh1)
    # cv2.waitKey(0)

    # ----Image dialation----
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    cv2.imwrite("processed_image/dilation.png", dilation)
    # cv2.imshow('dilation', dilation)
    # cv2.waitKey(0)

    # ---Finding contours ---
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return img, contours[::-1]


def preprocessing_tabular(path):
    # Load image
    img = cv2.imread(path)
    # img = cv.GaussianBlur(img,(5,5),0)

    # ----Grayscaling Image----
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- performing Otsu threshold ---
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # thresh = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)

    # Remove text characters with morph open and contour filtering
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    cnts = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 500:
            cv2.drawContours(opening, [c], -1, (0, 0, 0), -1)

    # Repair table lines, sort contours, and extract ROI
    close = 255 - cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

    cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts, _ = contours.sort_contours(cnts, method="top-to-bottom")
    return img, cnts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OCR on Tablular Image")
    parser.add_argument('--img-path', type=str, help='path to your image.')
    args = parser.parse_args()

    # ---Image_Path---
    path = args.img_path
    # path = "images/patient.png"

    img, cnts = preprocessing_non_tabular(path)
    if len(cnts) < 8:
        img, cnts = preprocessing_tabular(path)

    
    dummy_image = img.copy()

    bboxes = []

    for idx, cnt in enumerate(cnts):
        x, y, w, h = cv2.boundingRect(cnt)
        bboxes.append([ceil(x), ceil(y), ceil(x+w), ceil(y+h)])

    bboxes_sort = sorted(bboxes, key=lambda x:(x[1], x[0]))

    ymin_prev = 0
    rows = []
    single_row = []
    row_count = []

    for i in bboxes_sort:
        xmin, ymin, xmax, ymax = i
        roi = img[ymin:ymax, xmin:xmax]
        config = ("-l eng --oem 3 --psm 8")
        text = pytesseract.image_to_string(roi, config=config)
        # text_processed = [t for t in text if t not in ['\n', '\x0c', '<<', '-', '@', '(', ')']]
        text_processed = [t for t in text if t.isalnum() or t == ' ' or t == ':' 
                          or t == '.' or t == '/' or t == '=' or t == '&']
        text = ''.join(text_processed)

        # print(text)

        if abs(ymin-ymin_prev)>10:
            rows.append(single_row)
            row_count.append(len(single_row))
            single_row = []  
            single_row.append(text)
        else:  
            single_row.append(text) 

        ymin_prev = ymin

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # Drawing box
        cv2.rectangle(dummy_image, (xmin, ymin), (xmax, ymax), (b, g, r), 2)
    
    cv2.imwrite("processed_image/show_box.png", dummy_image)
    # cv2.imshow('final', dummy_image)
    # cv2.waitKey(0)

    print(row_count)

    updated_text_rows = list()
    columns = max(row_count)

    print(columns)

    for row in rows:
        diff = columns - len(row)
        for _ in range(diff):
            row.append(" ")
        updated_text_rows.append(row)

    # Creating a dataframe of the generated OCR list
    arr = np.array(updated_text_rows)       
    dataframe = pd.DataFrame(arr)
    dataframe.to_csv("output_csv/output.csv", index=False)
