from keras.models import Model
from keras.layers import BatchNormalization, Lambda, Input, Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.layers.merge import Concatenate
from keras import optimizers

# Implementation of model from https://arxiv.org/pdf/1510.07391.pdf

def make_model(input_shape, num_classes):
    """
    Creates a color prediction model with specified input shape and specified number of output classes
    Args:
        input_shape: The shape of the model input
        num_classes: Number of output classes for the model.

    Returns: The model with specified arguments
    """
    input_image = Input(shape=input_shape)
    # ============================================= TOP BRANCH ===================================================
    # first top convolution layer
    top_conv1 = Conv2D(filters=48, kernel_size=(11,11), strides=(4,4), input_shape=input_shape, activation='relu')(input_image)
    top_conv1 = BatchNormalization()(top_conv1)
    top_conv1 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(top_conv1)

    # second top convolution layer
    top_top_conv2 = Conv2D(filters=64, kernel_size=(3,3),activation='relu',padding='same')(top_conv1)
    top_top_conv2 = BatchNormalization()(top_top_conv2)
    top_top_conv2 = MaxPooling2D(pool_size=(3,3),strides=(2,2))(top_top_conv2)

    # second bot convolution layer
    top_bot_conv2 = Conv2D(filters=64, kernel_size=(3,3), activation='relu',padding='same')(top_conv1)
    top_bot_conv2 = BatchNormalization()(top_bot_conv2)
    top_bot_conv2 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(top_bot_conv2)

    # third top convolution layer
    top_conv3 = Concatenate()([top_top_conv2, top_bot_conv2])
    top_conv3 = Conv2D(filters=192,kernel_size=(3,3),activation='relu',padding='same')(top_conv3)

    # fourth top convolution layer
    top_top_conv4 = Conv2D(filters=96, kernel_size=(3,3), activation='relu', padding='same')(top_conv3)
    # fourth bot convolution layer
    top_bot_conv4 = Conv2D(filters=96, kernel_size=(3,3), activation='relu', padding='same')(top_conv3)

    # fifth top convolution layer
    top_top_conv5 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(top_top_conv4)
    top_top_conv5 = MaxPooling2D(pool_size=(3,3),strides=(2,2))(top_top_conv5) 

    # fifth bot convolution layer
    top_bot_conv5 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(top_bot_conv4)
    top_bot_conv5 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(top_bot_conv5)

    # ============================================= TOP BOTTOM ===================================================
    # first bottom convolution layer
    bottom_conv1 = Conv2D(filters=48, kernel_size=(11,11), strides=(4,4), input_shape=input_shape, activation='relu')(input_image)
    bottom_conv1 = BatchNormalization()(bottom_conv1)
    bottom_conv1 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(bottom_conv1)

    # second bottom convolution layer
    bottom_top_conv2 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(bottom_conv1)
    bottom_top_conv2 = BatchNormalization()(bottom_top_conv2)
    bottom_top_conv2 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(bottom_top_conv2)

    bottom_bot_conv2 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(bottom_conv1)
    bottom_bot_conv2 = BatchNormalization()(bottom_bot_conv2)
    bottom_bot_conv2 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(bottom_bot_conv2)

    # third bottom convolution layer
    bottom_conv3 = Concatenate()([bottom_top_conv2, bottom_bot_conv2])
    bottom_conv3 = Conv2D(filters=192, kernel_size=(3,3), activation='relu', padding='same')(bottom_conv3)

    # fourth bottom convolution layer
    bottom_top_conv4 = Conv2D(filters=96, kernel_size=(3,3), activation='relu', padding='same')(bottom_conv3)
    bottom_bot_conv4 = Conv2D(filters=96, kernel_size=(3,3), activation='relu', padding='same')(bottom_conv3)

    # fifth bottom convolution layer
    bottom_top_conv5 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(bottom_top_conv4)
    bottom_top_conv5 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(bottom_top_conv5) 

    bottom_bot_conv5 = Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same')(bottom_bot_conv4)
    bottom_bot_conv5 = MaxPooling2D(pool_size=(3,3), strides=(2,2))(bottom_bot_conv5)

    conv_output = Concatenate()([top_top_conv5, top_bot_conv5, bottom_top_conv5, bottom_bot_conv5])
    flatten = Flatten()(conv_output)

    fc1 = Dense(units=4096, activation='relu')(flatten)
    fc1 = Dropout(0.5)(fc1)
    fc2 = Dense(units=4096, activation='relu')(fc1)
    fc2 = Dropout(0.5)(fc2)
    out = Dense(units=num_classes, activation='softmax')(fc2)
    
    model = Model(inputs=input_image, outputs=out)
    optimizer = optimizers.SGD(lr=1e-3, momentum=0.9, decay=1e-6, nesterov=True)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    from keras.utils import plot_model
    model = make_model((227,227,3), 8)
    plot_model(model, to_file="model_graph.png")
