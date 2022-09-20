#
# Docker image for Social-Reporter
# Credits: https://github.com/VanakiWahid/PO-wahid
#

FROM ubuntu:bionic-20220902

WORKDIR /app
ADD Social-Reporter /app/Social-Reporter

RUN apt-get update \
    && apt-get install software-properties-common -y \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install python3.7 python3.7-distutils python3-pip -y \
    && apt-get install python3-pip -y 

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
    && update-alternatives --config python3 \
    && apt-get -y install tesseract-ocr

RUN pip3 install --upgrade pip \
    && pip3 install /app/Social-Reporter/requirements.txt


RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && apt-get install libtesseract-dev -y

RUN rm /usr/local/lib/python3.7/dist-packages/cvlib/object_detection.py \
    &&  rm /usr/local/lib/python3.7/dist-packages/facial_emotion_recognition/facial_emotion_recognition.py \
    &&  cp -a /app/Social-Reporter/adapted_python_libs/object_detection.py /usr/local/lib/python3.7/dist-packages/cvlib/ \
    &&  cp -a /app/Social-Reporter/adapted_python_libs/facial_emotion_recognition.py /usr/local/lib/python3.7/dist-packages/facial_emotion_recognition/
