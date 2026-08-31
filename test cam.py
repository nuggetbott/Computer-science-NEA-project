"""
Eyebrow raise detection for Face Bouncer
-----------------------------------------
Implements the "Both eyebrows raised?" decision from the face tracking
flowchart, using the MediaPipe Tasks FaceLandmarker API. Returns
"pause_menu" when both eyebrows are raised, otherwise returns no_input
(None), matching the track_face() pseudocode design.

Requires:
    pip install opencv-python mediapipe

Model file (required):
    Download "face_landmarker.task" from:
    https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task
    and place it in the same folder as this script.
"""

import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
MODEL_PATH = "face_landmarker.task"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True,          # gives expression scores directly
    output_facial_transformation_matrixes=False,
)
landmarker = vision.FaceLandmarker.create_from_options(options)

# Blendshape score needed (0.0-1.0) before an eyebrow counts as "raised".
# This is the sensitivity threshold - tune this during iterative testing.
# Lower = more sensitive (may cause false triggers).
# Higher = less sensitive (may miss genuine raises), which fits Tim's
# preference for the game to miss an action rather than trigger the wrong one.
RAISE_THRESHOLD = 0.4


def get_blendshape_score(blendshapes, category_name):
    """Return the score (0.0-1.0) for a named blendshape, or 0.0 if absent."""
    for category in blendshapes:
        if category.category_name == category_name:
            return category.score
    return 0.0


def check_eyebrows_raised(blendshapes):
    """
    Returns True if both eyebrows are raised above RAISE_THRESHOLD,
    otherwise False. Corresponds to the "Both eyebrows raised?" decision
    box in the face tracking flowchart.
    """
    left_score = get_blendshape_score(blendshapes, "browOuterUpLeft")
    right_score = get_blendshape_score(blendshapes, "browOuterUpRight")
    return left_score > RAISE_THRESHOLD and right_score > RAISE_THRESHOLD


def track_face(frame, timestamp_ms):
    """
    Processes a single video frame and returns the mapped game action,
    matching the track_face() function in the algorithm design.
    Returns "pause_menu" or None (no_input).
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # MediaPipe expects RGB
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = landmarker.detect_for_video(mp_image, timestamp_ms)

    if not result.face_blendshapes:
        return None  # no face detected -> no_input

    blendshapes = result.face_blendshapes[0]

    if check_eyebrows_raised(blendshapes):
        return "pause_menu"

    return None  # no_input


# ---------------------------------------------------------------------------
# Live webcam test loop
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # mirror for a natural selfie-view
        timestamp_ms = int((time.time() - start_time) * 1000)

        action = track_face(frame, timestamp_ms)

        # On-screen feedback for testing
        label = action if action else "no_input"
        colour = (0, 200, 0) if action else (0, 0, 200)
        cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, colour, 2)

        cv2.imshow("Face Bouncer - Eyebrow Detection Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()