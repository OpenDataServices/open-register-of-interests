import os
import sys
import threading
import time


# Spinner - Michael Wood - Toaster - lsupdates GPLv2
class Spinner(threading.Thread):
    """ A simple progress spinner to indicate download/parsing is happening"""

    def __init__(self, *args, **kwargs):
        super(Spinner, self).__init__(*args, **kwargs)
        self.setDaemon(True)
        self.signal = True

    def run(self):
        # Only show the spinner if in we're in an actual terminal.
        # Saves filling the log file up with characters.
        if os.environ.get("TERM") is None:
            return

        os.system("setterm -cursor off")
        while self.signal:
            for char in ["/", "-", "\\", "|"]:
                sys.stdout.write("\r" + char)
                sys.stdout.flush()
                time.sleep(0.25)
        os.system("setterm -cursor on")

    def stop(self):
        self.signal = False
