#import packages and subfunctions
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
from CNN_GenProgs import *
import matplotlib.pyplot as plt

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

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.show()
