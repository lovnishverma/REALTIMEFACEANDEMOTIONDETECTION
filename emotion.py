import streamlit as st
import cv2
import numpy as np
import time
from keras.models import load_model
import tempfile
from PIL import Image
# Larger title
st.markdown("<h1 style='text-align: center;'>Emotion Detection</h1>", unsafe_allow_html=True)

# Smaller subtitle
st.markdown("<h3 style='text-align: center;'>angry, fear, happy, neutral, sad, surprise</h3>", unsafe_allow_html=True)
start = time.time()

@st.cache_resource
def load_emotion_model():
    model = load_model('CNN_Model_acc_75.h5')
    return model

# Load the model
model = load_emotion_model()
print("time taken to load model : " , time.time() - start)
img_shape = 48
emotion_labels = ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def process_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        face_roi = cv2.resize(roi_color, (img_shape, img_shape))
        face_roi = np.expand_dims(face_roi, axis=0)
        face_roi = face_roi / float(img_shape)
        predictions = model.predict(face_roi)
        emotion = emotion_labels[np.argmax(predictions[0])]

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame

# def video_feed(video_source):
#     # Read and process video frames
#     while True:
#         ret, frame = video_source.read()
#         if not ret:
#             break
#         frame = process_frame(frame)
#         st.image(frame, channels="BGR")

def video_feed(video_source):
    # Create a placeholder to display the frames
    frame_placeholder = st.empty()  # This placeholder will be used to replace frames in-place

    while True:
        ret, frame = video_source.read()
        if not ret:
            break

        frame = process_frame(frame)

        # Display the frame in the placeholder
        frame_placeholder.image(frame, channels="BGR", use_column_width=True)



# Sidebar for video or image upload
upload_choice = st.sidebar.radio("Choose input source", [ "Upload Video", "Upload Image" ,"Camera"])

if upload_choice == "Camera":
    # Access camera
    video_source = cv2.VideoCapture(0)
    video_feed(video_source)

elif upload_choice == "Upload Video":
    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov", "avi", "mkv", "webm"])
    if uploaded_video:
        # Temporarily save the video to disk
        with tempfile.NamedTemporaryFile(delete=False) as tfile:
            tfile.write(uploaded_video.read())
            video_source = cv2.VideoCapture(tfile.name)
            video_feed(video_source)

elif upload_choice == "Upload Image":
    uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        frame = np.array(image)
        frame = process_frame(frame)
        st.image(frame, caption='Processed Image', use_column_width=True)

st.sidebar.write("Emotion Labels: Angry, Fear, Happy, Neutral, Sad, Surprise")