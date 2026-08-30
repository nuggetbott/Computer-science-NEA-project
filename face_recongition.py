import time
import cv2
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_url  = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task" # trained model for face landmark detection
urllib.request.urlretrieve(model_url, "face_landmarker.task") # dowloading the model into dir

base_options = python.BaseOptions(model_asset_path="face_landmarker.task") # tell mediapipe where the model is located and to load it
options = vision.FaceLandmarkerOptions(
    base_options= base_options,
    running_mode = vision.RunningMode.VIDEO,
    num_faces =1,
    output_face_blendshapes = True,
    output_facial_transformation_matrixes = True
)
with vision.FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0) # Opens the webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
    while True: