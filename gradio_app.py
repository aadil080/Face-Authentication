import gradio as gr
import cv2
import mediapipe as mp
import numpy as np

#Creating MediaPipe Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
cap = cv2.VideoCapture(0)


# Function to normalize landmarks
def normalize_landmarks(landmarks):
    mean = np.mean(landmarks, axis=0)
    std = np.std(landmarks, axis=0)
    normalized = (landmarks - mean) / std
    return normalized

# Function to check authorization of the user for access
def check_identity(to_check_landmarks, threshold=0.15):
    global known_landmarks

    # Normalize both sets of landmarks
    known_landmarks_normalized = normalize_landmarks(known_landmarks)
    to_check_landmarks_normalized = normalize_landmarks(to_check_landmarks)

    # Calculate the difference between the normalized known landmarks and the landmarks to check
    landmarks_diff = np.linalg.norm(known_landmarks_normalized - to_check_landmarks_normalized, axis=1)
    
    # Calculate mean of differences
    accuracy = np.mean(landmarks_diff)
    
    print("Accuracy", accuracy)

    # Compare with a threshold to determine if it's a match
    if accuracy <= threshold:
        print("Authorized")
        return True  # Authorized
    else:
        return False  # Not authorized


# To process real-time video feed
def processing_image():
    
    while True:
        ret, image = cap.read()
        if ret is not True:
            break
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, _ = rgb_image.shape
            result = face_mesh.process(rgb_image)
            if result.multi_face_landmarks is None:
                print("NoneType")
            else:
                landmarks_to_check = np.zeros((468, 3), dtype=np.float64)
                i=0
                for facial_landmarks in result.multi_face_landmarks:
                    for i in range(0, 468):
                        pt1 = facial_landmarks.landmark[i]
                        x = int(pt1.x * width)
                        y = int(pt1.y * height)
                        z = pt1.z
                        landmarks_to_check[i] = [x/width, y/height, z]
                        cv2.circle(image, (x, y), 1, (0, 255, 0), -1)

                authorized = check_identity(landmarks_to_check)
                if authorized:
                    cv2.putText(image, "Authorized", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    yield image
                    break
                
        except:
            print("No image")


        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        yield image  # Yield the image for real-time display

# To add new user to the system
def processing_input_image(image):
    try:
        print("type(image)", type(image))
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_image)
        if result.multi_face_landmarks is None:
            print("NoneType")
            return image
        facial_landmarks = result.multi_face_landmarks
        flat_landmarks = np.zeros((468, 3), dtype=np.float64)
        i=0
        for landmark in facial_landmarks:
            for point in landmark.landmark:
                flat_landmarks[i] = [point.x, point.y, point.z]
                i+=1

        np.save("aadil", flat_landmarks)
    except Exception as e:
        print("ERROR",e)


# Gradio application
with gr.Blocks() as demo:
    with gr.Row():
        output_image = gr.Image()
        input_image = gr.Image()
    
    with gr.Row():
        start_button = gr.Button(value="Start Recording...", variant="primary")
        stop_button = gr.Button(value="Stop Recording...", variant="stop")
    
    start_button.click(processing_image, outputs=[output_image])
    # stop_button.click(stop_recording)
    input_image.change(fn=processing_input_image, inputs=[input_image])


if __name__ == "__main__":

    known_landmarks = np.load("aadil.npy")
    # print("known_landmarks", known_landmarks)
    
    demo.launch()