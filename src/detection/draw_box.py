import cv2

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot read frame")
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Draw rectangle (x1, y1) to (x2, y2)
    cv2.rectangle(frame, (100, 100), (400, 300), (0, 255, 0), 2)

    # Add text
    cv2.putText(frame, "Demo Box", (100, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Detection Demo", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()