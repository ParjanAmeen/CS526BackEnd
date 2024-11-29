## How-to-run:

1. Start by cloning the CS526BackEnd repo from GitHub.
2. Next, cd into the CS526BackEnd repo.

### Install Required Packages on Your Computer

You will need to pip install a couple of things to be able to run the code. Below is a list of packages you will need to install:

```sh
pip install cv2
pip install numpy
pip install cvzone
pip install pickle
pip install pandas
pip install ultralytics
pip install json
pip install flask
pip install os
```


•After that you will need to set up your raspberry pi and be able to ssh into it. You only need to put the testing_webcam.py on the pi itself. Also make sure the rp camera module is securely connected and you will have to enable raspberry pi in the pi’s setting. Below is the list of packages you will need to install on the pi

```sh
pip install time
pip install os
pip install io
pip install requests
pip install threading
pip install picamera2
pip install io
```

•Next after positioning the pi camera at a parking lot you will want to take an initial image by running the following in a terminal:

```sh
libcamera-still -o 12345.jpeg”
```

•Next take that image and place it your backend repo directory on your laptop in upload_folder/12345. You will see a 12345.jpeg already in there as we pushed that code but the 12345 directory and the images would be created when running the server.py code. They need to be there initially for the next part to run. You only need to do this once

•Next run DefineParkingSpaces.py and your image taken with the pi will pop up as a screen and you can now draw parking spaces with your mouse and as you draw make sure to hold your left mouse button as you draw. As soon as you let go of the left mouse button the shape you drew will try to connect and in your terminal it will ask you to name the parking space. Please give it a number. Then move on to your next drawing. 

•After you have finished your drawing click the ‘s’ button on your keyboard and a file called parkspots will show up in upload_folder/12345. This file is then used in main.py to detect if a space is occupied. 

•You do not run main.py your next step is to run server.py and retrieve the link that is produced in the terminal

•Take that link and past it in the testing_webcam.py located on your pi

•Now run testing_webcam.py. This will run forever as it keeps taking an image every 30 seconds and sends it to the flask server we have running
