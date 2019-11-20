import keras
from keras.models import Model, Sequential
from keras import layers
from keras.layers import Dense, GlobalAveragePooling2D, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, CSVLogger, EarlyStopping, ReduceLROnPlateau, TensorBoard
import efficientnet.keras as efn

"""
This script runs num_epochs epochs of training on img_width x img_height sized images 
for the model specified in `make_model`
The best weights from the validation testing will be saved to output_weights.
batch_size should be adjusted according to the amount of memory available on the device,
and num_epochs should be changed accordingly to when one sees the model is overfitting.
Additionally, if you want the training process to abort when the validation accuracy stalls, you can
adjust the `patiaence` parameter accordingly.

`train_data_dir` specifies the directory containing the training set and 
`validation_data_dir` specifies the directory containing the validation set.
Both directories should be in a label-folder structure, where the folder-names specifies
the label for all images within that folder. E.g. all images within the folder "audi" are labelled as Audis.
"""

img_width, img_height = 512, 512

# dimensions of our images.
num_classes = 14

output_weights = "efficientnetb0.hdf5"

train_data_dir = "data/train"
validation_data_dir = "data/valid"

num_epochs = 200
batch_size = 6
patience=50

def make_model():
    """
    Creates an EfficientNet model with parameters specified `num_classes` outputs
    and `img_width` x `img_height` input shape.
    Args:

    Returns: an EfficientNet model with specified global parameters.
    """
    # create the base pre-trained model
    base_model = efn.EfficientNetB0(input_shape=(img_width, img_height, 3), include_top=False)
    # add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    predictions = Dense(num_classes, activation="softmax")(x)
    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    return base_model, model

if __name__ == "__main__":
    # prepare data augmentation configuration
    train_datagen = ImageDataGenerator(rotation_range=20.,
                                        width_shift_range=0.1,
                                        rescale= 1./255.,
                                        height_shift_range=0.1,
                                        zoom_range=0.2,
                                        horizontal_flip=True)
    validation_datagen = ImageDataGenerator(rescale=1./255.)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode="categorical"
    )

    validation_generator = validation_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode="categorical"
    )

    # Callbacks
    tensor_board = TensorBoard(log_dir="./logs", histogram_freq=0, write_graph=True, write_images=True)
    log_file_path = "logs/training.log"
    csv_logger = CSVLogger(log_file_path, append=False)
    early_stop = EarlyStopping("val_acc", patience=patience)
    reduce_lr = ReduceLROnPlateau("val_acc", factor=0.1, patience=10, verbose=1)
    model_checkpoint = ModelCheckpoint(output_weights, monitor="val_acc", verbose=1, save_best_only=True, save_weights_only=False)
    callbacks = [tensor_board, model_checkpoint, csv_logger, early_stop, reduce_lr]

    _, model = make_model()
    # train the model on the new data for a few epochs
    model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.n // batch_size,
        epochs=num_epochs,
        validation_data=validation_generator,
        validation_steps= validation_generator.n // batch_size,
        callbacks=callbacks,
        verbose=1
    )
