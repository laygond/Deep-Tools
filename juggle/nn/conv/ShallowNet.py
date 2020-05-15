# -*- coding: utf-8 -*-
# ShallowNet.py
'''
Implementation of the ShallowNet architecture.

ShallowNet architecture contains only a few layers – the entire
network architecture can be summarized as:

INPUT --> CONV -*-> RELU --> FC

'''


from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv2D




class ShallowNet:
    '''
    ShallowNet Architecture implementation in Keras
    '''

    @staticmethod
    def build(width:int, height:int, depth:int, classes:int):
        '''
        Build the ShallowNet architecture given width, height and depth
        as dimensions of the input tensor and the corresponding
        number of classes of the data.

        parameters
        ----------
            width:  width of input images.
            height: height of input images.
            depth:  depth if input images.
            classes: number of classes of the corresponding data.

        returns
        -------
            model: the ShallowNet model compatible with given inputs
                    as a keras sequential model.
        '''
        model = Sequential()
        inputShape = (height, width, depth)

        # if we ware using "channels first", update the input shape
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)

        # define the first (and only) CONV -*-> RELU layer
        model.add(Conv2D(32, (3, 3), padding = "same", input_shape = inputShape))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Flatten())
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        return model