import time
import os
import io
import requests
from threading import Thread
from picamera2 import Picamera2
from io import BytesIO

def capture_save_and_send():
    cap = Picamera2(0)
    cap.start()

    cap.resolution = (1024, 768)
    print("print 0")
    time.sleep(1)

    while True:
        try:
            print("print 1")

            # Capture a single frame
            stream = io.BytesIO()
            print("io bytes")

            cap.capture_file(stream, format='jpeg')
            print("print 2")

            stream.seek(0)
            image_data = stream.read()
            print("print 3")

            # Generate a random 5-digit lot ID
            lot_id = '12345' 

            # Send the image as a POST request to the specified URL
            server_url = 'http://192.168.1.3:8000/upload'
            files = {'image': (f'{lot_id}.jpeg', image_data, 'image/jpeg')}
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
