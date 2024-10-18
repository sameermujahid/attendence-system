import os
import cv2
import pandas as pd
import datetime
from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

app = Flask(__name__)

# Load the YOLOv8 model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'best.pt')  # Replace with your model path
model = YOLO(model_path)

# Brevo API Configuration
api_key = 'your_api_key_here'  # Replace with your actual API key
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = api_key

# Dictionary to keep track of recognized names and their timestamps
recognized_names = {}
deadline = "09:00"  # Default deadline time

# Function to send email notification using Brevo
def send_brevo_notification(subject, content):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": "Attendance System", "email": "your_email@example.com"}
    to = [{"email": "recipient_email@example.com"}]  # Replace with actual recipient email
    html_content = f"<html><body>{content}</body></html>"

    email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=subject,
        html_content=html_content
    )

    try:
        api_response = api_instance.send_transac_email(email)
        print(f"Email sent: {api_response}")
    except ApiException as e:
        print(f"Error sending email: {e}")

# Function to log attendance
def log_attendance(name, timestamp):
    formatted_time = timestamp.strftime("%H:%M:%S")
    formatted_date = timestamp.strftime("%d-%m-%Y")
    if name not in recognized_names:
        recognized_names[name] = {"time": formatted_time, "date": formatted_date, "late": formatted_time > deadline}

# Video streaming generator
def generate_frames(camera_index):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame)
        names_in_frame = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                name = model.names[cls]
                names_in_frame.append(name)

                label = f"{name}: {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        for name in set(names_in_frame):
            log_attendance(name, datetime.datetime.now())

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_attendance', methods=['GET'])
def get_attendance():
    return jsonify(recognized_names)

@app.route('/send_attendance', methods=['POST'])
def send_attendance():
    if recognized_names:
        attendance_list_html = "<br>".join(f"{name} - Time: {info['time']} | Date: {info['date']} | Late: {info['late']}"
                                            for name, info in recognized_names.items())
        email_content = f"<h1>Attendance List</h1><ul>{attendance_list_html}</ul>"
        send_brevo_notification("Attendance List", email_content)
        return {"message": "Attendance list sent successfully!"}, 200
    else:
        return {"message": "No attendees to send."}, 400

@app.route('/export_attendance', methods=['POST'])
def export_attendance():
    if recognized_names:
        # Create a DataFrame from the recognized_names dictionary
        attendance_data = []
        for name, info in recognized_names.items():
            attendance_data.append({
                "Name": name,
                "Time": info['time'],
                "Date": info['date'],
                "Late": info['late']
            })

        attendance_df = pd.DataFrame(attendance_data)

        # Specify the filename and export it to Excel
        filename = f"attendance_{datetime.datetime.now().strftime('%Y-%m-%d')}.xlsx"
        attendance_df.to_excel(filename, index=False)

        return {"message": f"Attendance list saved as {filename}."}, 200
    else:
        return {"message": "No attendees to export."}, 400

if __name__ == '__main__':
    app.run(debug=True)
