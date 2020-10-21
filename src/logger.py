# from src.pipeline.feature_extraction import extractor
from src.pipeline.preprocessing import preprocessing
from pynput import mouse
import config
import time


def data_capture_loop() -> None:
    """
    Collects data from the user's computer mouse
        "timestamp" - time in seconds from start of recording
        "button"    - button type: ['NoButton', 'Left', 'Scroll', 'Right']
        "state"     - state type: ['Move', 'Pressed', 'Released', 'Drag', 'Down', 'Up']
        "x"         - x-coordinate
        "y"         - y-coordinate
    """
    start_time = time.time()
    raw_data = list()
    state = "Released"

    def check_end():
        ddtm = raw_data[-1][0] - raw_data[0][0]
        return ddtm < config.TTIME_VALUE

    def on_move(x, y):
        move_state = 'Drag' if state == 'Pressed' else 'Move'
        raw_data.append(
            (time.time() - start_time, "NoButton", move_state, x, y)
        )
        return check_end()

    def on_click(x, y, button, pressed):
        nonlocal state
        state = "Pressed" if pressed else "Released"
        raw_data.append(
            (time.time() - start_time, button.name.capitalize(), state, x, y)
        )
        return check_end()

    def on_scroll(x, y, dx, dy):
        scroll_state = "Down" if dy < 0 else "Up"
        raw_data.append(
            (time.time() - start_time, "Scroll", scroll_state, x, y)
        )
        return check_end()

    while True:
        with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as listener:
            listener.join()
            # stopped when the chek_end() returns False
        print(len(raw_data))
        preprocessing(raw_data[:-1])
        if len(raw_data) < 100: break
        # extractor(preprocessing(raw_data[:-1]))
        raw_data.clear()


if __name__ == "__main__":
    print("Run!")
    data_capture_loop()
    print("End of run.")
