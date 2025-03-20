import streamlit as st
import cv2
import face_recognition
import os
from datetime import datetime
import sqlite3
import pandas as pd
import numpy as np
from PIL import Image

# --- App Configuration ---
st.set_page_config(
    page_title="Face Recognition Attendance",
    page_icon="✅",
    layout="wide"
)

# --- Database Connection ---
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# --- Create Attendance Table (if not exists) ---
cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        date TEXT,
        time TEXT,
        status TEXT 
    )
''')
conn.commit()

# --- Load Known Faces ---
def load_known_faces():
    """Loads known faces from the 'Photos' directory."""
    images = []
    classnames = []
    directory = "Photos"

    for cls in os.listdir(directory):
        if os.path.splitext(cls)[1] in [".jpg", ".jpeg"]:
            img_path = os.path.join(directory, cls)
            curImg = cv2.imread(img_path)
            images.append(curImg)
            classnames.append(os.path.splitext(cls)[0])

    return images, classnames

# --- Encode Known Faces ---
def find_encodings(images):
    """Encodes the given images."""
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# --- Load and Encode Known Faces ---
Images, classnames = load_known_faces()
encodeListKnown = find_encodings(Images)

# --- Add New Face ---
def add_new_face():
    """Adds a new face to the system."""
    new_name = st.text_input("Enter your name:")
    roll_no = st.text_input("Enter your roll number:")

    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None and new_name and roll_no:
        image = np.array(Image.open(img_file_buffer))  # Convert to numpy array
        img_path = os.path.join("Photos", f"{new_name}_{roll_no}.jpg")
        cv2.imwrite(img_path, image)

        # Update known faces and encodings
        global Images, classnames, encodeListKnown
        Images, classnames = load_known_faces()
        encodeListKnown = find_encodings(Images)

        # Add to database (without updating attendance)
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S')
        cursor.execute("INSERT INTO attendance (name, roll_no, date, time, status) VALUES (?, ?, ?, ?, 'Registered')", 
                       (new_name, roll_no, date, time))
        conn.commit()

        st.success(f"New face added for {new_name} ({roll_no}).")

# --- Face Recognition ---
def recognize_face():
    """Performs face recognition and updates attendance."""
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer is not None:
        with st.spinner("Recognizing face..."):
            image = np.array(Image.open(img_file_buffer))  # Convert to numpy array
            imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            name = "Unknown"
            roll_no = "Unknown"

            if len(encodesCurFrame) > 0:
                for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = classnames[matchIndex].split("_")[0]
                        roll_no = classnames[matchIndex].split("_")[1]

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    # Check for duplicate attendance entries
                    date = datetime.now().strftime('%Y-%m-%d')
                    time = datetime.now().strftime('%H:%M:%S')
                    cursor.execute("SELECT * FROM attendance WHERE name=? AND date=? AND time=?", (name, date, time))
                    existing_attendance = cursor.fetchone()

                    if existing_attendance:
                        st.info(f"Attendance already recorded for {name} at {time}.")
                    else:
                        # Allow manual marking of attendance
                        status = st.radio("Mark Attendance:", ("Present", "Absent"))
                        cursor.execute("INSERT INTO attendance (name, roll_no, date, time, status) VALUES (?, ?, ?, ?, ?)", 
                                       (name, roll_no, date, time, status))
                        conn.commit()
                        st.success(f"Attendance updated for {name} at {time} ({status}).")

            st.image(image, caption="Detected Face", use_container_width=True)
            if name == "Unknown":
                st.info("Face not recognized.")

# --- View Attendance Records ---
def view_attendance_records():
    """Displays attendance records."""
    st.subheader("Attendance Records")
    cursor.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")
    records = cursor.fetchall()

    if records:
        df = pd.DataFrame(records, columns=["ID", "Name", "Roll No", "Date", "Time", "Status"])
        st.table(df)
    else:
        st.info("No attendance records available.")

# --- Main App Logic ---
if __name__ == "__main__":
    st.title("Face Recognition Attendance")

    # --- Password Protection (Optional) ---
    password = st.text_input("Enter password", type="password")
    if password != "123":
        st.stop()

    # --- App Sections ---
    app_mode = st.sidebar.selectbox("Select Mode", ["Recognize", "Add New Face", "View Records"])

    if app_mode == "Recognize":
        recognize_face()
    elif app_mode == "Add New Face":
        add_new_face()
    elif app_mode == "View Records":
        view_attendance_records()

# --- Close Database Connection ---
conn.close()
