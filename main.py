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

