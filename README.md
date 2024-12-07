## SmartPark Backend

This repository is the backend portion of the SmartPark project. The frontend repository can be found [here](https://github.com/ParjanAmeen/SmartPark-FrontEnd). The system uses a Raspberry Pi 4 to take a picture every 30 seconds and sends it to a Flask server. The server analyzes the photo to check if a vehicle is occupying the designated parking spots. This data is stored in a JSON file and sent to the frontend, which displays the parking lot data via an app.

### Install Required Packages on Your Computer

You will need to run the `computer-package-install.py` script to install the necessary packages. Below is the command to run the script:

```sh
python computer-package-install.py
```

•After that you will need to set up your raspberry pi and be able to ssh into it. You only need to put the camera.py and pi-package-install.py on the pi itself. Also make sure the rp camera module is securely connected and you will have to enable raspberry pi in the pi’s setting. You will need to run the `pi-package-install.py` script to install the necessary packages on the pi. Below is the command to run the script:

```sh
python pi-package-install.py
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

•Now run camera.py. This will run forever as it keeps taking an image every 30 seconds and sends it to the flask server we have running
