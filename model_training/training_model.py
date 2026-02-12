import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# --- 1. UNZIP DATA ---
# This opens your uploaded zip file
if os.path.exists("dataset.zip"):
    print("Unzipping dataset...")
    !unzip -q dataset.zip
    print("Unzip Complete!")
else:
    print("ERROR: Please upload dataset.zip first!")

# --- 2. SETTINGS ---
BATCH_SIZE = 32
IMG_SIZE = (224, 224)
DATA_DIR = "dataset"  # This matches the folder inside your zip

# --- 3. DATA LOADERS ---
# IMPROVED DATA LOADER (With Augmentation)
datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=20,      # Rotate image slightly
    width_shift_range=0.2,  # Shift left/right
    height_shift_range=0.2, # Shift up/down
    shear_range=0.2,        # Distort shape
    zoom_range=0.2,         # Zoom in (Helpful for cracks)
    horizontal_flip=True,   # Mirror image
    fill_mode='nearest',
    validation_split=0.2
)
# The rest of your code (flow_from_directory) stays exactly the same!

print("\nLoading Training Data...")
train_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

print("\nLoading Validation Data...")
val_generator = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# --- 4. BUILD MODEL ---
print("\nDownloading MobileNetV2...")
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze the base

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# --- 5. TRAIN ---
print("\nStarting Training on GPU...")
history = model.fit(
    train_generator,
    epochs=20,  # We can do more epochs since GPU is fast!
    validation_data=val_generator
)

# --- 6. SAVE ---
model.save("my_house_model.h5")
print("\nSUCCESS! Model saved as 'my_house_model.h5'")
