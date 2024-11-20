import cv2
import time
import os
import requests
from threading import Thread

# Might have to import the pi camera library cuz this is if a webcam is connected to it

def capture_save_and_send():
    while True:
        try:
            # Open the default camera
            cap = cv2.VideoCapture(0)

            # Check if the camera opened successfully
            if not cap.isOpened():
                raise Exception("Error: Unable to open the camera.")

            # Capture a single frame
            ret, frame = cap.read()

            # Check if the frame was captured successfully
            if not ret:
                raise Exception("Error: Unable to capture a frame.")

            # Release the camera
            cap.release()

            # Generate a random 5-digit lot ID
            lot_id = '12345' 

            # Send the image as a POST request to the specified URL
            server_url = 'http://192.168.1.3:8000/upload'
            _, buffer = cv2.imencode('.png', frame)
            image_data = buffer.tobytes()
            files = {'image': ('image.png', image_data, 'image/png')}
            headers = {'lotID': lot_id}

            response = requests.post(server_url, files=files, headers=headers)

            if not response.ok:
                raise Exception(f"Error: Request failed with status code {response.status_code}.")

            print(f"Image sent to server: {server_url}")

        except Exception as e:
            print(f"Error: {e}")

        # Sleep for 30 seconds before capturing the next image
        time.sleep(30)

if __name__ == '__main__':

    capture_thread = Thread(target=capture_save_and_send)
    capture_thread.start()

    while True:
        pass
