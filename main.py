import cv2
import pickle
import pandas as pd
from ultralytics import YOLO
import cvzone
import json

# Constants and file paths
coco_classes_file = "coco.txt"
yolo_model = 'yolov8s.pt'

# Load the COCO classes
with open(coco_classes_file, "r") as file:
    class_list = file.read().split("\n")

# Load the YOLO model
model = YOLO(yolo_model)


def process_frame(frame):

    results = model.predict(frame)

    boxes = pd.DataFrame(results[0].boxes.data).astype("float")

    totalVehicles_set = set()

    # Iterate through the detected objects
    for _, row in boxes.iterrows():

        x1, y1, x2, y2 = map(int, row[:4])


        class_id = int(row[5])

        # Get the class name
        class_name = class_list[class_id]

        if 'car' in class_name or 'bus' in class_name or 'truck' in class_name:
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Draw a bounding box around the detected object
            totalVehicles_set.add((cx, cy))

    return frame, totalVehicles_set


def ProduceOutput(lot_id):
    imagepath = f'./upload_folder/{lot_id}/{lot_id}.jpeg'
    image = cv2.imread(imagepath)
    # Load parking spot data
    with open(f'./upload_folder/{lot_id}/parkspots', "rb") as f:
        data = pickle.load(f)
        lines, spaceName = data['polylines'], data['area_names']

    frame = cv2.resize(image, (1020, 500))
    processed_frame, vehicle_coordinates = process_frame(frame.copy())
    occupied_count = 0
    occupied_spots = []
    free_spots = []

    for i, polyline in enumerate(lines):

        # Draw parking spot lines
        cvzone.putTextRect(processed_frame, f'{spaceName[i]}', tuple(polyline[0]), 1, 1)
        cv2.polylines(processed_frame, [polyline], True, (0, 255, 0), 2)

        found = False
        for cx, cy in vehicle_coordinates:
            if cv2.pointPolygonTest(polyline, (cx, cy), False) == 1:
                occupied_spots.append(spaceName[i])

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
