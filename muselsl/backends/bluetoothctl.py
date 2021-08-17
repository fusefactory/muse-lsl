import atexit
import time


def sleep(seconds):
    time.sleep(seconds)


def _list_muses_bluetoothctl(timeout, verbose=False):
    """Identify Muse BLE devices using bluetoothctl.

    When using backend='gatt' on Linux, pygatt relies on the command line tool
    `hcitool` to scan for BLE devices. `hcitool` is however deprecated, and
    seems to fail on Bluetooth 5 devices. This function roughly replicates the
    functionality of `pygatt.backends.gatttool.gatttool.GATTToolBackend.scan()`
    using the more modern `bluetoothctl` tool.

    Deprecation of hcitool: https://git.kernel.org/pub/scm/bluetooth/bluez.git/commit/?id=b1eb2c4cd057624312e0412f6c4be000f7fc3617
    """
    try:
        import pexpect
    except (ImportError, ModuleNotFoundError):
        msg = ('pexpect is currently required to use bluetoothctl from within '
               'a jupter notebook environment.')
        raise ModuleNotFoundError(msg)

    # Run scan using pexpect as subprocess.run returns immediately in jupyter
    # notebooks
    print('Searching for Muses, this may take up to 10 seconds...')
    scan = pexpect.spawn('bluetoothctl scan on')
    try:
        scan.expect('foooooo', timeout=timeout)
    except pexpect.EOF:
        before_eof = scan.before.decode('utf-8', 'replace')
        msg = f'Unexpected error when scanning: {before_eof}'
        raise ValueError(msg)
    except pexpect.TIMEOUT:
        if verbose:
            print(scan.before.decode('utf-8', 'replace').split('\r\n'))

    # List devices using bluetoothctl
    list_devices_cmd = ['bluetoothctl', 'devices']
    devices = subprocess.run(
        list_devices_cmd, stdout=subprocess.PIPE).stdout.decode(
            'utf-8').split('\n')
    muses = [{
            'name': re.findall('Muse.*', string=d)[0],
            'address': re.findall(r'..:..:..:..:..:..', string=d)[0]
        } for d in devices if 'Muse' in d]
    _print_muse_list(muses)

    return muses


class Adapter:

    def __init__(self, *args, **kwargs):
        self.connected = set()
        atexit.register(self.stop)

    def start(self):
        pass

    def stop(self):
        pass

    def scan(self, timeout=10):
        return _list_muses_bluetoothctl(timeout)

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

