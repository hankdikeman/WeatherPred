#import packages and subfunctions
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
from CNN_GenProgs import *

##
#   Need to include data processing and import function
##

# generate model using generation function
CNN_model = Gen_CNN_Model(x_len, y_len, day_num, num_fil)
# compile model using adam optimizer
CNN_model.compile(optimizer = 'adam',
                    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
                    metrics = ['accuracy']
                    )
# run model on training data
history = CNN_model.fit(train_x, train_y,
                        epochs = epoch_num,
                        validation_data=(test_x, test_y))
