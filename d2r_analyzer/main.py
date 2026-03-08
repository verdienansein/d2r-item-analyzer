import queue
import sys
import threading
import traceback
from datetime import datetime
from pathlib import Path
from time import sleep

import cv2
import pynput
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

work_q = queue.Queue()
stop_event = threading.Event()


def worker_loop():
    while True:
        x, y = work_q.get()
        try:
            frame = capture_screenshot(x, y)
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
            overlay.show(evaluation, x=x, y=y)
        except Exception as exc:
            print(f"Error in worker loop: {exc}")
            traceback.print_exc()
        finally:
            work_q.task_done()


def capture_and_print_base64() -> None:
    try:
        mouse = pynput.mouse.Controller()
        mx, my = mouse.position
        work_q.put((mx, my))
    except Exception as exc:
        print(f"Failed to queue work: {exc}")
        traceback.print_exc()


hotkeys = {"<ctrl>+<shift>+a": capture_and_print_base64}

evaluator = Evaluator()


def main() -> None:
    worker = threading.Thread(target=worker_loop, daemon=True)
    worker.start()
    listener = keyboard.GlobalHotKeys({"<ctrl>+<shift>+a": capture_and_print_base64})
    listener.start()
    print("Running. Press Ctrl+Shift+A to capture. Press Ctrl+C to stop.")
    try:
        while not stop_event.is_set():
            sleep(0.2)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stop_event.set()
        listener.stop()
        work_q.put(None)  # unblock worker if waiting on queue.get
        worker.join(timeout=2)


if __name__ == "__main__":
    main()
