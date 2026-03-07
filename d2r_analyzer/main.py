import sys
from logging import info
from pathlib import Path

from pynput import keyboard

TIMEOUT = 10

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from d2r_analyzer.capture import capture_screenshot, frame_to_base64
    from d2r_analyzer.evaluator import Evaluator
except ModuleNotFoundError:
    from capture import capture_screenshot, frame_to_base64
    from evaluator import Evaluator


def capture_and_print_base64() -> None:
    frame = capture_screenshot()
    encoded = frame_to_base64(frame)
    item = evaluator.parse_item(encoded)
    print("Extracted item info:")
    print(item.model_dump_json(indent=2))


hotkeys = {"<ctrl>+<shift>+a": capture_and_print_base64}

evaluator = Evaluator()

with keyboard.GlobalHotKeys(hotkeys) as h:
    info("D2R Item Analyzer is running. Press Ctrl+Shift+A to capture a screenshot.")
    h.join(timeout=TIMEOUT)
