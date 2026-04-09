import cv2

# Step 1: Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

while True:
    # Step 2: Read frame from camera
    ret, frame = cap.read()

    # If frame not captured properly
    if not ret:
        print("Failed to grab frame")
        break

    # Step 3: Show the frame
    cv2.imshow("Live Camera Feed", frame)

    # Step 4: Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Step 5: Release camera & close windows
cap.release()
cv2.destroyAllWindows()