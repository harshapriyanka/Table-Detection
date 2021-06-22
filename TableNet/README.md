# TableNet

This repository consists of extension of [TableNet](https://arxiv.org/abs/2001.01469) i.e. base model VGG is replaced by **ResNet18**.

To training or predict, you should first install the requirements by running the following code:

```bash
pip install -r requirements.txt
```
To install 'pytesseract'
'''
apt install tesseract-ocr
apt install libtesseract-dev
pip install pytesseract
'''

To train is only needed the `train.py` file which can be configured as wanted.

To predict, it can be used the pre-trained weights already available and should be downloaded on the following link: [TableNet Weights](https://drive.google.com/drive/folders/1LvPnSxnDrl0dywRGAxbOD6hX-jmvw_qb?usp=sharing)

In the same link, you find `data` alongwith **Annotations**.

```bash
 python predict.py --model_weights='<weights path>' --image_path='<image path>'
```

or simply:
```bash
 python predict.py
```

To predict with the default image.

Reference: [OCR_TableNet](https://github.com/tomassosorio/OCR_tablenet)
