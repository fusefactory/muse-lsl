import atexit
import time
import pygatt


def sleep(seconds):
    time.sleep(seconds)


class Adapter:

    def __init__(self, interface, *args, **kwargs):
        self.connected = set()
        atexit.register(self.stop)
        self.adapter = pygatt.GATTToolBackend(interface)
        self.backend_name = "gatt"

    def start(self):
        self.adapter.start()

    def stop(self):
        self.adapter.stop()

    def scan(self, timeout=10):
        devices = self.adapter.scan(timeout=timeout)
        return devices

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

