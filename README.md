The python programs require the following libraries to be imported:
-os
-shutil
-math
-random

Instructions for cleaning the Yolov8 data:
1. Find and delete the two images in the 'coco128' folder that do not have corresponding labels.
2. Find and delete the two labels in the 'coco128' folder that do not have corresponding images.

Instructions for adding new images to the Yolov8 data:
1. Download and use the labelling tool from 'https://github.com/ivangrov/ModifiedOpenLabelling'.
2. Run the 'run.py' program and draw boxes around the person or object of interest.
3. Modify the files in the 'bbox_txt' folder to reflect the new class numbers (in our case starting from 80).

Instructions for splitting the Yolov8 data:
1. Make sure the 'train2017' folder is placed inside the 'ee104_val' folder in both the images and labels folders.
2. Run the 'yolov8_ee104_split_train_val_files.py' program to create an 80/20 split in training and validation.

Instructions for training the Yolov8 model:
yolo task=detect mode=train data=C:/Users/USERNAME/datasets/coco128/coco128_ee104.yaml model=yolov8n.pt epochs=100

Instructions for predicting with the Yolov8 model:
yolo task=detect mode=predict model=C:/Users/USERNAME/ultralytics/runs/detect/train/weights/best.pt source=0 show=True

Instructions for using the dragons.py program:
1. Run the game from the command prompt.
2. Use the arrow keys to move Hero 1.
3. Use the 'WASD' keys to move Hero 2.
4. Win the game by collecting 50 eggs.
5. Lose the game by colliding with dragons 3 times.
