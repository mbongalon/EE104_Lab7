#!/usr/bin/env python
# coding: utf-8
# By Christopher Pham


import os
from random import choice
import shutil

#Create empty arrays to store file names
imgs =[]
xmls =[]


#You should already have these two folders from your download:
# C:/yolov5/datasets/coco128/images/train2017
# C:/yolov5/datasets/coco128/labels/train2017

#Now you must manually create the followings sub-directories if they are not already existing:
# The code below will split the train2017 into 80% to the ee104_train directory
#  and 20% into the ee104_val directory.
# trainImagePath = 'C:/yolov5/datasets/coco128/images/ee104_train' 
#   valImagePath = 'C:/yolov5/datasets/coco128/images/ee104_val'
# trainLabelPath = 'C:/yolov5/datasets/coco128/labels/ee104_train' 
#   valLabelPath = 'C:/yolov5/datasets/coco128/labels/ee104_val'


#setup dir names
##IMPORTANT NOTE: If you will add more images and labels later, the number of files in train/val directory pairs must match.
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

ee104TrainImagePath = '.\\coco128\\images\\ee104_train'
ee104TrainLabelPath = '.\\coco128\\labels\\ee104_train'
ee104ValImagePath = '.\\coco128\\images\\ee104_val'
ee104ValLabelPath = '.\\coco128\\labels\\ee104_val'

coco_images = f'{ee104ValImagePath}\\train2017' #dir where downloaded images are stored
coco_labels = f'{ee104ValLabelPath}\\train2017' #dir where downloaded annotations txt files are stored

#setup ratio (val ratio = rest of the files in origin dir after splitting into train and test)
train_ratio = 0.8
val_ratio = 0.2


#total count of imgs
totalImgCount = len(os.listdir(coco_images))
print("Total number of COCO images are : ",totalImgCount)

#storing files to corresponding arrays
for (dirname, dirs, files) in os.walk(coco_images):
    for filename in files:
        if filename.endswith('.jpg'):
            imgs.append(filename)
for (dirname, dirs, files) in os.walk(coco_labels):
    for filename in files:
        if filename.endswith('.txt'):
            xmls.append(filename)


#counting range for cycles
countForTrain = int(len(imgs)*train_ratio)
countForVal = int(len(imgs)*val_ratio)
print("Number of training images are   : ",countForTrain)
print("Number of validation images are : ",countForVal)


#cycle for train dir
for x in range(countForTrain):

    fileJpg = choice(imgs) # get name of random image from origin dir
    fileXml = fileJpg[:-4] +'.txt' # get name of corresponding annotation file

    shutil.copy(os.path.join(coco_images, fileJpg), os.path.join(ee104TrainImagePath, fileJpg))
    shutil.copy(os.path.join(coco_labels, fileXml), os.path.join(ee104TrainLabelPath, fileXml))


    #remove files from arrays
    imgs.remove(fileJpg)
    xmls.remove(fileXml)


#cycle for val dir   
for x in range(countForVal):

    fileJpg = choice(imgs) # get name of random image from origin dir
    fileXml = fileJpg[:-4] +'.txt' # get name of corresponding annotation file

    #move both files into train dir
    shutil.copy(os.path.join(coco_images, fileJpg), os.path.join(ee104ValImagePath, fileJpg))
    shutil.copy(os.path.join(coco_labels, fileXml), os.path.join(ee104ValLabelPath, fileXml))
    
    #remove files from arrays
    imgs.remove(fileJpg)
    xmls.remove(fileXml)

#The rest of files will be validation files, so rename origin dir to val dir
#os.rename(crsPath, valPath)
shutil.move(coco_images, ee104ValImagePath) 
shutil.move(coco_labels, ee104ValLabelPath) 