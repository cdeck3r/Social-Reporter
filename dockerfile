#
# Docker image for Social-Reporter
# based on https://github.com/VanakiWahid/PO-wahid/dockerfile
#

FROM ubuntu:bionic-20220902

WORKDIR /app
ADD Social-Reporter /app/Social-Reporter

RUN apt-get update \
    && apt-get -y install software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get -y install python3.7 python3.7-distutils python3-pip \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
    && update-alternatives --config python3 \
    && apt-get -y install tesseract-ocr \
    && apt-get -y install ffmpeg libsm6 libxext6 \
    && apt-get -y install libtesseract-dev 

RUN python3 -m pip install --upgrade pip \
    && cat /app/Social-Reporter/required_packages.txt | xargs -I{} sh -c 'pip3 install "$1" || exit 255' -- {} 

RUN rm /usr/local/lib/python3.7/dist-packages/cvlib/object_detection.py \
    &&  rm /usr/local/lib/python3.7/dist-packages/facial_emotion_recognition/facial_emotion_recognition.py \
    &&  cp -a /app/Social-Reporter/adapted_python_libs/object_detection.py /usr/local/lib/python3.7/dist-packages/cvlib/ \
    &&  cp -a /app/Social-Reporter/adapted_python_libs/facial_emotion_recognition.py /usr/local/lib/python3.7/dist-packages/facial_emotion_recognition/
