from ftdi_serial import Device, SerialDeviceNotImplementedException
from north_c9.controller import C9Controller


class C9SerialDevice(Device):
    def __init__(self, controller: C9Controller, port: int):
        Device.__init__(self)
        self.controller = controller
        self.port = port
        self.read_timeout = 1000

    def clear(self):
        self.controller.com_flush(self.port)

    def set_baud_rate(self, baudrate: int):
        self.controller.com_init(self.port, baudrate)

    def set_timeouts(self, read_timeout: float, write_timeout: float):
        self.read_timeout = read_timeout

    def set_parameters(self, data_bits: int, stop_bits: int, parity_bits: int):
        if data_bits != 8 or stop_bits not in (0, 1, 2) or parity_bits != 0:
            raise SerialDeviceNotImplementedException(f'C9 serial devices only support 8 data bits, 1 stop bit and no parity')

    def get_input_size(self) -> int:
        return self.controller.com_rx_size(self.port)

    def get_output_size(self) -> int:
        raise SerialDeviceNotImplementedException(f'Cannot read output buffer size on C9 serial devices')

    def write(self, data: bytes):
        super().write(data)
        self.controller.com_write(self.port, data)

    def read(self, num_bytes: int, raw: bool = True) -> bytes:
        return self.controller.com_read(self.port, num_bytes)
