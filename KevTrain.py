#Beta for KevTrain

import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Variables for counting reps
reps = 0
stage = None  # 'up' or 'down'

# Video feed
cap = cv2.VideoCapture(0)  # Use webcam

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(frame_rgb)

    # Draw landmarks
    mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    if result.pose_landmarks:
        # Example: Track elbow and shoulder for a bicep curl
        landmarks = result.pose_landmarks.landmark
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

        # Calculate the angle (simplified example)
        angle = calculate_angle(left_shoulder, left_elbow, left_wrist)  # Custom function

        # Repetition logic
        if angle > 160:
            stage = "down"
        if angle < 30 and stage == "down":
            stage = "up"
            reps += 1

    # Display the rep count
    cv2.putText(frame, f'Reps: {reps}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Workout Tracker', frame)

    # Break on 'q' key
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()