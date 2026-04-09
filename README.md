# 🚗 AI Smart Parking System (ALPR)

An AI-powered Smart Parking System that uses **Automatic License Plate Recognition (ALPR)** to detect vehicles, assign parking slots, and manage entry/exit with billing.

---

## 🔥 Features

* 🚘 Vehicle Detection using YOLOv8
* 🔍 License Plate Recognition using EasyOCR
* 🅿️ Automatic Parking Slot Allocation
* ⏱ Entry & Exit Time Tracking
* 💰 Automatic Billing System
* 📊 Real-time Dashboard (Streamlit)

---

## 🛠 Tech Stack

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* EasyOCR
* SQLite
* Streamlit

---

## 📁 Project Structure

smart-parking-alpr/
│
├── app/              # Dashboard (Streamlit)
├── src/
│   ├── detection/   # YOLO + camera logic
│   ├── database/    # DB handling
│   ├── parking/     # Slot allocation logic
│
├── requirements.txt
└── README.md

---

## 🚀 How to Run

### 1. Clone repo

git clone https://github.com/ankitrajqqq-rgb/smart-parking-alpr.git
cd smart-parking-alpr

### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run detection system

python src/detection/yolo_detect.py

### 5. Run dashboard

streamlit run app/dashboard.py

---

## ⚠️ Note

* Model weights (.pt) are not included due to size limits
* Database file is generated automatically

---

## 💡 Future Improvements

* Custom trained license plate model
* Multi-camera support
* Cloud deployment
* Mobile app integration

---

## 👨‍💻 Author

Ankit Raj
