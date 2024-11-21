import cv2
import numpy as np
import cvzone
import pickle

# Global variables
image_path = './upload_folder/12345/12345.jpeg'
park_spots_file = "upload_folder/12345/parkspots"

# Loading the image
image = cv2.imread(image_path)

# Initializing variables for drawing
drawing = False
area_names = []
polylines = []
points = []
current_name = " "

# Try to load existing parking spot data if available
try:
    with open(park_spots_file, "rb") as f:
        data = pickle.load(f)
        polylines, area_names = data['polylines'], data['area_names']
except FileNotFoundError:
    pass


def draw(event, x, y, flags, params):
    global points, drawing, area_names, polylines, current_name
    if event == cv2.EVENT_LBUTTONDOWN:
        # Start a new line and set drawing flag to true
        points = [(x, y)]
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        # Add point to line while moving the mouse
        points.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        # Stop drawing on mouse button release
        drawing = False
        # Input name for the area
        current_name = input('area-name: ')
        if current_name:
            # Add area name to list and add line to list
            area_names.append(current_name)
            polylines.append(np.array(points, np.int32))


def main():
    global points
    while True:
        # Resize image for display
        frame = cv2.resize(image, (1020, 500))

        # Draw all lines and area names that are saved
        for i, polyline in enumerate(polylines):
            cv2.polylines(frame, [polyline], True, (225, 0, 147), 2)
            cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)

        # Draw temporary points while drawing a line to help the user
        for point in points:
            cv2.circle(frame, point, 2, (255, 0, 147), -1)

        # Display the frame
        cv2.imshow('FRAME', frame)

        # Call draw function on the frame for mouse events
        cv2.setMouseCallback('FRAME', draw)

        # Wait for a key press
        key = cv2.waitKey(100) & 0xFF
        if key == ord('s'):
            # Save the drawn lines and area names as parkspots
            with open(park_spots_file, "wb") as f:
                data = {'polylines': polylines, 'area_names': area_names}
                pickle.dump(data, f)

        # Exit the loop if 'q' is pressed
        elif key == ord('q'):
            break

    # Close all OpenCV windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()