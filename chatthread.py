import threading


class ChatThread(threading.Thread):
    def __init__(self, sleep_time=0.1, func=None):
        self._stop_event = threading.Event()
        self._sleep_time = sleep_time
        self.func = func

        """call base class constructor"""
        super().__init__()

    def run(self):
        """main control loop"""
        while not self._stop_event.is_set():
            # do work
            self.func()
            self._stop_event.wait(self._sleep_time)

    def join(self, timeout=None):
        """set stop event and join within a given time period"""
        self._stop_event.set()
        super().join(timeout)
