import logging
import queue
import sys
import threading
from datetime import datetime
from pathlib import Path
from time import sleep

import cv2
import pynput
from pynput import keyboard

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from d2r_analyzer.capture import capture_screenshot, frame_to_base64
from d2r_analyzer.config import config
from d2r_analyzer.evaluator import Evaluator
from d2r_analyzer.ui.overlay import ItemOverlay

logger = logging.getLogger(__name__)

evaluator = Evaluator(
    config.llm_model_name,
    config.llm_base_url,
    config.openai_api_key,
    config.evaluation_mode,
    config.manual_evaluation_rules_file,
)

work_q = queue.Queue()
ui_q = queue.Queue()
stop_event = threading.Event()


def worker_loop() -> None:
    while True:
        job = work_q.get()
        if job is None:
            work_q.task_done()
            break

        x, y = job
        try:
            frame = capture_screenshot(x, y)
            if config.save_captured_images:
                screenshots_dir = Path(__file__).resolve().parent.parent / "screenshots"
                screenshots_dir.mkdir(exist_ok=True)
                filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                save_path = screenshots_dir / filename
                cv2.imwrite(str(save_path), frame)
                logger.info("Screenshot saved to %s", save_path)
            encoded = frame_to_base64(frame)
            item = evaluator.parse_item(encoded)
            logger.debug("Extracted item info:\n%s", item.model_dump_json(indent=2))
            logger.info("Evaluating item...")
            evaluation = evaluator.evaluate_item(item)
            logger.debug("Evaluation result:\n%s", evaluation.model_dump_json(indent=2))
            ui_q.put(("result", evaluation, x, y))
        except Exception as exc:
            logger.exception("Error in worker loop: %s", exc)
            ui_q.put(("error", str(exc), x, y))
        finally:
            work_q.task_done()


def capture_and_print_base64() -> None:
    try:
        mouse = pynput.mouse.Controller()
        mx, my = mouse.position
        ui_q.put(("analyzing", "Analyzing item...", mx, my))
        work_q.put((mx, my))
    except Exception as exc:
        logger.exception("Failed to queue work: %s", exc)


def main() -> None:
    logging.basicConfig(
        level=config.log_level.upper(),
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    overlay = ItemOverlay(auto_close_ms=10000)
    worker = threading.Thread(target=worker_loop, daemon=True)
    worker.start()
    listener = keyboard.GlobalHotKeys({config.capture_hotkey: capture_and_print_base64})
    listener.start()
    logger.info(
        "Running. Press %s to capture. Press Ctrl+C to stop.", config.capture_hotkey
    )
    try:
        while not stop_event.is_set():
            while True:
                try:
                    event_type, payload, x, y = ui_q.get_nowait()
                except queue.Empty:
                    break
                if event_type == "analyzing":
                    overlay.show_status(str(payload), x=x, y=y)
                elif event_type == "result":
                    overlay.show(payload, x=x, y=y)
                elif event_type == "error":
                    overlay.show_status(
                        f"Evaluation failed: {payload}",
                        x=x,
                        y=y,
                        auto_close_ms=4500,
                    )

            try:
                overlay.process_events()
            except Exception:
                pass
            sleep(0.2)
    except KeyboardInterrupt:
        logger.info("Stopping...")
    finally:
        stop_event.set()
        listener.stop()
        work_q.put(None)
        worker.join(timeout=2)


if __name__ == "__main__":
    main()
