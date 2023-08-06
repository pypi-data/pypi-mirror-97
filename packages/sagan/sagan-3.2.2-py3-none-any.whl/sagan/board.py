import subprocess
from subprocess import PIPE

def checkVersion():
    cp = subprocess.run(["i2cdetect", "-y", "1"], stdout=PIPE)
    stdoutstr = str(cp.stdout)
    if "1e" in stdoutstr:
        return "4"
    if "1d" in stdoutstr:
        return "3"
    return "unknown"