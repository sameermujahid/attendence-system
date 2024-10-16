
# Attendance System using YOLOv8
## Project Overview

The **Attendance System Using YOLOv8** is a Flask-based web application that leverages computer vision techniques to automatically recognize individuals and maintain attendance records. This project utilizes the YOLOv8 (You Only Look Once) object detection model to identify faces in video streams. It is designed to simplify attendance tracking in various settings, such as classrooms or corporate environments.

The application captures video feeds from a webcam, processes each frame to detect individuals, and records their attendance based on recognized faces. The recorded attendance data can be emailed to designated recipients and exported as an Excel file for further analysis.

## Key Features

- **Real-time Face Detection**: Uses YOLOv8 to detect and recognize individuals in video streams.
- **Attendance Logging**: Automatically logs attendance, capturing the time and date for each individual.
- **Email Notifications**: Sends attendance lists via email using the Brevo (formerly Sendinblue) API.
- **Excel Export**: Exports attendance data to an Excel file for easy sharing and reporting.
- **User-Friendly Interface**: A simple and intuitive web interface for interaction.

## Folder Structure

Here’s the folder structure for the project:

```
attendance_system/
│
├── app.py                  # Main application script
├── best.pt                 # Trained YOLOv8 model weights
├── requirements.txt        # Required Python packages
├── templates/              # HTML templates for the Flask application
│   └── index2.html         # Main page of the attendance system
├── dataset/                # Directory for the custom dataset
│   ├── person1/            # Folder for each individual
│   │   ├── img1.jpg        # Training image
│   │   ├── img2.jpg        # Training image
│   │   └── ...
│   ├── person2/
│   └── ...
│
├── processed_dataset/      # Processed dataset for YOLOv8 training
│   ├── train/              # Training images and labels
│   │   ├── images/
│   │   ├── labels/
│   │   └── ...
│   ├── val/                # Validation images and labels
│   │   ├── images/
│   │   ├── labels/
│   │   └── ...
│   └── ...
│
└── README.md               # Project documentation
```
## Technologies Used

- Python
- Flask
- OpenCV
- YOLOv8
- Pandas
- Brevo API for email notifications
- HTML/CSS for front-end development
- JavaScript (jQuery) for asynchronous operations

## Installation

To set up the Attendance System on your local machine, follow these instructions:

### Prerequisites

- Python
- pip

### Steps to Install

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd attendance-system-yolov8
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download YOLOv8 Model**:
   Place your trained model `best.pt` in the project directory.

5. **Set Up Brevo API**:
   - Sign up for a Brevo account.
   - Obtain your API key and update it in the code.

6. **Run the Application**:
   ```bash
   python app.py
   ```

7. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

Once the application is running, you can use it as follows:

1. **Webcam Access**: Grant permission for the application to access your webcam.
2. **Attendance Capture**: The system will automatically capture frames every few seconds, processing them to detect and recognize faces.
3. **Send Attendance**: Click the "Send Attendance" button to email the attendance list.
4. **Export Attendance**: Click the "Export Attendance" button to download the attendance data in Excel format.

## Dataset Preparation

To achieve accurate attendance recognition, a custom dataset was created as follows:

1. **Folder Structure**:
   - Create a folder for each individual to be recognized, named after their respective identity.
   - Inside each folder, include multiple images of the individual under various lighting conditions and angles.
   Example:
   ```
   dataset/
   ├── person1/
   │   ├── img1.jpg
   │   ├── img2.jpg
   │   └── ...
   ├── person2/
   └── ...
   ```
2. **Processing Dataset**:
   - The dataset was processed using an existing YOLOv8 implementation to generate the necessary annotations for training.
   - The processed dataset consists of two main splits: training and validation.
   Example of processed dataset structure:
   ```
   processed_dataset/
   ├── train/
   │   ├── images/
   │   ├── labels/
   ├── val/
   │   ├── images/
   │   ├── labels/
   └── ...
   ```
3. **Training the YOLOv8 Model**:
   - Using the processed dataset, the YOLOv8 model was trained to recognize the individuals.
   - The best model weights were saved as `best.pt`.

## Model Training

The training process involved the following steps:

1. **Loading the Dataset**: The processed dataset containing images and annotations was loaded.
2. **Model Configuration**: Configured the YOLOv8 training parameters, including batch size, learning rate, and epochs.
3. **Training Execution**: Initiated the training process, monitoring for performance metrics such as loss and accuracy.
4. **Model Evaluation**: Evaluated the model on the validation set to ensure it generalizes well to unseen data.
5. **Model Saving**: Upon successful training, the model was saved as `best.pt` for deployment in the application.

## Acknowledgments

- **YOLOv8**: For providing a robust object detection framework.
- **Flask**: For enabling easy web application development.
- **OpenCV**: For handling video processing and image manipulation.
- **Brevo API**: For facilitating email notifications.
- **Pandas**: For managing attendance data and exporting to Excel.

## Future Enhancements

- **Mobile Application**: Consider developing a mobile app for attendance tracking.
- **Improved UI/UX**: Enhance the web interface for better user experience.
- **Additional Features**: Implement facial recognition for more advanced attendance management, including features like automatic reminders for attendance.
