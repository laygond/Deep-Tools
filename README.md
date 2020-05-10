# Juggle
Inspired by Adrian Rosebrock Pyimagesearch starter, practitioner, and imagenet bundle DL4CV.
```
pip install juggle
```
The juggle directory contains the classic pyimagesearch tools with additional deep learnig tools

#### Differences with pyimagesearch
These are the 5 following changes:
- The first letter of every word in a file's title has been switched to uppercase, e.g.,`simpledatasetloader.py` is now `SimpleDatasetLoader.py` 
- All Keras libraries have been already moved to `tensorflow.keras` so is up to date with TensorFlow 2.0 ,i.e,
```
# Before
from keras.preprocessing.image import load_img
# Now
from tensorflow.keras.preprocessing.image import load_img
```
- `SimpleDatasetLoader.py` previously located in `pyimageserach/datasets` has been moved to `preprocessing` to match Keras style 
```
from tensorflow.keras.preprocessing.image import load_img
from juggle.preprocessing import SimpleDatasetLoader
```