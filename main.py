import cv2
import pickle
import pandas as pd
from ultralytics import YOLO
import cvzone
import json

# Constants and file paths
coco_classes_file = "coco.txt"
yolo_model = 'yolov8s.pt'

# Load class names for object detection
with open(coco_classes_file, "r") as file:
    class_list = file.read().split("\n")

# Initialize YOLO model for object detection
model = YOLO(yolo_model)


def process_frame(frame):
    # Predict objects in the frame using the YOLO model
    results = model.predict(frame)

    # Convert the results to a DataFrame for easier processing
    # 'boxes' will contain the coordinates and class IDs of detected objects
    boxes = pd.DataFrame(results[0].boxes.data).astype("float")

    # Initialize a set to store coordinates of detected vehicles
    # We had trouble where a vehicle was being counted twice
    totalVehicles_set = set()

    # Iterate through each detected object
    for _, row in boxes.iterrows():
        # Extract the coordinates of the bounding box and convert the coordinates to integers
        x1, y1, x2, y2 = map(int, row[:4])

        # Get the class ID of the detected object and convert class ID to integer
        class_id = int(row[5])

        # Retrieve the class name using the class ID
        class_name = class_list[class_id]

        # Check if the detected object is a vehicle (car, bus, or truck)
        # and add its center coordinates to the totalVehicles_set
        if 'car' in class_name or 'bus' in class_name or 'truck' in class_name:
            # Calculate the center coordinates of the bounding box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Add the center coordinates to the set
            totalVehicles_set.add((cx, cy))

    return frame, totalVehicles_set


# Main function
def ProduceOutput(lot_id):
    imagepath = f'./upload_folder/{lot_id}/{lot_id}.jpeg'
    image = cv2.imread(imagepath)
    # Load parking spot data
    with open(f'./upload_folder/{lot_id}/parkspots', "rb") as f:
        data = pickle.load(f)
        lines, spaceName = data['polylines'], data['area_names']

    # Resize the image for display
    frame = cv2.resize(image, (1020, 500))
    processed_frame, vehicle_coordinates = process_frame(frame.copy())
    occupied_count = 0
    occupied_spots = []
    free_spots = []
    # Loop through each parking spot to check occupancy
    for i, polyline in enumerate(lines):

        # Draw parking spot lines
        cvzone.putTextRect(processed_frame, f'{spaceName[i]}', tuple(polyline[0]), 1, 1)
        cv2.polylines(processed_frame, [polyline], True, (0, 255, 0), 2)

        found = False
        # Check if any vehicle is within the parking spot and highlight occupied spots
        for cx, cy in vehicle_coordinates:
            if cv2.pointPolygonTest(polyline, (cx, cy), False) == 1:
                occupied_spots.append(spaceName[i])

                # Highlight occupied spots and increment count of occupied spaces
                cv2.polylines(processed_frame, [polyline], True, (0, 0, 225), 2)
                occupied_count += 1
                found = True

        if not found:
            free_spots.append(spaceName[i])

    total_spaces = len(lines)

    file_data = {
        'total_spaces': total_spaces,
        'occupied_spots': occupied_spots,
        'free_spots': free_spots
    }

    
    with open(f'upload_folder/{lot_id}/out/parking_status.json', 'w') as json_file:
        json.dump(file_data, json_file)

    cv2.imwrite(f'upload_folder/{lot_id}/out/{lot_id}.jpeg', image)
