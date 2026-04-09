from ultralytics import YOLO
import cv2
import easyocr
import re
import time

from src.database.db import vehicle_entry, vehicle_exit
from src.parking.manager import ParkingManager

# 🔥 USER INPUT
total_slots = int(input("Enter total parking slots: "))
manager = ParkingManager(total_slots)

# Load models
model = YOLO("yolov8n.pt")
reader = easyocr.Reader(['en'], gpu=False)

# Vehicle classes
vehicle_classes = ["car", "motorcycle", "bus", "truck"]

# Camera
cap = cv2.VideoCapture(0)

# 🔥 NEW SYSTEM VARIABLES
plate_buffer = {}              # multi-frame validation
FRAME_THRESHOLD = 3            # must detect 3 times
last_processed_time = {}       # cooldown tracking
COOLDOWN = 5                  # seconds

# Indian plate regex
plate_pattern = r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{3,4}$'

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)[0]

    for box in results.boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]

        if label in vehicle_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw vehicle box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # 🔥 Plate region (bottom 40%)
            crop_y1 = int(y2 - (y2 - y1) * 0.4)
            plate_region = frame[crop_y1:y2, x1:x2]

            if plate_region.size > 0:
                # 🔥 Better preprocessing
                gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray, 11, 17, 17)
                _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
                thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

                # OCR
                results_ocr = reader.readtext(thresh)

                for (bbox, text, prob) in results_ocr:
                    if prob < 0.5:
                        continue

                    text = text.strip().upper()
                    text = re.sub(r'[^A-Z0-9]', '', text)

                    # 🔥 STRICT FILTER
                    if not re.match(plate_pattern, text):
                        continue

                    # 🔥 MULTI-FRAME VALIDATION
                    plate_buffer[text] = plate_buffer.get(text, 0) + 1

                    if plate_buffer[text] >= FRAME_THRESHOLD:

                        current_time = time.time()

                        # 🔥 COOLDOWN CHECK
                        if text in last_processed_time:
                            if current_time - last_processed_time[text] < COOLDOWN:
                                continue

                        print("\n✅ FINAL Plate Detected:", text)

                        # ENTRY / EXIT
                        if text not in manager.occupied:
                            slot = manager.assign_slot(text)

                            if slot is None:
                                print("❌ Parking Full!")
                            else:
                                vehicle_entry(text, slot)
                                print(f"✅ Assigned Slot: {slot}")

                        else:
                            slot = manager.release_slot(text)
                            vehicle_exit(text)
                            print(f"🚪 Freed Slot: {slot}")

                        # Update cooldown
                        last_processed_time[text] = current_time

                        # Reset buffer
                        plate_buffer = {}

                    # Display text
                    cv2.putText(frame, text, (x1, y1 - 40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 0, 255), 2)

                cv2.imshow("Processed Plate", thresh)

    cv2.imshow("Smart Parking System", frame)

    # 🔥 Slight delay → improves stability
    time.sleep(0.3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()