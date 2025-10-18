"""Model loading and image prediction utilities for digit classification using Keras."""
# Importing required libs
import os
from keras.models import load_model
from keras.utils import img_to_array
import numpy as np
from PIL import Image, UnidentifiedImageError

# Loading model
model = load_model("digit_model.h5")


# Preparing and pre-processing the image
def preprocess_img(img_path):
    """
    Preprocess an input image for model prediction.

    Steps:
    - Opens the image from the provided path.
    - Resizes it to 224x224 pixels.
    - Converts it to a normalized NumPy array.
    - Reshapes it to match the model input dimensions.

    Args:
        img_path (str or file-like): Path to the image file or a file stream.

    Returns:
        np.ndarray: Preprocessed image array ready for prediction.
        If array (image) cannot be read, return error
    """
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image file not found: {img_path}")


    try:
        op_img = Image.open(img_path)

        img_resize = op_img.resize((224, 224))
        img2arr = img_to_array(img_resize) / 255.0
        img_reshape = img2arr.reshape(1, 224, 224, 3)
        return img_reshape
    except (OSError, UnidentifiedImageError):
        print(f"Warning: Could not read image {img_path}")
        raise OSError(f"Corrupted or unreadable image: {img_path}")


# Predicting function
def predict_result(predict):
    """
    Generate a digit prediction from a preprocessed image.

    Args:
        predict (np.ndarray): Preprocessed image array from `preprocess_img`.

    Returns:
        int: Predicted digit label.
    """

    pred = model.predict(predict)
    return np.argmax(pred[0], axis=-1)
