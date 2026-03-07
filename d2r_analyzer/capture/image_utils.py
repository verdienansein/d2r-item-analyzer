import base64
import io

from numpy import np
from PIL import Image


def frame_to_base64(frame: np.ndarray) -> str:
    image = Image.fromarray(frame)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
