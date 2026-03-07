import bettercam

camera = bettercam.create()

def capture_screenshot():
    region = bettercam.Region(0, 0, 1920, 1080)
    frame = camera.grab(region=region)