# SocialReporter
As a master thesis a system was developed, which recognizes the interesting moments in events of the university, in order to post it in the social media.

## Requirements
It is recommended to use following versions: 

```
Python=3.7.1
pip=21.1.2
```


## How to setup
- All required packages are summarized in requirements.txt. Install all these packages: 
``
pip -r requirements.txt
``
- Folder adapted_python_libs contains two modified Python classes (object_detection.py and facial_emotion_recognition.py). 
The just installed classes must be overwritten with these.
  1. Navigate to the install location of object_detection.py. This should be in: 
  ``
  C:\Users\{username}\AppData\Local\Programs\Python\Python37\Lib\site-packages\cvlib\object_detection.py
  ``
  2. Replace it's content with: 
  ``
  adapted_python_libs/object_detection.py
  ``
  3. save replaced file.
  4. Repeat the process for facial_emotion_recognition.py

- Install Tessarct as described here
``
https://medium.com/@marioruizgonzalez.mx/how-install-tesseract-orc-and-pytesseract-on-windows-68f011ad8b9b
``. Select as installation location: ``C:/Program Files (x86)/Tesseract-OCR``. 
- You can also choose another installation location. Then adjust the corresponding paths in ``config.py (lines 31 and 32)``.



## How to use
- Start main program:
``
python social_reporter.py
``
  - The files are loaded one after the other from the folder ``input`` and analyzed
  - The files in the folder must have the following format: ``Cam01_20211015_174122``
  - If a social media relevant image is given, the image will be extracted to the folder: ``output``
  - In addition, an entry will be written in the file ``output/contents.csv``

- Start collage maker:
``
python collage_maker.py
``
  - Photo collages are created from the folder ``output``
  - If there are enough single images, the collage will be created again in the same folder

## Thesis

This work is the result of Mustafa Dursun's thesis in the masters program [Digital Business Engineering](https://www.hhz.de/master/digital-business-engineering/) at the [Herman Hollerith Center](https://www.hhz.de/) in Böblingen. 

### Abstract

Reporting on social media about the daily life of a university involves a lot of organizational effort, because the content is created in manual activity. For the generation of images from the daily lecture routine, the lectures are interrupted and the writing of a corresponding text is a time-consuming activity that has to be carried out afterwards. 

The concept of lifelogging promises to assist in the editorial work of a university by collecting images during lecture events for publication. Lifelogging is understood as the digital recording of the various forms of everyday life. In the context of this thesis a design space of such a system is investigated, which recognizes relevant image content with as little human interaction as possible and generates appropriate texts for it. The developed software solution is a prototype that serves to extend smart environments of an event space. 

First, an overview of the various existing lifelogging approaches is provided and these are compared with the solution proposed in this thesis. Subsequently, the prototype is presented and evaluated.

### BibTeX

Please cite this work using this BibTex entry:

```
@mastersthesis{dursun2022,
    author     =     {Mustafa Dursun},
    title      =     {Social Reporter – Entwicklung und Evaluation eines Lifelogging Systems für Hochschulen, um Bilder aus dem Alltag der Hochschule für soziale Medien zu erfassen},
    school     =     {Herman-Hollerith-Zentrum, Fakultät Informatik, Hochschule Reutlingen},
    address    =     {Alteburgstraße 150, 72762 Reutlingen, Germany},
    month      =     {February},
    year       =     {2022},
}
```


