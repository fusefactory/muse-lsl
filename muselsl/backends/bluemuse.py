import atexit
import time
import subprocess


def sleep(seconds):
    time.sleep(seconds)


class Adapter:

    def __init__(self, *args, **kwargs):
        self.connected = set()
        atexit.register(self.stop)

    def start(self):
        pass

    def stop(self):
        pass

    def scan(self, timeout=10):
        print("Starting BlueMuse, see BlueMuse window for interactive list of devices.")
        subprocess.call("start bluemuse:", shell=True)
        return []

    def connect(self, address):
        raise NotImplemented()


class Device:

    def __init__(self, adapter, address):
        self._adapter = adapter
        self._address = address

    def connect(self):
        raise NotImplemented()

    def disconnect(self):
        raise NotImplemented()

    def char_write_handle(self, value_handle, value, wait_for_response=True, timeout=30):
        raise NotImplemented()

    def subscribe(self, uuid, callback=None, indication=False, wait_for_response=True):
        raise NotImplemented()

