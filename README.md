# 🎓 AI Face Attendance System

A modern, desktop-based Face Recognition Attendance System built with Python. Designed to automate the attendance process for institutions using facial recognition, completely replacing manual roll calls. 

This project features a clean, highly responsive dashboard built with `CustomTkinter` and utilizes `OpenCV` for robust face detection and recognition.

---

## ✨ Features

- **Modern Dashboard:** A sleek, dark-themed UI built with `CustomTkinter` that is easy to navigate.
- **Live Statistics & Charts:** Visualizes total students, today's attendance rate, and weekly trends dynamically using `Matplotlib`.
- **Face Registration & Training:** Easily add new students, capture their facial data via webcam, and train the local recognition model on the fly.
- **Automated Logging:** Recognizes faces in real-time and logs the attendance (Time, ID, Name, Class, Status).
- **Data Management:** Search, filter, and manage student records and attendance logs directly from the app. Data is persistently stored in lightweight CSV format.

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Computer Vision:** OpenCV (`cv2`)
- **GUI Framework:** CustomTkinter & Tkinter
- **Data Analytics/Visualization:** Matplotlib, Pandas (optional based on local environment)
- **Database:** Local CSV Files (`attendance.csv`, `students.csv`)

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/FaceAttendance.git
   cd FaceAttendance
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install opencv-python customtkinter matplotlib
   ```
   *(Note: Ensure you have `pillow` installed if you face any image rendering issues in CustomTkinter)*

3. **Run the Application:**
   Launch the main dashboard:
   ```bash
   python dashboard.py
   ```

---

## 💻 How to Use

1. **Add a Student:** Navigate to the **Students** tab, click **Add Student**, and enter their ID, Name, and Class.
2. **Register Face:** Go to the **Quick Actions** section on the dashboard (or the corresponding menu) and select **Register New Face**. The webcam will open and capture 50-100 sample frames of the student's face.
3. **Train Model:** Once faces are registered, click **Train Model**. This processes the captured images and updates the `trainer.yml` file.
4. **Take Attendance:** Click **Start Camera** on the dashboard. The system will scan faces through the webcam and mark them as "Present" in today's attendance log.

---

## 📁 Project Structure

- `dashboard.py`: Main entry point containing the UI and dashboard logic.
- `attendance_recognize.py`: Script handling the webcam feed and live face matching.
- `register_face.py`: Captures training images of students via webcam.
- `train_model.py`: Generates the `trainer.yml` LBPH face recognizer model.
- `theme.py`: UI styling, colors, and font configurations.
- `attendance_utils.py` / `student_utils.py`: Helper functions for managing CSV data.
- `faces/`: Directory where captured sample images are temporarily saved.
- `trainer.yml`: The trained facial recognition model.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
