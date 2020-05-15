# FCHNet.py

from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout


class FCHeadNet:
    '''
    '''
    @staticmethod
    def build(baseModel:'keras.model', classes:int, D:int) -> 'Head Model':
        '''
        parameters
        ----------
            baseModel: The mmain body of the neural network
            classes: the number of classes for the dataset
            D: number of nodes in the fully-connected layer
        returns
        -------
            headModel: The last layer of the nerual net as a FC layer
        '''
        # initialize the head model that will be placed on top of
        # the base, then add a FC layer
        headModel = baseModel.output
        headModel = Flatten(name = "flatten")(headModel)
        headModel = Dense(D, activation = "relu")(headModel)
        headModel = Dropout(0.5)(headModel)

        # add a softmax layer
        headModel = Dense(classes, activation = "softmax")(headModel)

        # return the model
        return headModel

