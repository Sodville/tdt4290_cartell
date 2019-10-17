import keras
import argparse
import os
from resnet_152 import resnet152_model
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping
from keras.callbacks import ReduceLROnPlateau


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Train network on data.")
    parser.add_argument("--image_width", dest="img_width",
                        type=int, default=224,
                        help="image width of resized images (default 224px)")
    parser.add_argument("--image_height", dest="img_height",
                        type=int, default=224,
                        help="image height of resized images (default 224px)")
    parser.add_argument("--image_channels", dest="num_channels",
                        type=int, default=3,
                        help="number of channels in images (default 3)")
    parser.add_argument("data_path",
                        help="path to data-folder (e.g. data/stanford)")
    parser.add_argument("-nc", "--num_classes", type=int,
                        help=("number of classes in dataset (defaults to the "
                              "number of folders in train-folder if not set)"))
    parser.add_argument("--batch_size", type=int, default=16,
                        help="batch size (defaults to 16)")
    parser.add_argument("-ne", "--num_epochs", type=int, default=10000,
                        help="upper limit on number of epochs (default 10000)")
    parser.add_argument("-p", "--patience", type=int, default=50,
                        help=("number of epochs with no improvement to "
                              "observe before early stopping (default 50)"))
    parser.add_argument("-v", "--verbosity", type=int,
                        choices=[0, 1, 2], default=1,
                        help=("verbosity parameter passed to relevant "
                              "functions (defaults to 1)"))

    args = parser.parse_args()
    print(args)

    # Create training and validation paths
    train_path = os.path.join(args.data_path, "train")
    valid_path = os.path.join(args.data_path, "valid")

    # Retrieve number of classes if not passed as argument
    if not args.num_classes:
        args.num_classes = len(os.listdir(train_path))
    if args.verbosity:
        print(f"Found {args.num_classes} classes.")

    # build a classifier model
    model = resnet152_model(
        args.img_height,
        args.img_width,
        args.num_channels,
        args.num_classes
    )

    # prepare data augmentation configuration
    train_data_gen = ImageDataGenerator(
        rotation_range=20.,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True
    )
    valid_data_gen = ImageDataGenerator()
    # callbacks
    tensor_board = keras.callbacks.TensorBoard(
        log_dir="./logs",
        histogram_freq=0,
        write_graph=True,
        write_images=True
    )
    log_file_path = "logs/training.log"
    csv_logger = CSVLogger(log_file_path, append=False)
    early_stop = EarlyStopping("val_acc", patience=args.patience)
    reduce_lr = ReduceLROnPlateau(
        "val_acc",
        factor=0.1,
        patience=int(args.patience / 4),
        verbose=min(args.verbosity, 1)
    )
    trained_models_path = "models/model"
    model_names = trained_models_path + ".{epoch:02d}-{val_acc:.2f}.hdf5"
    model_checkpoint = ModelCheckpoint(
        model_names,
        monitor="val_acc",
        verbose=min(args.verbosity, 1),
        save_best_only=True
    )
    callbacks = [tensor_board, model_checkpoint, csv_logger,
                 early_stop, reduce_lr]

    # generators
    train_generator = train_data_gen.flow_from_directory(
        train_path,
        (args.img_width, args.img_height),
        batch_size=args.batch_size,
        class_mode="categorical"
    )
    valid_generator = valid_data_gen.flow_from_directory(
        valid_path,
        (args.img_width, args.img_height),
        batch_size=args.batch_size,
        class_mode="categorical"
    )

    # fine tune the model
    model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.n / args.batch_size,
        validation_data=valid_generator,
        validation_steps=valid_generator.n / args.batch_size,
        epochs=args.num_epochs,
        callbacks=callbacks,
        verbose=args.verbosity
    )
