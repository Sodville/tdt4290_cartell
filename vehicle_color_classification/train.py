from model import make_model

from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint, TensorBoard

from time import time

CKPT_PATH = 'color_weights.hdf5'
WIDTH, HEIGHT = 227, 227
NUM_CLASSES = 8
BATCH_SIZE = 32
NUM_EPOCHS = 10

if __name__ == "__main__":
    img_shape = (HEIGHT, WIDTH, 3)
    model = make_model(img_shape, NUM_CLASSES)

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_set = train_datagen.flow_from_directory(
        'data/train/',
        target_size=(HEIGHT, WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    val_set = val_datagen.flow_from_directory(
        'data/val/',
        target_size=(HEIGHT, WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # only save the weights that results the best validation accuracy
    checkpoint = ModelCheckpoint(CKPT_PATH, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    tensorboard = TensorBoard(log_dir='logs/{}'.format(time()))
    callbacks_list = [checkpoint, tensorboard]

    model.fit_generator(
        train_set,
        steps_per_epoch=train_set.n//BATCH_SIZE,
        epochs=NUM_EPOCHS,
        validation_data=val_set,
        validation_steps=val_set.n//BATCH_SIZE,
        callbacks=callbacks_list
    )
    model.save('color_model.h5')

    print("Finished", NUM_EPOCHS, "epochs of training")
