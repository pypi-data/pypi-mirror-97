import os
from datetime import datetime
import cv2
import logging
import time

from src.device_class import DeviceGetter
from src.types import TemperatureFrames, FrameGenerator
from src.utils import \
    put_text, \
    get_temperatures, \
    get_frames_configuration, \
    clear_pt_frame
from src.constants import \
    BUFFER_FRAME_SEPARATOR, \
    PT_CAMERA_FOURCC, \
    TEXT_COORDINATES, \
    DATE_FORMAT


class ThermalCamera:
    def __init__(self, cameras_number: int):
        self.retries = 10

        self.pt_cameras = []
        self.pt_devices = []

        self.frame_size = None
        self.mice_count = None
        self.group_frames = None
        self.concatenate_groups = None

        self.cameras_number = cameras_number

        self.buffer_size = None

        is_connected = self.connect_devices()
        if not is_connected:
            logging.error('Couldn\'t connect to cameras')
            exit(-1)

        self.buffer_size = self.frame_size[0] * self.frame_size[1]\
                           + 4 * self.mice_count\
                           + len(BUFFER_FRAME_SEPARATOR) * (self.mice_count - 1)

    def connect_devices(self, is_retry=False):
        self.release_devices()
        if self.retries <= 0:
            return False

        if is_retry:
            self.retries -= 1
            logging.info('%s, RESETTING DEVICES, left: %s', datetime.utcnow(), self.retries)
            os.system('sudo trkir-usb-recycle > /dev/null 2>&1')
            time.sleep(5)

        devices = DeviceGetter.get_camera_devices()
        logging.info(devices)
        self.pt_devices = devices['PureThermal']
        if len(self.pt_devices) != self.cameras_number:
            logging.error('Should be {} cameras, found {}'.format(self.cameras_number, len(self.pt_devices)))
            self.connect_devices(is_retry=True)

        self.frame_size, self.mice_count, self.group_frames, self.concatenate_groups = get_frames_configuration(
            self.pt_devices,
        )
        if self.frame_size is None:
            logging.error('Cameras configuration not found')
            self.connect_devices(is_retry=True)
        try:
            for device in self.pt_devices:
                device_number = device['camera-device']
                cap = cv2.VideoCapture(int(device_number))
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*PT_CAMERA_FOURCC))
                cap.set(cv2.CAP_PROP_CONVERT_RGB, False)
                if not cap.isOpened():
                    logging.error('Cant\'t open %s device', device)
                    raise Exception

                self.pt_cameras.append(cap)
        except Exception as e:
            logging.exception(e)
            logging.info('Retries left %s', self.retries)
            self.connect_devices(is_retry=True)

        self.retries = 10
        return True

    def get_frame(self) -> TemperatureFrames:
        pt_frames = []
        while len(pt_frames) != len(self.pt_cameras):
            for cap in self.pt_cameras:
                frame = cap.read()[1]
                if frame is None:
                    pt_frames = []
                    self.connect_devices(is_retry=True)
                    break
                pt_frames.append(clear_pt_frame(frame))

        groups = self.group_frames(pt_frames)
        temperatures = get_temperatures(groups)
        frames = self.concatenate_groups(groups)

        now = datetime.utcnow()
        for frame in frames:
            put_text(
                frame,
                TEXT_COORDINATES,
                now.strftime(DATE_FORMAT),
            )

        return temperatures, frames

    def release_devices(self):
        for cap in self.pt_cameras:
            try:
                cap.release()
            except Exception:
                continue
        cv2.destroyAllWindows()
        self.pt_cameras = []

    def streaming(self) -> FrameGenerator:
        while True:
            yield self.get_frame()
