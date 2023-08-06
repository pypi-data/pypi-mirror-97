import subprocess
from .telemetry import Telemetry
from collections import namedtuple
from datetime import datetime
import base64

CAPTURE_EXECUTABLE = 'ov2640_capture'

resolutions = [
    (160, 120),
    (176, 144),
    (320, 240),
    (352, 288),
    (640, 480),
    (800, 600),
    (1024, 768),
    (1280, 960),
    (1600, 1200),
]

X_RESOLUTION = resolutions[5][0]
Y_RESOLUTION = resolutions[5][1]

CameraCaptureResult = namedtuple(
    'CameraCaptureResult',
    'filename'
)


def _image_to_string(filename=None):
    if filename is not None:
        try:
            with open(filename, 'rb') as imgText:
                result = "START_BASE_64{}END_BASE_64".format(base64.b64encode(imgText.read()))
                return result
        except FileNotFoundError:
            pass
    return "error"


class Camera:
    def capture(self, filename=None, width=X_RESOLUTION, height=Y_RESOLUTION):

        if not filename:
            filename = '{}.jpg'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

        if len(filename) > 4 and filename[-4:] != '.jpg':
            filename += '.jpg'

        command = '{} -c {} {}x{}'.format(
            CAPTURE_EXECUTABLE,
            filename,
            width,
            height
        )

        status = subprocess.call(command, shell=True)
        packet = {
            "src": _image_to_string(filename)
        }
        Telemetry.update("cam", packet)
        camera_result = CameraCaptureResult(filename)
        assert status == 0, "Failed to capture image with command {}".format(command)
        return camera_result

    def capture_low(self, filename=None):
        return self.capture(filename=filename, width=resolutions[2][0], height=resolutions[2][1])

    def capture_moderate(self, filename=None):
        return self.capture(filename=filename, width=resolutions[5][0], height=resolutions[5][1])

    def capture_high(self, filename=None):
        return self.capture(filename=filename, width=resolutions[8][0], height=resolutions[8][1])
