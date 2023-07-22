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


def super_resolution(
    base64_image,
    width=1080,
    height=1920,
    method="espcn",
    ratio=4,
):
    image_bufferIO = io.BytesIO(base64.b64decode(base64_image))
    cv_image = imdecode(numpy.frombuffer(image_bufferIO.getbuffer(), numpy.uint8), -1)

    sr = dnn_superres.DnnSuperResImpl_create()
    path = f"{MODELS_PATH}/{method}_x{ratio}.pb"
    sr.readModel(path)
    sr.setModel(
        method, ratio
    )  # set the model by passing the value and the upsampling ratio
    result = sr.upsample(cv_image)  # upscale the input image

    resized = resize(result, (width, height), interpolation=INTER_AREA)

    _, im_buf_arr = imencode(f".{extension}", resized)

    return base64.b64encode(im_buf_arr.tobytes())
