# rank_accuracy.py
# Chapter 4.1 Practitioner Bundle
# Rank Accuracy on predictions from a pickle saved model on an HDF5 dataset

# USAGE:
# python sample_code/rank_accuracy.py -d ../datasets/HDF5/Flowers-17.hdf5 --model output/Flowers-17.cpickle


import h5py
import pickle
import argparse
from juggle.utils.ranked import rank5_accuracy


# argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--db", required = True,
        help = "path HDF5 database")
ap.add_argument("-m", "--model", required = True,
        help = "path to pre-trained model")
args = vars(ap.parse_args())


# load the pre-trained model
print("[INFO] loading pre-trained model...")
model = pickle.loads(open(args["model"], "rb").read())


# open the HDF5 database for reading the determine the index
# of the rtrainind and testing split, provided that this data was
# already shuffled *prior* to writing it to disk
db = h5py.File(args["db"], "r")
i = int(db["labels"].shape[0] * 0.75)


# make predictions on the testing set then compute the rank-1
# and rank-5 accuracies
print("[INFO] predicting...")
preds = model.predict_proba(db["features"][i:])
(rank1, rank5) = rank5_accuracy(preds, db["labels"][i:])

# display the rank-1 and rank-5 accuracies
print("[INFO] rank-1: {:.2f}%".format(rank1 * 100))
print("[INFO] rank-5: {:.2f}%".format(rank5 * 100))

# close database
db.close()
