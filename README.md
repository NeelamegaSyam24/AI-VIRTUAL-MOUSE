# 🖐️ AI Virtual Mouse (AI Gesture OS)

AI Virtual Mouse is a real-time gesture-based desktop control system built using Python, MediaPipe, and OpenCV.  
It allows users to control their computer using hand gestures through a webcam — without touching the mouse.

---

## 🎯 Features

- 👆 Index Finger → Cursor Movement
- 👍 Thumb Only → Click
- ✌️ Two Fingers → Volume Up
- 🖖 Four Fingers → Volume Down
- ✋ Five Fingers → Scroll Up
- 👊 Closed Fist → Scroll Down
- 📌 Always-On-Top Webcam Window
- 🚀 Splash Screen on Startup
- 🎨 Custom App Icon
- 📦 Packaged as Standalone Windows EXE

---

## 🧠 How It Works

1. Webcam captures real-time video.
2. MediaPipe detects 21 hand landmarks.
3. Gesture logic interprets finger positions.
4. PyAutoGUI performs OS-level actions.
5. Smooth cursor mapping ensures stable control.

---

## 🛠 Tech Stack

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- Tkinter (Splash Screen)
- PyInstaller (EXE Packaging)

---

## 📂 Project Structure
