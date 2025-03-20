# Face and Emotion Recognition Attendance System

## Overview
This project is a **Face and Emotion Recognition-based Attendance System** built with **Streamlit**, **OpenCV**, **Face Recognition**, **Keras**, and **SQLite**. It captures real-time face and emotion data to automatically mark attendance with emotional state detection.

## Features
- **Face Recognition**: Identifies registered faces.
- **Emotion Detection**: Recognizes six emotions (angry, fear, happy, neutral, sad, surprise).
- **Attendance Marking**: Automatically records attendance along with detected emotion.
- **Database Storage**: Uses **SQLite** for storing attendance records.
- **Real-time Emotion Detection**: Displays detected emotions from webcam feed.
- **New Face Registration**: Users can add their face to the system.
- **View Attendance Records**: View past attendance with names, timestamps, and emotions.

## Installation
### Prerequisites
Ensure you have **Python 3.8+** installed and the required dependencies.

### Clone the Repository
```sh
git clone https://github.com/lovnishverma/REALTIMEFACEANDEMOTIONDETECTION.git
cd REALTIMEFACEANDEMOTIONDETECTION
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage
### Run the Application
```sh
streamlit run app.py
```

### Application Modes
- **Recognize Face & Emotion**: Captures a face image, detects emotion, and marks attendance.
- **Add New Face**: Allows new users to register their face.
- **Real-time Emotion Detection**: Detects emotions continuously from a live webcam feed.
- **View Records**: Displays stored attendance records.
- **Real-time Emotion and Face Recognition**: Automatically recognizes faces and emotions while marking attendance.

## File Structure
```
├── Photos/                 # Folder containing registered face images
├── app.py                  # Main application file
├── CNN_Model_acc_75.h5     # Pre-trained CNN model for emotion recognition
├── attendance.db           # SQLite database for storing attendance records
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

## Database Schema (SQLite)
| Column  | Type    | Description |
|---------|--------|-------------|
| id      | INTEGER | Auto-incremented primary key |
| name    | TEXT    | Recognized name |
| roll_no | TEXT    | Unique roll number |
| date    | TEXT    | Date of attendance |
| time    | TEXT    | Time of recognition |
| status  | TEXT    | Attendance status ('Present') |
| emotion | TEXT    | Detected emotion |

## Requirements
Install required libraries using:
```sh
pip install -r requirements.txt
```
## How to run
Open terminal enter:
```sh
streamlit run app.py
```

![WhatsApp Image 2025-03-20 at 11 12 53 AM](https://github.com/user-attachments/assets/a55c8959-c8ea-4f62-9ec7-b00a536ac94c)



## Troubleshooting
- **Face Not Recognized?** Ensure your image is clear and well-lit.
- **Emotion Detection Incorrect?** The model works best under consistent lighting.
- **Database Errors?** Ensure `attendance.db` is not locked by another process.

## Author
**Lovnish Verma**  
GitHub: [lovnishverma](https://github.com/lovnishverma)

## License
This project is open-source under the MIT License.
