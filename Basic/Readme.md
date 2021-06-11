# Tabular Image to CSV:-

## Prerequisites :-

* [OpenCV]()
* [pytesseract]()
* [PIL]()
* [Pandas]()
* [Imutils]()



### Installing Requirements:

Install requirements from requirements.txt
```
pip install -r requirements.txt
```

To install 'pytesseract'
'''
apt install tesseract-ocr
apt install libtesseract-dev
pip install pytesseract
'''

##Project Structure:-

* [images]() :- This folder contains images to be used for OCR.
* [output_csv]() :- It contains result of tabular image in csv file.
* [processed_image]() :- Contains images generated while pre-processing.
* [requirements.txt]() :- Requirement file.
* [image-to-csv.py]() :- Code file.




## Python command  to run script

```
python3 image-to-csv.py --img-path images/patient.png
```

### Original:-

![Screenshot](images/patient.png)

### Threashold:-

![Screenshot](processed_image/threshold.png)

### Dialated:-

![Screenshot](processed_image/dilation.png)

### ROI:-

![Screenshot](processed_image/show_box.png)






    
