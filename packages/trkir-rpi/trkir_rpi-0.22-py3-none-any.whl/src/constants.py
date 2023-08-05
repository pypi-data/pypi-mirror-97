MAX_WORKERS = 4

# socket
SOCKET_SERVER = ('0.0.0.0', 8081)
SOCKET_MAX_CONNECTIONS = 1
SOCKET_RECV_LENGTH = 9

# camera
FPS = 3
TEXT_COORDINATES = [5, 15]
PT_CAMERA_FOURCC = 'Y16 '
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# round pixels
IR_ROUND_PIXEL = 180

# formatting
PT_PIXEL_BYTES_FORMAT = 'big'
FRAME_ENCODING_FORMAT = '.jpg'

BUFFER_FRAME_SEPARATOR = b'\n\r\n\r'

MAX_FRAME_PIXEL = 34 * 100 + 27315
MIN_FRAME_PIXEL = 25 * 100 + 27315


DEVICE_TYPES = ['PureThermal', 'USB 2.0 Camera']

CALIBRATION_MAP = {
    # Prod 1
    '80060026-5113-3538-3930-383900000000': {'min': -7.43, 'max': -7},  # top left
    '0019002d-5113-3538-3930-383900000000': {'min': -7.16, 'max': -5.71},  # top right
    '8021002d-5110-3039-3433-373300000000': {'min': -4.66, 'max': -3.91},  # bottom left
    '80110004-5113-3538-3930-383900000000': {'min': -7.78, 'max': -9.1},  # bottom right

    # Prod 2
    '80210005-5113-3538-3930-383900000000': {'min': -7.05, 'max': -6.89},  # top left
    '00160004-5113-3538-3930-383900000000': {'min': -4.97, 'max': -4.74},  # top right
    '8001001e-510a-3138-3533-373900000000': {'min': -4.59, 'max': -5.29},  # bottom left
    '00158002-5113-3538-3930-383900000000': {'min': -5.89, 'max': -6.46},  # bottom right

    # Prod 3
    '00188003-5113-3538-3930-383900000000': {'min': -5.64, 'max': -6.25},  # top left
    '80160027-5112-3039-3433-373300000000': {'min': -3.41, 'max': -3.75},  # top right
    '00040030-5113-3538-3930-383900000000': {'min': -4.22, 'max': -5.57},  # bottom left
    '80040006-5113-3538-3930-383900000000': {'min': -9.61, 'max': -9},  # bottom right

    # Prod 4
    '80190008-5113-3538-3930-383900000000': {'min': -7.59, 'max': -7.9},  # top left
    '80108002-5113-3538-3930-383900000000': {'min': -6.28, 'max': -7.87},  # top right
    '00038001-510a-3138-3533-373900000000': {'min': -8.07, 'max': -7.16},  # bottom left
    '001f002e-5113-3538-3930-383900000000': {'min': -4.31, 'max': -5.05},  # bottom right

    'default': {'min': 0, 'max': 0},
}
