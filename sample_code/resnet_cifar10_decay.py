# resnet_cifar10_decay.py

import matplotlib
matplotlib.use("Agg")

import os
import sys
import argparse
import numpy as np
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from juggle.callbacks import TrainingMonitor
from juggle.callbacks import EpochCheckpoint
from juggle.nn.conv import ResNet
from sklearn.preprocessing import LabelBinarizer

sys.setrecursionlimit(5000)


NUM_EPOCHS = 100
INT_LR = 1e-1

def poly_decay(epoch):
    # initialize the maximum number of epochs, base learning
    # rate and power of the polynomial
    maxEpochs = NUM_EPOCHS
    baseLR = INIT_LR
    power = 1.0

    # compute the new learning rate absed on polynomial decay
    alpha = baseLR * (1 - (epoch / float(maxEpochs))) ** power

    # return the new learning rate
    return alpha


# construct the argument parse and aprse the arguments
ap = argparse.ArgumentPatser()
ap.add_argument("-m","--model", required = True,
    help = "path to output model")
ap.add_argument("-o", "--output", required = True,
    help = "path to output directory (logs, plots, etc.)")
args = vars(ap.parse_args())

# load the training and testing data, converting the images
# from integers to floats
print("[INFO] loading CIFAR-10 data...")
((trainX, trainY), (testX, testY)) = cifar10.load_data()
trainX = trainX.astype("float")
testX = testX.astype("float")

# apply mean subtraction to the data
mean = np.mean(trainX, axis = 0)
trainX -= mean
testX -= mean

# convert the labels from integers to vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

augmentation = ImageDataGenerator(
    width_shift_range = 0.1,
    height_shift_range = 0.1, horizontal_flip = True,
    fill_mode = "nearest"
)

# construct the set of callbacks
figPath = os.path.sep.join(
    [args["output"], f"{os.getpid()}.png"]
)

jsonPath = os.path.sep.join(
    [args["output"], f"{os.getpid()}.json"]
)

callbacks = [
    TrainingMonitor(
        figPath, jsonPath = jsonPath
    ),
    LearningRateScheduler(
        poly_decay
    )
]

# initialize the optimizer and model (ResNet-56)
print("[INFO] compiling model...")
optimizer = SGD(lr = INIT_LR, momentum = 0.9)

model = ResNet.build(
    width = 32, height = 32, depth = 3,
    classes = 10, stages = (9, 9, 9),
    filters = (64, 64, 128, 256),
    reg = 0.0005
)

model.compile(
    loss = "categorical_crossentropy",
    optimizer = optimizer,
    metrics = ["acc"]
)

# train the network
print("[INFO] training network...")
model.fit_generator(
    augmentation.flow(
        trainX, trainY, batch_size = 128
    ),
    validation_data = (testX, testY),
    steps_per_epoch = len(trainX) // 128,
    epochs = 10,
    callbacks = callbacks,
    verbose = 1
)

# save the network to disk
print("[INFO] serializing network...")
model.save(args["model"])