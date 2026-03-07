import sys
from datetime import datetime
from pathlib import Path

import pynput

import cv2
from pynput import keyboard

TIMEOUT = 200000000

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from d2r_analyzer.capture import capture_screenshot, frame_to_base64
    from d2r_analyzer.evaluator import Evaluator
    from d2r_analyzer.ui.overlay import ItemOverlay
except ModuleNotFoundError:
    from capture import capture_screenshot, frame_to_base64
    from evaluator import Evaluator
    from ui.overlay import ItemOverlay


def capture_and_print_base64() -> None:
    frame = capture_screenshot()

    screenshots_dir = Path(__file__).resolve().parent.parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    save_path = screenshots_dir / filename
    cv2.imwrite(str(save_path), frame)
    print(f"Screenshot saved to {save_path}")

    encoded = frame_to_base64(frame)
    item = evaluator.parse_item(encoded)
    print("Extracted item info:")
    print(item.model_dump_json(indent=2))
    print("Evaluating item...")
    evaluation = evaluator.evaluate_item(item)
    print("Evaluation result:")
    print(evaluation.model_dump_json(indent=2))
    overlay = ItemOverlay()
    mouse = pynput.mouse.Controller()
    mx, my = mouse.position
    overlay.show(evaluation, x=mx, y=my)


hotkeys = {"<ctrl>+<shift>+a": capture_and_print_base64}

evaluator = Evaluator()

with keyboard.GlobalHotKeys(hotkeys) as h:
    print("D2R Item Analyzer is running. Press Ctrl+Shift+A to capture a screenshot.")
    h.join(timeout=TIMEOUT)
