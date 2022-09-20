import cv2
from facial_emotion_recognition import EmotionRecognition
from pytesseract import pytesseract

frame_width = 0
frame_height = 0
my_video = ""
output_dir = ""
emotion_model = None
time_to_leave_in_sec = 0
lectureKeyWords = []
path_tesseract = ""
input_dir = ""

def init():
    global frame_width
    global frame_height
    global input_dir
    global output_dir
    global emotion_model
    global time_to_leave_in_sec
    global lectureKeyWords
    global path_tesseract
    input_dir = "./input"
    frame_width = 1920
    frame_height = 1080
    output_dir = "./output/"
    emotion_model = EmotionRecognition(device='cpu', gpu_id=0)
    time_to_leave_in_sec = 5
    lectureKeyWords = open("./keywords.txt", "r").read().split(";")
    path_tesseract = "/usr/bin/tesseract"
    pytesseract.tesseract_cmd = "/usr/bin/tesseract"
