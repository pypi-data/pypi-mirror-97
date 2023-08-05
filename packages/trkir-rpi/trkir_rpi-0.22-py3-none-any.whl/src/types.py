from numpy import ndarray
from typing import Generator, List, Tuple


Frame = ndarray
TemperatureFrames = Tuple[List[List], List[Frame]]
FrameGenerator = Generator[TemperatureFrames, None, None]
