import cv2

for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Camera {i}", frame)
            print(f"Camera {i} opened - press key to continue")

            cv2.waitKey(0)
            cv2.destroyAllWindows()

        cap.release()

print("Done")