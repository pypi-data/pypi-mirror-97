import unittest
import logging
import time
from ftdi_serial import Serial
from north_utils.test import assert_equal, assert_float_equal
from north_c9.controller import C9Controller
from north_c9.serial import C9SerialDevice
from north_devices.pumps.tecan_cavro import TecanCavro
from north_devices.scales.scientech_zeta import ScientechZeta

logging.basicConfig(level=logging.WARNING)
# logging.basicConfig(level=logging.DEBUG)

# C9_SERIAL = 'DA1FUC12'  # Propeller Quickstart board
# C9_SERIAL = 'A505PCDE'  # C9 Dev board
# C9_SERIAL = 'FT2FVF6U'  # C9 Network
C9_SERIAL = 'FT3FM1O1'
CLIENT_SERIAL = 'FTU9RIS7'
# CLIENT_SERIAL = 'FT2FVF6U'
COM_PORT = 1


class ComTestCase(unittest.TestCase):
    c9: C9Controller = None
    client: Serial = None

    @classmethod
    def setUpClass(cls):
        # cls.c9 = C9Controller(device_serial=C9_SERIAL, debug_protocol=True)
        cls.c9 = C9Controller(device_serial=C9_SERIAL)
        cls.client = Serial(device_serial=CLIENT_SERIAL)
        try:
            cls.c9.com_init(COM_PORT, 115200)
            time.sleep(1)
        except Exception as err:
            print(err)

    @classmethod
    def tearDownClass(cls):
        cls.c9.disconnect()
        cls.client.disconnect()

    def setUp(self):
        self.c9.com_init(COM_PORT, 115200)
        self.client.flush()
        self.c9.com_flush(COM_PORT)
        time.sleep(1)

    def test_flush(self):
        self.client.write(b'1234')
        size = self.c9.com_rx_size(COM_PORT)
        assert_equal(size, 4)
        self.c9.com_flush(COM_PORT)
        size = self.c9.com_rx_size(COM_PORT)
        assert_equal(size, 0)

    def test_size(self):
        message = b'test'
        self.client.write(message)
        time.sleep(0.1)
        size = self.c9.com_rx_size(COM_PORT)
        assert_equal(size, len(message))

    def test_read(self):
        message = b'foobar'
        self.client.write(message)
        time.sleep(0.1)
        data = self.c9.com_read(COM_PORT, len(message))
        assert_equal(data, message)

    def test_write(self):
        message = b'testing'
        self.c9.com_write(COM_PORT, message)
        time.sleep(0.1)
        data = self.client.read()
        assert_equal(data, message)

    def test_binary(self):
        self.client.set_parameters(baudrate=9600)
        self.c9.com_init(COM_PORT, 9600)

        message = b'\x0213k50R\x03?'
        self.c9.com_write(COM_PORT, message)
        time.sleep(0.1)
        data = self.client.read()
        assert_equal(data, message)
        time.sleep(0.1)
        message = b'\x0213k50R\x03?'
        self.client.write(message)
        time.sleep(0.1)
        data = self.c9.com_read(COM_PORT, len(message))
        assert_equal(data, message)

    def test_serial_device(self):
        device = C9SerialDevice(self.c9, COM_PORT)
        serial = Serial(device=device)

        message = b'test'
        serial.write(message)
        time.sleep(0.1)
        data = self.client.read()
        assert_equal(data, message)

        message = b'cool'
        self.client.write(message)
        time.sleep(0.1)
        data = serial.read()
        assert_equal(data, message)

    def test_request(self):
        serial = Serial(device=C9SerialDevice(self.c9, COM_PORT))

        request = b'request\r'
        response = b'response\r\n'
        self.client.write(response)
        time.sleep(0.1)
        response_data = serial.request(request, line_ending=b'\r\n')
        time.sleep(0.1)
        request_data = self.client.read()
        assert_equal(response_data, response.strip())
        assert_equal(request_data, request)

    def test_init(self):
        self.client.set_parameters(baudrate=9600)
        self.c9.com_init(COM_PORT, 9600)

        message = b'foobar'
        self.client.write(message)
        time.sleep(0.1)
        data = self.c9.com_read(COM_PORT, len(message))
        assert_equal(data, message)

        self.c9.com_init(COM_PORT, 115200)

    def test_cavro(self):
        serial = Serial(device=C9SerialDevice(self.c9, 0), baudrate=9600)
        cavro = TecanCavro(serial, 1)

        cavro.home()

        # Test dispense
        cavro.dispense_ml(0.1, 1, 2, velocity_ml=2)
        cavro.dispense_ml(0.5, 1, 2, velocity_counts=500)
        cavro.dispense_ml(2.5, 1, 2)

        # test velocity
        cavro.move_absolute_counts(1400, velocity_counts=500)
        cavro.move_absolute_counts(0)

        # test loop
        cavro.loop_start()
        cavro.move_absolute_counts(1000)
        cavro.move_absolute_counts(0)
        cavro.loop_end(2)
        cavro.execute()

    def test_cavro_network(self):
        serial = Serial(device=C9SerialDevice(self.c9, 0), baudrate=9600)
        cavro_a = TecanCavro(serial, 0)
        cavro_b = TecanCavro(serial, 1)

        TecanCavro.home_all()

        cavro_a.dispense_ml(0.5, 1, 2, wait=False)
        cavro_b.dispense_ml(0.5, 1, 2)

    def test_scale(self):
        serial = Serial(device=C9SerialDevice(self.c9, 1), baudrate=9600)
        scale = ScientechZeta(serial)
        scale.tare()
        weight = scale.weigh()
        assert_float_equal(weight, 0, diff=0.1)

    def test_cavro_and_scale(self):
        cavro = TecanCavro(self.c9.com(0), address=0)
        scale = ScientechZeta(self.c9.com(1))

        while True:
            cavro.home()
            scale.tare()
            scale.weigh()
            cavro.dispense_ml(0.1, 1, 2, velocity_ml=2)
            scale.tare()
            scale.weigh()
            cavro.dispense_ml(0.5, 1, 2, velocity_counts=500)
            scale.tare()
            scale.weigh()
            cavro.dispense_ml(2.5, 1, 2)