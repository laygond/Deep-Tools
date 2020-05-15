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
- All training sample codes with plots have been modified to meet (TF 2.0 Metrics [acc] vs [accuracy])[https://github.com/keras-team/keras/releases/tag/2.3.0]. All metrics have been switched to \[acc\] for backward compatibility. In summary the new changes suggest that if you specify metrics=["accuracy"] in the model.compile(), then the history object will have the keys as 'accuracy' and 'val_accuracy'. While if you specify it as metrics=["acc"] then they will be reported with the keys 'acc' and 'val_acc'.
- General TF 2.0 Differences
```
# BEFORE
from keras.utils.np_utils import to_categorical
from keras.layers.core import Dense
from keras.layers.convolutional import Conv2D

# NOW
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Conv2D

```