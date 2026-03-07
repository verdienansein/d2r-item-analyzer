import bettercam
import pynput

WIDTH, HEIGHT = 800, 800
camera = bettercam.create()


def capture_screenshot():
    mouse = pynput.mouse.Controller()
    x, y = mouse.position
    left = x - WIDTH // 2
    top = y - HEIGHT // 2
    right = x + WIDTH // 2
    bottom = y + HEIGHT // 2
    region = (left, top, right, bottom)
    try:
        frame = camera.grab(region=region)
        print("Screenshot captured.")
    except ModuleNotFoundError as exc:
        if exc.name == "cv2":
            raise RuntimeError(
                "OpenCV is required by bettercam. Install it with: pip install opencv-python"
            ) from exc
        raise

    return frame
