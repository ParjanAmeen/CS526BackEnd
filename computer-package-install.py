import subprocess
import pkg_resources
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required = {
    'opencv-python': 'cv2',
    'numpy': 'numpy',
    'cvzone': 'cvzone',
    'pickle': 'pickle',
    'pandas': 'pandas',
    'yolov8': 'ultralytics.YOLO',
    'json': 'json',
    'flask': 'flask',
    'os': 'os'
}
installed = {pkg.key for pkg in pkg_resources.working_set}

for package, import_name in required.items():
    try:
        __import__(import_name)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found, installing now.")
        install(package)

print("All packages are installed.")