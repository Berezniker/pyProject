from src.pipeline.feature_extraction import extractor
from src.pipeline.preprocessing import preprocessing
from config import RawData, TTIME_VALUE
from typing import Callable, List
from pynput import mouse
import time


# link:
# https://docs.python.org/3/library/collections.html#collections.namedtuple
# https://pythonhosted.org/pynput/mouse.html#monitoring-the-mouse


def data_capture_loop() -> None:
    """
    Collects data from the user's computer mouse
        "timestamp" - time in seconds from start of recording
        "button"    - button type: ['NoButton', 'Left', 'Scroll', 'Right']
        "state"     - state type: ['Move', 'Pressed', 'Released', 'Drag', 'Down', 'Up']
        "x"         - x-coordinate
        "y"         - y-coordinate
    """
    start_time: float = time.time()
    raw_data: List[RawData] = list()
    click_state: str = "Released"

    def check_end(action: Callable):
        """Decorator"""

        def wrapper(*args, **kwargs) -> bool:
            action(*args, **kwargs)
            ddtm = raw_data[-1].timestamp - raw_data[0].timestamp
            return ddtm < TTIME_VALUE

        return wrapper

    @check_end
    def on_move(x: int, y: int):
        """
        The callback to call when mouse move events occur.
        """
        move_state = "Drag" if click_state == "Pressed" else "Move"
        raw_data.append(RawData(
            timestamp=time.time() - start_time,
            button="NoButton",
            state=move_state,
            x=x, y=y
        ))

    @check_end
    def on_click(x: int, y: int, button: mouse.Button, pressed: bool):
        """
        The callback to call when a mouse button is clicked.
        """
        nonlocal click_state
        click_state = "Pressed" if pressed else "Released"
        raw_data.append(RawData(
            timestamp=time.time() - start_time,
            button=button.name.capitalize(),
            state=click_state,
            x=x, y=y
        ))

    @check_end
    def on_scroll(x: int, y: int, dx: int, dy: int):
        """
        The callback to call when mouse scroll events occur.
        """
        scroll_state = "Down" if dy < 0 else "Up"
        raw_data.append(RawData(
            timestamp=time.time() - start_time,
            button="Scroll",
            state=scroll_state,
            x=x, y=y
        ))

    while True:
        # A listener for mouse events
        with mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll) as listener:
            listener.join()
            # stopped when the chek_end() returns False
        print(len(raw_data))
        if len(raw_data) < 100: break
        extractor(preprocessing(raw_data))
        raw_data.clear()


if __name__ == "__main__":
    print("Run!")
    data_capture_loop()
    print("End of run.")
