# -*- coding: utf-8 -*-
# extract_features.py

import os
import random
import argparse
import progressbar
import numpy as np
from imutils import paths
from juggle.io import HDF5DatasetWriter
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.applications import ResNet50


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
    help = "path to input dataset")
ap.add_argument("-o", "--output", required = True,
    help = "path to output HDF5 file")
ap.add_argument("-b", "--batch-size", type = int, default = 16,
    help = "batch size of images to be passed through network")
ap.add_argument("-s", "--buffer-size", type = int, default = 1000,
    help = "size of feature extraction buffer")
args = vars(ap.parse_args())


# store the batch size in a convenience variable
bs = args["batch_size"]

# grab the list of images that we'll be describing then randomly shuffle
# them to allow for easy training and testing splits via
# array slicing during training time
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["dataset"]))
random.shuffle(imagePaths)


# extract the class labels from the image paths then encode the labels
labels = [p.split(os.path.sep)[-1].split(".")[0] for p in imagePaths]
le = LabelEncoder()
labels = le.fit_transform(labels)

# load the ResNet50 network
print("[INFO] loading network...")
model = ResNet50(weights = "imagenet", include_top = False)

# initialize the HDF5 dataset writer, then store the class label
# names in the dataset
dataset = HDF5DatasetWriter(
    (len(imagePaths), 2048),
    args["output"], dataKey = "features", bufSize = args["buffer_size"]
)
dataset.storeClassLabels(le.classes_)

# iinitialize the progressbar
widgets = ["Extracting Features: ", progressbar.Percentage(), " ",
    progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval = len(imagePaths), widgets = widgets).start()


for i in np.arange(0, len(imagePatjs), bs):
    # extract the batch of images and labels, the initialize the
    # list of actual iamges that will be passed through the network
    # for feature extraction
    batchPaths = imagePaths[i: i + bs]
    batchLabels = labels[i: i + bs]
    batchImages = []

    # loop over the images nad labels in the current batch
    for (j, imagePath) in enumerate(batchPaths):
        # load the input image using the Keras helper utility
        # while ensuring the iamge is resized to 224 * 224 pixels
        image = load_img(imagePath, target_size = (224, 224))
        image = img_to_array(image)

        # preprocess the image by (1) expanding the dimensions and
        # (2) subtracting the mean RGB pixel intensiry from the
        # imagenet dataset
        image = np.expand_dims(image, axis = 0)
        image = imagenet_utils.preprocess_input(image)

        # add the image to the batch
        batchImages.append(image)

        # pass the image throught the network and use the output as out
        # actual features
        batchImages = np.vstack(batchImages)
        features = model.predict(batchImages, batch_size = bs)

        # reshape the features so that each image is represented by
        # a flattened feature vector of the `MaxPooling2D` outputs
        features = features.reshape((features.shape[0], 2048))

        # add features and labels to out HDF5 dataset
        dataset.add(features, batchLabels)
        pbar.update(i)

# close the dataset
dataset.close()
pbar.finish()

