import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pickle
from database_operations import insert_new_data, get_name, get_all_encodings, get_details

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="486279315",
  database="face_recognition"
)


known_face_names, known_face_encodings = get_all_encodings(mydb=mydb)
details = get_details(mydb=mydb)
print(details)

print(known_face_names)

# print(type(known_face_encodings[0][0]))

# path = 'images'

# images = []
# classNames = []
# mylist = os.listdir(path)
# for cl in mylist:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

cap = cv2.VideoCapture(0)
while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
            name = "Unknown"
            company = ""
            position = ""
            can_access = ""

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = details[best_match_index][0]
                position = details[best_match_index][1]
                company = details[best_match_index][2]
                can_access = details[best_match_index][3]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Add debug prints to check coordinates and names
        print(f"Coordinates: top={top}, right={right}, bottom={bottom}, left={left}, name={name}")

        # Ensure coordinates are within frame dimensions
        if top < 0 or right < 0 or bottom < 0 or left < 0 or top >= frame.shape[0] or right >= frame.shape[1] or bottom >= frame.shape[0] or left >= frame.shape[1]:
            print(f"Invalid coordinates for name={name}")
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), 0)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left, top - 8), font, 1.0, (0, 255, 0), 2)
        cv2.putText(frame, company, (right + 6, top + 30), font, 1.0, (0, 255, 0), 2)
        cv2.putText(frame, position, (right + 6, int((top + bottom) / 2) + 14), font, 1.0, (0, 255, 0), 2)
        cv2.putText(frame, can_access, (right + 6, bottom), font, 1.0, (0, 255, 0), 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()