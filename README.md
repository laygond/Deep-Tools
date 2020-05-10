Inspired on Pyimagesearch starter, practitioner, and imagenet bundle.
"""
pip install juggle
"""
The juggle directory contains the classic pyimagesearch tools with the 5 following changes:
- The first letter of every word in a file's title has been switched to uppercase, e.g.,`simpledatasetloader.py` is now `SimpleDatasetLoader.py` 
- `SimpleDatasetLoader.py` previously located in `pyimageserach/datasets` has been moved to `preprocessing` to match Keras style 
"""
from tensorflow.keras.preprocessing.image import load_img
from juggle.preprocessing import SimpleDatasetLoader
"""
- 