import time
import math
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
        sucess, frame = cap.read() # read the webcam frame
        if not sucess:
            break
        cv2.imshow("Webcam",frame) # Opens a window called Webcam and display frame
        if cv2.waitKey(1) & 0xFF == ord("q"): # Creates a delay for cv2 to update , 
            break

        rgb_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # converts cv2 BGR colour to RGB for face landmarker
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_color)
        timestamp = int(time.time()*1000) # creates a time reference for mediapipe and converts it into miliseconds.
        result = landmarker.detect_for_video(mp_image,timestamp)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0] # list of all 476 facial landmarks
            right_eye = landmarks[33] # corner on right eye
            left_eye = landmarks[263] # corner on left eye
            diff_x = right_eye.x - left_eye.x
            diff_y = right_eye.y - left_eye.y

            angle = math.degrees(math.atan2(diff_y,diff_x))
            print(angle)
            
    cap.release()
    cv2.destroyAllWindows()