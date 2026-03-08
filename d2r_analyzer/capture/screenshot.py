import bettercam

WIDTH, HEIGHT = 800, 800
OFFSET_X = 0
OFFSET_Y = -260

camera = bettercam.create()


def capture_screenshot(x, y):
    center_x = int(x + OFFSET_X)
    center_y = int(y + OFFSET_Y)

    left = center_x - WIDTH // 2
    top = center_y - HEIGHT // 2
    right = center_x + WIDTH // 2
    bottom = center_y + HEIGHT // 2

    screen_w = getattr(camera, "width", None)
    screen_h = getattr(camera, "height", None)
    if (
        isinstance(screen_w, int)
        and isinstance(screen_h, int)
        and screen_w > 0
        and screen_h > 0
    ):
        left = max(0, left)
        top = max(0, top)
        right = min(screen_w, right)
        bottom = min(screen_h, bottom)

    if right <= left or bottom <= top:
        raise RuntimeError(
            "Computed capture region is invalid. Tune WIDTH/HEIGHT/OFFSET values."
        )

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
