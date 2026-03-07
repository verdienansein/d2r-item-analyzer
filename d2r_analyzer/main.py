from logging import info

from pynput import keyboard

TIMEOUT = 10

try:
    from d2r_analyzer.capture import capture_screenshot
except ModuleNotFoundError:
    from capture import capture_screenshot

hotkeys = {"<ctrl>+<shift>+w": capture_screenshot}

with keyboard.GlobalHotKeys(hotkeys) as h:
    info("D2R Item Analyzer is running. Press Ctrl+Shift+W to capture a screenshot.")
    h.join(timeout=TIMEOUT)
