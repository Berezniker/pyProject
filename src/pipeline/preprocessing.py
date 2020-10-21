from typing import List, Tuple
import config

RawDataVector = Tuple[float, str, str, int, int]
DataVector = Tuple[float, int, int]

def preprocessing(raw_data: List[RawDataVector]) -> List[DataVector]:
    if len(raw_data) < config.MIN_N_ACTION:
        return []
    data = [
        (timestamp, max(x, 0), max(y, 0))
        for timestamp, _, _, x, y in raw_data
    ]
    return data
