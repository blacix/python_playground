import os
import signal
import subprocess

COMMAND = r"c:\Program Files\SEGGER\JLink\JLinkRTTLogger.exe"
LOG_FILE = r"d:\log.log"
# COMMAND_ARGS = f"-Device NRF52840_XXAA -If SWD -Speed 4000 -RTTChannel 0 {LOG_FILE}"
COMMAND_ARGS = ["-Device", "NRF52840_XXAA", "-If", "SWD", "-Speed", "4000", "-RTTChannel", "0", LOG_FILE]

if __name__ == '__main__':
    print('hello')
    os.remove("d:\\log.log")
    os.chdir(r"c:\Program Files\SEGGER\JLink")
    process = subprocess.Popen([COMMAND] + COMMAND_ARGS)
    print(process.pid)
    cnt = 0
    while True:
        cnt = cnt + 1
