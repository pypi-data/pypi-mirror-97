import cv2
from typing import List, Dict, Tuple, Callable, Optional
import numpy as np

from src.types import Frame
from src.constants import \
    PT_PIXEL_BYTES_FORMAT, \
    IR_ROUND_PIXEL, \
    MAX_FRAME_PIXEL, \
    MIN_FRAME_PIXEL, \
    BUFFER_FRAME_SEPARATOR


def calibrate_frame(frame, device):
    return frame + device['calibration-values']['max']


def get_frames_configuration(
        pt_devices: List[Dict]
) -> Tuple[Optional[List], Optional[int], Optional[Callable], Optional[Callable]]:
    size, mice_count, group_frames, concatenate_groups = None, None, None, None
    if len(pt_devices) == 3:
        frames_order = [[1, 2, 0]]
        size = [180, 80]
        mice_count = 1

        def group_frames(pt_frames: [Frame]) -> List[List[Frame]]:
            return [
                [
                    cv2.rotate(
                        calibrate_frame(pt_frames[index], pt_devices[index]),
                        cv2.ROTATE_90_COUNTERCLOCKWISE,
                    )
                    for index in frames_order_group
                ]
                for frames_order_group in frames_order
            ]

        def concatenate_groups(frame_groups: List[List[Frame]]) -> List[Frame]:
            frame_groups = [
                normalize_frame(frame)
                for frame in frame_groups[0]
            ]

            return [resize_frame(np.concatenate(frame_groups, axis=1), size)]

    if len(pt_devices) == 4:
        frames_order = [[0, 3], [1, 2]]
        size = [160, 120]
        mice_count = 2

        def group_frames(pt_frames: [Frame]) -> List[List[Frame]]:
            return [
                [
                    calibrate_frame(pt_frames[index], pt_devices[index])
                    for index in frames_order_group
                ]
                for frames_order_group in frames_order
            ]

        def concatenate_groups(frame_groups: List[List[Frame]]) -> List[Frame]:
            return [
                resize_frame(normalize_frame(np.concatenate(frame_groups[0], axis=1)), [size[0], size[1] // 2]),
                resize_frame(normalize_frame(np.concatenate(frame_groups[1], axis=1)), [size[0], size[1] // 2]),
            ]

    return size, mice_count, group_frames, concatenate_groups


def normalize_frame(frame: Frame) -> Frame:
    frame[np.where(frame < 0)] = 0
    frame_max, frame_min = np.max(frame), np.min(frame)
    frame = (frame - frame_min) / (frame_max - frame_min)
    frame[np.where(frame < 0)] = 0

    frame = (frame - np.mean(frame))
    frame[np.where(frame < 0)] = 0
    frame = (255 * frame / np.max(frame)).astype(np.uint8)

    return frame


def clear_pt_frame(frame):
    return frame[:-2]


def process_pt_frame(frame: Frame) -> Frame:
    return normalize_frame(
        clear_pt_frame(frame),
    )


def process_ir_frame(frame: Frame) -> Frame:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.normalize(frame, frame, 0, IR_ROUND_PIXEL, cv2.NORM_MINMAX)

    return frame


def get_temperatures(groups: List[List[Frame]]) -> List[List[int]]:
    return [
        [min([np.min(frame) for frame in group]), max([np.max(frame) for frame in group])]
        for group in groups
    ]


def resize_frame(frame: Frame, size: [int]) -> Frame:
    return cv2.resize(frame, tuple(size), interpolation=cv2.INTER_AREA)


def put_text(frame: Frame, coordinates: [int], text: str):
    cv2.putText(
        frame,
        text=text,
        org=tuple(coordinates),
        fontFace=cv2.FONT_ITALIC,
        fontScale=0.1,
        thickness=1,
        color=114,
    )


def show_frame(frame: Frame, index=''):
    cv2.imshow(f'streaming {index}', frame / np.max(frame))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise KeyboardInterrupt('stopping stream')


def int16_to_bytes(value: int, length: int = 2) -> bytes:
    return value.to_bytes(length, PT_PIXEL_BYTES_FORMAT)


def make_frame_buffer(temperatures: [[int]], frames: [Frame]) -> bytes:
    return BUFFER_FRAME_SEPARATOR.join(
        b''.join(map(int16_to_bytes, map(int, temperatures[index]))) + frame.astype(np.uint8).flatten().tostring()
        for index, frame in enumerate(frames)
    )
