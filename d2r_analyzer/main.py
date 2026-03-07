from logging import info

from pynput import keyboard

TIMEOUT = 10

try:
    from d2r_analyzer.capture import capture_screenshot, frame_to_base64
except ModuleNotFoundError:
    from capture import capture_screenshot, frame_to_base64


def capture_and_print_base64() -> None:
    frame = capture_screenshot()
    encoded = frame_to_base64(frame)
    print(encoded)


hotkeys = {"<ctrl>+<shift>+a": capture_and_print_base64}

with keyboard.GlobalHotKeys(hotkeys) as h:
    info("D2R Item Analyzer is running. Press Ctrl+Shift+A to capture a screenshot.")
    h.join(timeout=TIMEOUT)
