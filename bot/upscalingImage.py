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
from flask import Flask, request, jsonify

app = Flask(__name__)

MODELS_PATH = "/models CV2"

extension = "jpg"


def super_resolution(
    base64_image,
    width=1218,
    height=1572,
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

    return base64.b64encode(im_buf_arr.tobytes()).decode("utf-8")


@app.route("/upscale_image", methods=["POST"])
def handle_post_request():
    data = request.json

    if "image" in data:
        response = {
            "message": "Image upscaling successful!",
            "upscaled_image": super_resolution(data["image"]),
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid data format"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
