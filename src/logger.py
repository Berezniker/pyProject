from src.pipeline.feature_extraction import extractor
from src.pipeline.preprocessing import preprocessing
from src.pipeline.model import authentication
from typing import Callable, List
from config import RawData
from pynput import mouse
import logging
import time


# link:
# https://docs.python.org/3/library/collections.html#collections.namedtuple
# https://pythonhosted.org/pynput/mouse.html#monitoring-the-mouse


def data_capture_loop(user_id: int, args) -> None:
    """
    Collects data from the user's computer mouse
        "timestamp" - time in seconds from start of recording
        "button"    - button type: ['NoButton', 'Left', 'Scroll', 'Right']
        "state"     - state type: ['Move', 'Pressed', 'Released', 'Drag', 'Down', 'Up']
        "x"         - x-coordinate
        "y"         - y-coordinate

    :param user_id: User ID
    :param args: Command line arguments
    :return: None, when lock is needed
    """
    start_time: float = time.time()
    raw_data: List[RawData] = list()
    click_state: str = "Released"

    def check_end(action: Callable):
        """Decorator"""
        ttime_value = args.ttime_value

        def wrapper(*args, **kwargs) -> bool:
            action(*args, **kwargs)
            ddtm = raw_data[-1].timestamp - raw_data[0].timestamp
            return ddtm < ttime_value

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
        # ------------------------------------------ #
        preprocessing_data = preprocessing(
            raw_data=raw_data,
            min_n_action=args.min_n_action
        )
        if len(preprocessing_data) == 0:
            logging.debug("Empty Preprocessing Data")
        else:
            feature = extractor(data=preprocessing_data)
            if not authentication(user_id=user_id, feature=feature, args=args):
                break  # block
        raw_data.clear()
        # -- time: 15 - 30 ms ----------------------- #

    return


if __name__ == "__main__":
    pass
