from cv2 import (
    dnn_superres,
    imencode,
    resize,
    imdecode,
    INTER_AREA,
)
import numpy
import base64
import io

MODELS_PATH = "ws-gonsta-api/bot/models CV2"

extension = "jpg"


# def super_resolution(
#     base64_image,
#     width=1080,
#     height=1920,
#     method="espcn",
#     ratio=4,
# ):
#     image_bufferIO = io.BytesIO(base64.b64decode(base64_image))
#     cv_image = imdecode(numpy.frombuffer(image_bufferIO.getbuffer(), numpy.uint8), -1)

#     sr = dnn_superres.DnnSuperResImpl_create()
#     path = f"{MODELS_PATH}/{method}_x{ratio}.pb"
#     sr.readModel(path)
#     sr.setModel(
#         method, ratio
#     )  # set the model by passing the value and the upsampling ratio
#     result = sr.upsample(cv_image)  # upscale the input image

#     resized = resize(result, (width, height), interpolation=INTER_AREA)

#     _, im_buf_arr = imencode(f".{extension}", resized)

#     return base64.b64encode(im_buf_arr.tobytes())


import base64
import io
import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained EDSR model
model = tf.keras.models.load_model("path_to_pretrained_model")


def super_resolution(base64_image, width=1080, height=1920, ratio=4):
    # Decode base64 image data and load it into a numpy array
    image_data = base64.b64decode(base64_image)
    nparr = np.frombuffer(image_data, np.uint8)
    cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Preprocess the image (normalize, resize, etc.) if needed
    # For example, you can use cv2.resize() to resize the image before super-resolution

    # Perform super-resolution on the input image using the loaded model
    upscaled_image = model.predict(np.expand_dims(cv_image, axis=0))

    # Resize the upscaled image to the desired dimensions
    resized_image = cv2.resize(
        upscaled_image.squeeze(), (width, height), interpolation=cv2.INTER_AREA
    )

    # Encode the resized image data to base64 and return
    _, im_buf_arr = cv2.imencode(".jpg", resized_image)
    return base64.b64encode(im_buf_arr.tobytes())
