from deepface import DeepFace
import cv2
import os
import requests
import datetime

KNOWN_FACES_DIR = "employee_pics"
WEBHOOK_URL = "https://pree.app.n8n.cloud/webhook-test/attendance"

# Load employee faces
employee_db = {}
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        employee_id = os.path.splitext(filename)[0]
        employee_db[employee_id] = os.path.join(KNOWN_FACES_DIR, filename)

# Start webcam
video_capture = cv2.VideoCapture(0)
print("Camera started. Press 'q' to quit.")

last_sent_time = {}

while True:
    ret, frame = video_capture.read()
    if not ret: break

    cv2.imwrite("current_frame.jpg", frame)

    try:
        result_df = DeepFace.find(
            img_path="current_frame.jpg",
            db_path=KNOWN_FACES_DIR,
            enforce_detection=False,
            detector_backend='opencv',
            silent=True
        )

        if len(result_df) > 0 and len(result_df[0]) > 0:
            best_match_path = result_df[0].iloc[0]["identity"]
            matched_id = os.path.splitext(os.path.basename(best_match_path))[0]

            now = datetime.datetime.now()
            last_time = last_sent_time.get(matched_id)

            if not last_time or (now - last_time).total_seconds() > 300:
                last_sent_time[matched_id] = now

                data = {
                    "employee_id": matched_id,
                    "timestamp": str(now)
                }

                try:
                    response = requests.post(WEBHOOK_URL, json=data)
                    print(f"Sent to n8n: {matched_id} – {response.status_code}")
                except Exception as e:
                    print(f"Failed to send data for {matched_id}: {e}")

    except Exception as e:
        print(f"Face match error: {e}")

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

# Cleanup
if os.path.exists("current_frame.jpg"):
    os.remove("current_frame.jpg")
