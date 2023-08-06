import os
import sys
import json

_FIFO = open(os.environ.get('TELEMETRY', '/dev/null'), 'w')


class Telemetry:
    @staticmethod
    def update(prefix: str, data: str):
        try:
            _FIFO.write("{}:{}\n".format(prefix[0:3], json.dumps(data)))
            _FIFO.flush()
        except BaseException as err:
            print("Telemetry.update: {}".format(err), file=sys.stderr)
            return False
        return True
