import os
import time
import math
import cv2
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


all_face = True # set to true if you want to see all the landmarks, set to false if you only want to see the eyebrow and eye landmarks
model_url  = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task" # trained model for face landmark detection
model_path = "face_landmarker.task"
if not os.path.exists(model_path):
    # Only download if it isn't already sitting in the project folder, and
    # don't let a network hiccup crash the whole program.
    try:
        urllib.request.urlretrieve(model_url, model_path) # dowloading the model into dir
    except (urllib.error.URLError, urllib.error.HTTPError) as error:
        raise SystemExit(f"Could not download face landmark model: {error}")

base_options = python.BaseOptions(model_asset_path=model_path) # tell mediapipe where the model is located and to load it
options = vision.FaceLandmarkerOptions(  # required options for the face landmark model
    base_options= base_options,
    running_mode = vision.RunningMode.VIDEO,
    num_faces =1,
    output_face_blendshapes = True,
    output_facial_transformation_matrixes = True
)
def draw_landmark(frame,result,no):
    if not result.face_landmarks:  # if no face is detected, return
        return
    landmarks = result.face_landmarks[0] # set landmark as the first face detected
    pixel_x = int(landmarks[no].x*w) # turn the normalised value into actual frame width
    pixel_y = int(landmarks[no].y*h) # turn the normalised value into actual farm length
    cv2.circle(frame, (pixel_x,pixel_y),1,(0,255,0),-1) # drawing a green dot on the landmark point, -1 means fill the circle, 1 is the radius of the circle
    return

def draw_all_landmarks(frame,result):
    if not result.face_landmarks: # if no face is detected, return
        return
    landmarks = result.face_landmarks[0] # set landmark as the first face detected
    h,w,_ = frame.shape
    for i in range(len(landmarks)):
        pixel_x = int(landmarks[i].x*w) # turn the normalised value into actual frame width
        pixel_y = int(landmarks[i].y*h) # turn the normalised value into actual farm length
        cv2.circle(frame, (pixel_x,pixel_y),1,(0,255,0),-1) # drawing a green dot on the landmark point, -1 means fill the circle, 1 is the radius of the circle
    return

def detect_angle(result):
    if result.face_landmarks:
        landmarks = result.face_landmarks[0]
        right_eye = landmarks[33] # corner on right eye
        left_eye = landmarks[263] # corner on left eye
        diff_x = right_eye.x - left_eye.x
        diff_y = right_eye.y - left_eye.y
        angle = math.degrees(math.atan2(diff_y,diff_x))
        return angle
    return None
def detect_eyebrow_raised(result):
    if result.face_landmarks:
        landmarks = result.face_landmarks[0]
        eye = landmarks[65]
        eyebrow = landmarks[145]
        eyebrow_gap = (eyebrow.y - eye.y)*100
        right_eye = landmarks[33] # corner on right eye
        left_eye = landmarks[263] # corner on left eye
        eye_width = left_eye.x - right_eye.x
        relative_eyebrow_gap = eyebrow_gap / eye_width # Find relative gap between eyebrow and eye based on eye width, to remove distance factor
        if relative_eyebrow_gap > 46:  # Adjust this threshold 
            print("eyebrow raised")
        return relative_eyebrow_gap
    return None

with vision.FaceLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0) # Opens the webcam
    if not cap.isOpened(): 
        print("Error: Could not open webcam.")
        exit()
    try:
        while True:
            sucess, frame = cap.read() # read contains the frame and whether the frame was successfully read or not
            if not sucess:
                break

            rgb_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert the frame form BGR to RGB
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_color)
            timestamp = int(time.time() * 1000)
            result = landmarker.detect_for_video(mp_image, timestamp)

            draw_landmark(frame, result, 65)
            draw_landmark(frame, result, 145)
            if all_face :
                draw_all_landmarks(frame, result)

            cv2.imshow("Webcam", frame)
            print(detect_eyebrow_raised(result))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
