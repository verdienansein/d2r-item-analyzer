from logging import info

from pynput import keyboard

TIMEOUT = 10

try:
    from d2r_analyzer.capture import capture_screenshot
    from d2r_analyzer.capture import frame_to_base64
except ModuleNotFoundError:
    from capture import capture_screenshot
    from capture import frame_to_base64

hotkeys = {"<ctrl>+<shift>+a": capture_screenshot}

with keyboard.GlobalHotKeys(hotkeys) as h:
    info("D2R Item Analyzer is running. Press Ctrl+Shift+A to capture a screenshot.")
    h.join(timeout=TIMEOUT)
