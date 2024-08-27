import cv2
import mediapipe as mp
import numpy as np

#Creating MediaPipe Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

cap = cv2.VideoCapture(0)

while True:
    ret, image = cap.read()

    if ret is not True:
        break

    # Importing Image
    # image = cv2.imread('images/Bill Gates.jpg')
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, _ = rgb_image.shape

    # Extracting Landmarks
    result = face_mesh.process(rgb_image)

    if result.multi_face_landmarks is None:
        print("NoneType")
    else:
        for facial_landarks in result.multi_face_landmarks:
            for i in range(0, 468):
                pt1 = facial_landarks.landmark[i]
                x = int(pt1.x * width)
                y = int(pt1.y * height)
                # print("x, y : ", x, y)
                cv2.circle(image, (x, y), 1, (0, 255, 0), -1)

    cv2.imshow('Image', image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


# Destroy all OpenCV windows
cv2.destroyAllWindows()