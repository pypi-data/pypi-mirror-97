#!/usr/local/bin/python3

"""
    Get camera devices by type (PT and IR)
"""

import re
import subprocess

from src.constants import \
    CALIBRATION_MAP, \
    DEVICE_TYPES


class DeviceGetter:
    @staticmethod
    def get_usb_part__(line):
        # example: TODO
        return line.split(' ')[-1][1:-2]

    @staticmethod
    def get_usb_hub__(line):
        return line.split('-')[1].split('.')[0]

    @staticmethod
    def get_usb_port__(line):
        return line.split('-')[-1]

    @staticmethod
    def get_camera_device__(line):
        return line.replace('\t', '').replace('/dev/video', '')

    @staticmethod
    def get_device_serial_number__(device_number: int):
        serial_number = re.findall(
            '(?<=ID_SERIAL_SHORT=).*$',
            subprocess \
                .run(
                    f'sudo udevadm info --query=all /dev/video{device_number} | grep "ID_SERIAL_SHORT"',
                    shell=True,
                    stdout=subprocess.PIPE,
                ) \
                .stdout \
                .decode('utf-8')
                .replace('\n', ''),
        )[0]

        return serial_number

    @staticmethod
    def get_camera_calibration_values__(serial_number: str):
        if serial_number in CALIBRATION_MAP:
            return {
                key: int(value * 100)
                for key, value in CALIBRATION_MAP[serial_number].items()
            }

        return {
            key: int(value * 100)
            for key, value in CALIBRATION_MAP['default'].items()
        }

    @staticmethod
    def get_camera_devices():
        result = subprocess \
            .run(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE) \
            .stdout \
            .decode('utf-8') \
            .split('\n')

        groupped_by_device = {
            device: []
            for device in DEVICE_TYPES
        }
        for index, line in enumerate(result[:-1]):
            for device in DEVICE_TYPES:
                if device in line:
                    camera_device = DeviceGetter.get_camera_device__(result[index + 1])
                    serial_number = DeviceGetter.get_device_serial_number__(camera_device)
                    groupped_by_device[device].append({
                        'usb-hub': DeviceGetter.get_usb_hub__(DeviceGetter.get_usb_part__(line)),
                        'usb-port': DeviceGetter.get_usb_port__(DeviceGetter.get_usb_part__(line)),
                        'camera-device': camera_device,
                        'serial-number': serial_number,
                        'calibration-values': DeviceGetter.get_camera_calibration_values__(serial_number),
                    })

        for device in DEVICE_TYPES:
            groupped_by_device[device] = sorted(
                groupped_by_device[device],
                key=lambda item: (item['usb-hub'], item['usb-port']),
            )

        return groupped_by_device
