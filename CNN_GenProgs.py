import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# generates and returns convolutional model based on following parameters:
# x_len = stations west to east, y_len = stations north to south
# day_num = number of days modelled, num_fil = number of filters used
def Gen_CNN_Model(x_len, y_len, day_num, num_fil):
    # declare model
    CNN_model = models.Sequential()
    # 1 convolutional layer with num_fil 3x3 filters
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu',
                                input_shape = (x_len, y_len, day_num)))
    # 2x2 pooling layer
    CNN_model.add(layers.MaxPooling2d((2, 2)))
    # 2nd convolutional layer
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu'))
    # 2nd 2x2 pooling layer
    CNN_model.add(layers.MaxPooling2d((2, 2)))
    # 3rd convolutional layer
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu'))
    # 3rd pooling layer
    CNN_model.add(layers.MaxPooling2d((2, 2)))
    # flatten output to 1 dimension
    CNN_model.add(layers.Flatten())
    # 1st dense layer with 64 nodes
    CNN_model.add(layers.Dense(64,
                               activation = 'relu'))
    # output layer with 1 output node (for temp)
    CNN_model.add(layers.Dense(1))
    # return generated model
    return CNN_model


def ModelRun_CNN(train_x, train_y, test_x, test_y, day_num, num_fil, epoch_num = 10):
    # these values for the x and y length are WRONG, placeholders
    # these should really be the dimensions of our station grid
    x_len = np.shape(train_x)[0]
    y_len = np.shape(train_x)[1]
    # generate model using above function
    CNN_model = Gen_CNN_Model(x_len, y_len, day_num, num_fil)
    # compile model
    CNN_model.compile(optimizer = 'adam',
                      loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
                      metrixs = ['accuracy']
                      )
    # run model on training data
    history = CNN_model.fit(train_x, train_y, epochs = epoch_num, 
                    validation_data=(test_x, test_y))
    # return model result
    return (CNN_model, history)
