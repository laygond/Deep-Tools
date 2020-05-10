# minivggnet_flowers17_data_aug.py

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from imutils import paths
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from juggle.nn.conv import MiniVGGNet
from juggle.preprocessing import SimpleDatasetLoader
from juggle.preprocessing import AspectAwarePreprocessor
from juggle.preprocessing import ImageToArrayPreprocessor
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer



ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
        help = "path to input dataset")
args = vars(ap.parse_args())



# grab the list of images that we'll be describing, then extract
# the class label names from the image paths
print("[INFO] loading images...")
imagePaths = list(paths.list_images(args["dataset"]))
classNames = [imagepath.split(os.path.sep)[-2] for imagepath in imagePaths]
classNames = [str(name) for name in np.unique(classNames)]


aap = AspectAwarePreprocessor(64, 64)
iap = ImageToArrayPreprocessor()


# load the dataset from disk then scale
# raw pizel intensities to range [0, 1]
sdl = SimpleDatasetLoader(preprocessors = [aap, iap])
(data, labels) = sdl.load(imagePaths, verbose = 500)
data = data.astype("float") / 255.0


# partition the data into training and testing split
(trainX, testX,trainY, testY) = train_test_split(data, labels, test_size = 0.25, random_state = 42)


# convert the labels from integers to vectors
trainY = LabelBinarizer().fit_transform(trainY)
testY = LabelBinarizer().fit_transform(testY)


# image data generator for data augmentation
augmentation = ImageDataGenerator(rotation_range = 30,
                        width_shift_range = 0.1,
                        height_shift_range = 0.1,
                        shear_range = 0.2,
                        zoom_range = 0.2,
                        horizontal_flip = True,
                        fill_mode = "nearest"
    )


# initializing model
print("[INFO] compiling model...")
optimizer = SGD(lr = 0.05)
model = MiniVGGNet.build(width = 64,
                    height = 64,
                    depth = 3,
                    classes = len(classNames)
    )
model.compile(loss = "categorical_crossentropy",
            optimizer = optimizer,
            metrics = ["accuracy"]
    )

# train the network
print("[INFO] training network...")
H = model.fit_generator(augmentation.flow(trainX, trainY, batch_size = 32),
                validation_data = (testX, testY),
                steps_per_epoch = len(trainX) // 32,
                epochs = 100,
                verbose = 1
    )


# evaluate network
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size = 32)
print(classification_report(testY.argmax(axis = 1),
                    predictions.argmax(axis = 1),
                    target_names = classNames)
    )


# plot training loss and accuracy
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, 100), H.history["loss"], label = "train_loss")
plt.plot(np.arange(0, 100), H.history["val_loss"], label = "val_loss")
plt.plot(np.arange(0, 100), H.history["acc"], label = "train_acc")
plt.plot(np.arange(0, 100), H.history["val_acc"], label = "val_acc")
plt.title("Training Loss and accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss / Accuracy")
plt.legend()
plt.show()

