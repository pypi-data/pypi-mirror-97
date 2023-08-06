from typing import Optional, List, Any, Dict, Union, Tuple, Iterable, NamedTuple
import time
import random
import logging
from threading import Lock
from ftdi_serial import Serial, Device, SerialException, SerialReadTimeoutException
from north_utils.crc import build_c9_crc

logger = logging.getLogger(__name__)


C9_NUM_AXIS = 10
C9_FLAG_AXIS_MOVING = '1'
C9_AXIS_MOVING_SLEEP_TIME = 0.001


FlagsDict = Dict[str, Union[int, bytes, float]]


class C9ControllerError(Exception):
    """
    Base Exception class for C9Controller errors
    """
    pass


class C9Error(C9ControllerError):
    """
    Errors sent from the C9 Controller
    """

    SUCCESS = 0
    TIMEOUT = 1
    INVALID_COMMAND = 2
    INVALID_ARGUMENT = 3
    INVALID_SEPARATOR = 4
    TOO_MANY_ARGUMENTS = 5
    CMD_NOT_FOUND = 6
    INVALID_ARGUMENTS = 7
    INVALID_AXIS = 8
    INVALID_POSITION = 9
    INVALID_VELOCITY = 10
    INVALID_ACCELERATION = 11
    AXIS_MOVING = 12
    EEPROM_READ = 13
    EEPROM_WRITE = 14
    AXIS_FEATURE_UNAVAILABLE = 15
    MODBUS_TIMEOUT = 16
    MODBUS_INVALID_RESPONSE = 17
    INVALID_TEMP_CONT = 18
    INVALID_JOINT = 19
    INVALID_CRC = 20
    HOMING = 21
    SCALE_ERROR = 34

    CONTROLLER_DEADLOCK = 50

    def __init__(self, error_number, error_message, *args, **kwargs):
        super().__init__(error_message, *args, **kwargs)
        self.error_number = error_number


class C9ResponseError(C9ControllerError):
    """
    Response errors
    """
    pass


def dict_to_value_list(items: Dict[Any, Any]) -> List[Any]:
    """
    Convert a dictionary into a flattened value list containing keys and values in sequence

    :param items: dictionary to convert
    :return: list with keys and values from items dictionary
    """

    values = []
    for k, v in items.items():
        values += [k, v]

    return values


def retry_timeout_scale(total_retries: int, remaining: int, scale: float=0.3) -> float:
    """
    Calculate an exponential retry timeout based on the max and remaining number of retries

    :param total_retries: total number of retries allowed
    :param remaining: number of retries remaining
    :param scale: optional scale for exponential, defaults to 0.3
    :return: retry timeout in seconds
    """

    return 2 ** ((total_retries - remaining) * scale)


class C9ControllerStats:
    def __init__(self):
        self.requests: int = 0
        self.responses: int = 0
        self.commands: int = 0
        self.errors: int = 0
        self.error_types: Dict[int, int] = {}

    @property
    def error_types_str(self):
        return ', '.join([f'{k}={v}' for k, v in self.error_types.items()])

    def add_error(self, error: Exception):
        error_number = getattr(error, 'error_number', -1)
        self.error_types[error_number] = self.error_types.get(error_number, 0) + 1


class C9Controller:
    """
    C9Controller is the main class used to communicate with the North C9
    """

    NUM_MAIN_AXES = 4

    BIAS_MIN_SHOULDER = 0
    """ Bias arm position to keep the shoulder near the center """
    BIAS_MAX_SHOULDER = 1
    """ Bias arm position to keep the shoulder away from the center """
    BIAS_CLOSEST = 2
    """ Bias arm by keeping new positions as close to the old position as possible, avoids large elbow swings """

    AXIS_GRIPPER = 0
    """ Gripper axis number """
    AXIS_ELBOW = 1
    """ Elbow axis number """
    AXIS_SHOULDER = 2
    """ Shoulder axis number """
    AXIS_COLUMN = 3
    """ Column axis number """
    AXIS_CAROUSEL = 4
    """ Carousel axis number """

    RETRY_ERRORS = [
        C9Error.INVALID_CRC,
        C9Error.INVALID_ARGUMENT,
        C9Error.INVALID_ARGUMENTS,
        C9Error.INVALID_SEPARATOR,
        C9Error.INVALID_COMMAND,
        C9Error.CMD_NOT_FOUND,
    ]

    default_controller = None
    locks: Dict[Device, Lock] = {}

    @classmethod
    def get_lock(cls, device: Device):
        if device in cls.locks:
            return cls.locks[device]

        cls.locks[device] = Lock()
        return cls.locks[device]

    def __init__(self,
                 connection: Serial=None,
                 address: Optional[int]=1,
                 device: Device=None,
                 device_serial: str=None,
                 device_number: int=None,
                 home: bool=False,
                 connect: bool=True,
                 write_timeout: float=0.5,
                 read_timeout: float=0.5,
                 retry_timeout: float=0.5,
                 lock_timeout: float=120,
                 move_wait_delay: float=0.1,
                 move_wait_scale: float=0.8,
                 move_prediction: bool=True,
                 retries: int=10,
                 command_delay: float=0.0015,
                 debug_protocol: bool=False,
                 paused: bool=False,
                 use_joystick: bool=True,
                 ignore_missing_joystick: bool=True,
                 verbose=False) -> None:
        """
        Create an instance of C9Controller.

        :param connection: optional Serial connection to use for communication (a Serial connection will be created if needed)
        :param device: optional Serial Device to use when creating the Serial connection
        :param device_serial: serial number of the FTDI device to connect to, will connect to first device if not given
        :param device_number: index of the FTDI serial device to connect to, device_serial should be used when possible
        :param home: home the robot connected to the C9, defaults to False
        :param connect: send a ping command after creation to check C9 controller connection
        :param write_timeout: timeout to use when writing data to the serial connection, defaults to 0.5s
        :param read_timeout: timeout to use when reading data from the serial connection, defaults to 0.5s
        :param retry_timeout: amount of time to wait between retrying failed commands, defaults to 0.5s
        :param lock_timeout: the amount of idle time needed to trigger a deadlock error
        :param move_wait_delay: an estimate of the delay in sending a command to the C9, used for movement duration prediction
        :param move_wait_scale: a percentage used to scale the estimated movement duration to ensure we undershoot it
        :param move_prediction: enable move prediction, defaults to True. This will sleep while the robot is moving to reduce protocol chatter
        :param retries: the number of times to retry a failed command, defaults to 10
        :param command_delay: the delay between sending a command and releasing the lock for threading
        :param debug_protocol: use the simpler debug protocol without CRCs if True. This is needed when connecting to a C9 using the USB port
        :param paused: pause sending commands if True, will resume when paused is reset to False
        :param use_joystick: create a joystick instance if True, defaults to True
        :param ignore_missing_joystick: ignore errors from missing joysticks
        """
        try:
            self.connection = connection if connection is not None else \
                Serial(device=device, device_serial=device_serial, device_number=device_number, connect=connect,
                       read_timeout=read_timeout, write_timeout=write_timeout)
        except SerialException as err:
            if self.connection and self.connection.device is not None:
                self.connection.device.close()
            raise err

        self.logger = logger.getChild(self.__class__.__name__)
        self.device_logger = logger.getChild(self.__class__.__name__ + '.device')
        self.network_address = address
        self.axis_handlers = {}
        self.output_handlers = {}
        self.verbose = verbose
        self.command_error_count = {}
        self.retries = retries
        self.read_timeout = read_timeout
        self.write_timeout = write_timeout
        self.retry_timeout = retry_timeout
        self.lock_timeout = lock_timeout
        self.move_wait_delay = move_wait_delay
        self.move_wait_scale = move_wait_scale
        self.move_prediction = move_prediction
        self.sequence_number = random.choice(range(1, 99))
        self.debug_protocol = debug_protocol
        self.paused = paused
        self.lock = self.get_lock(self.connection.device)
        self.command_delay = command_delay
        self.stats = C9ControllerStats()

        if connect:
            try:
                self.ping()
            except C9Error:
                if not self.debug_protocol:
                    self.debug_protocol = True
                    self.ping()

        if C9Controller.default_controller is None:
            C9Controller.default_controller = self

        if use_joystick:
            from north_c9.joysticks import N9Joystick
            self.joystick = N9Joystick(self, ignore_missing_joystick=ignore_missing_joystick)

        if home:
            self.home()

    def connect(self):
        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()
        if self.joystick.running:
            self.joystick.stop()

    def is_aux_axis(self, axis):
        return axis >= self.NUM_MAIN_AXES

    def encode_command(self, name: str, flags_dict: FlagsDict, args: List[Any], sequence_number: int):
        args = [arg for arg in args if arg is not None]
        command = [name]
        command += self.build_flags(flags_dict)
        command += [str(round(arg)) for arg in args if arg is not None]
        command_str = ' '.join(command) + '\r'

        if not self.debug_protocol:
            command_str = str(sequence_number) + ' ' + command_str
            crc = build_c9_crc(command_str.encode()).decode()
            header_str = ' '.join([f'@{self.network_address}', '99', crc])
            command_str = header_str + ' ' + command_str

        return command_str.encode()

    def request_command(self, name: str, args: Iterable[Any]=[], flags: Dict[str, bool]={}, timeout: Optional[float]=None,
                        retries: Optional[int]=None, sequence_number: Optional[int]=None, reset_sequence: bool=False) -> str:
        if self.paused:
            while self.paused:
                time.sleep(0.5)

        if retries is None:
            retries = self.retries

        if sequence_number is None or reset_sequence:
            sequence_number = self.sequence_number
            self.sequence_number = (self.sequence_number + 1) % 98 + 1

        command = self.encode_command(name, flags, args, sequence_number)

        self.logger.debug(f'Sending command: name={name}, args={args}, flags={flags}, retries={retries}, raw: {command}')
        self.stats.requests += 1
        self.stats.commands += 1

        try:
            crc_fail = False

            if not self.lock.acquire(timeout=self.lock_timeout):
                self.logger.critical(f'Controller {self.network_address} deadlocked')
                raise C9Error(C9Error.CONTROLLER_DEADLOCK, f'Controller {self.network_address} deadlocked')

            self.connection.write(command, timeout=self.write_timeout)
            response = self.connection.read_line(line_ending=b'\r\n', timeout=timeout or self.read_timeout)
            time.sleep(self.command_delay)
            self.lock.release()

            self.logger.debug(f'Response received: {response}')
            self.stats.responses += 1

            if not self.debug_protocol:
                try:
                    response, crc = response.rsplit(b'\r', 1)
                    response = response.strip(b'\r\x00')
                    response_crc = build_c9_crc(response + b'\r')
                    crc_fail = response_crc != crc.strip()
                except ValueError:
                    crc_fail = True

            try:
                # strip out any log statements
                lines = response.split(b'\r')
                logs = [line for line in lines if line.startswith(b'|')]
                response_lines = [line for line in lines if not line.startswith(b'|')]
                response = b'\n'.join(response_lines).strip().decode()

                self.logger.debug(f'Response received: "{response}"')

                for log in logs:
                    self.device_logger.info(log.lstrip(b'|').decode())

            except UnicodeDecodeError:
                crc_fail = True

            if crc_fail or response.startswith('ERROR'):
                if crc_fail:
                    error_number = C9Error.INVALID_CRC
                    error_message = 'Invalid response CRC'
                else:
                    error_number, error_message = response.strip('ERROR ').split(':')

                error = C9Error(int(error_number), error_message.strip())

                self.stats.add_error(error)

                self.logger.warning(f'Response error: {error}')
                self.logger.debug(f'Errors: {self.stats.error_types_str}')

                if int(error_number) in self.RETRY_ERRORS and retries > 0:
                    return self.request_command(name, args, flags, timeout=timeout, retries=retries - 1, sequence_number=sequence_number, reset_sequence=reset_sequence)

                self.logger.error(f'Response error: [{error_number}] {error_message}')

                raise error

            return response

        except SerialException as error:
            self.lock.release()

            if retries == 0:
                self.logger.error(f'Serial error: {error}')
                raise error

            self.stats.add_error(error)

            self.logger.warning(f'Serial error: {error}')
            self.logger.debug(f'Errors: {self.stats.error_types_str}')

            timeout = retry_timeout_scale(self.retries, retries) * self.retry_timeout
            self.logger.debug(f'Retry timeout: {timeout}')
            time.sleep(timeout)

            return self.request_command(name, args, flags, timeout=timeout, retries=retries - 1, sequence_number=sequence_number, reset_sequence=reset_sequence)

    def register_output_handler(self, event, output, handler):
        if output not in self.output_handlers:
            self.output_handlers[output] = {}

        if event not in self.output_handlers[output]:
            self.output_handlers[output][event] = []

        self.output_handlers[output][event].append(handler)

    def dispatch_output_event(self, event, output: Optional[int]=None, *args, **kwargs):
        # if we weren't supplied an output, dispatch event to all handlers
        if output is None:
            for output, event_handlers in self.output_handlers.items():
                for handler in event_handlers.get(event, []):
                    handler(*args, **kwargs)
            return

        # otherwise look up the handler using the output and event
        if output not in self.output_handlers:
            return

        if event not in self.output_handlers[output]:
            return

        for handler in self.output_handlers[output][event]:
            handler(*args, **kwargs)

    def register_axis_handler(self, event, axis, handler):
        if axis not in self.axis_handlers:
            self.axis_handlers[axis] = {}

        if event not in self.axis_handlers[axis]:
            self.axis_handlers[axis][event] = []

        self.axis_handlers[axis][event].append(handler)

    def dispatch_axis_event(self, event, axis: Optional[int]=None, *args, **kwargs):
        # if we weren't supplied an axis, dispatch event to all handlers
        if axis is None:
            for axis, event_handlers in self.axis_handlers.items():
                for handler in event_handlers.get(event, []):
                    handler(*args, **kwargs)
            return

        # otherwise look up the handler using the axis and event
        if axis not in self.axis_handlers:
            return

        if event not in self.axis_handlers[axis]:
            return

        for handler in self.axis_handlers[axis][event]:
            handler(*args, **kwargs)

    def dispatch_axes_events(self, event, axes, *args, **kwargs):
        for axis in axes:
            self.dispatch_axis_event(event, axis, *args, **kwargs)

    def dispatch_position_events(self, axes, positions):
        axes_list = list(axes)
        for i in range(0, len(positions)):
            pass
            self.dispatch_axis_event('position', axes_list[i], int(positions[i]))

    def build_arm_args(self, x, y, z=None, gripper=None, velocity=None, acceleration=None):
        args = [x * 1000, y * 1000]

        if z is not None:
            args.append(z * 1000)

        if gripper is not None:
            args.append(gripper * 1000)

        if velocity is not None or acceleration is not None:
            if z is None:
                raise C9Error('ARMA command does not support velocity and acceleration without a z argument')
            if velocity is None or acceleration is None:
                raise C9Error('Both velocity and acceleration required')

            args += [velocity, acceleration]

        return args

    def build_flags(self, flags_dict: FlagsDict) -> List[str]:
        flags = []

        for flag, value in flags_dict.items():
            if isinstance(value, bool):
                if value:
                    flags.append(f'/{flag} 1')
            elif isinstance(value, float):
                flags.append(f'/{flag} {round(value)}')
            elif value is not None:
                flags.append(f'/{flag} {value}')

        return flags

    # Basic protocol
    def info(self) -> str:
        """
        Returns the firmware name and version of the connected C9 controller
        """
        return self.request_command('INFO')

    def calibration(self, *, dangerously_set_calibration: Optional[Tuple[int, int, int, int]]=None) -> List[int]:
        calibration = []

        if dangerously_set_calibration is not None:
            for axis in range(0, len(dangerously_set_calibration)):
                calibration.append(int(self.request_command('CALI', [axis, dangerously_set_calibration[axis]])))
                self.wait_for_axis(axis)
        else:
            for axis in range(0, 4):
                calibration.append(int(self.request_command('CALI', [axis])))

        return calibration

    def ping(self, timeout: float=1.0, retries: int=5):
        """
        Sends a ping to the C9 controller, used to test connection
        """
        self.request_command('PING', timeout=timeout, retries=retries, reset_sequence=True)

    def address(self, new_address: int=None) -> int:
        """
        Return the address of the connected C9 controller, changing it to a new address if given

        :param new_address: optional new address to use for C9 controller
        :return: address of connected C9 controller
        """
        address = int(self.request_command('ADDR', [new_address]))
        if new_address is not None:
            self.network_address = new_address

        return address

    def home(self, *axes: int, if_needed: bool = True, skip: bool = False, timeout: int = 240, double_home: bool=False):
        """
        Homes the robot or axes connected to the C9 controller. If no axes are given, the main axes / robot will be homed.
        :param axes: axes to home, will home all main axes / robot if none given
        :param if_needed: only home if the connected C9 hasn't homed since power on
        :param skip: skip actual homing (WARNING: never use this)
        :param timeout: home timeout
        """
        response = self.request_command('HOME', axes or [None], flags={'C': if_needed, 'K': skip}, timeout=timeout)
        # This is a temporary hack to perform a double-home which avoids inaccurate homing when hall sensors aren't connected
        # only do a second home if we are homing all main axes and the joint positions after the first home are all 0, which
        # should only happen if the first home was actually needed
        if axes == () and response == '0 0 0 0' and not skip and double_home:
            response = self.request_command('HOME', axes or [None], flags={'C': False, 'K': False}, timeout=timeout)
        self.dispatch_axes_events('home', [0, 1, 2, 3])
        self.dispatch_position_events([0, 1, 2, 3], response.strip().split(' '))

    def halt(self, *axes: int):
        """
        Halts the given axes which immediately turns off the axis motors
        :param axes: axes to halt, at least one axis required
        """
        if len(axes) == 0:
            raise C9ControllerError('At least one axis required for halt')

        self.request_command('HALT', axes)

    def elbow_bias(self, bias: Optional[int]=None) -> int:
        """
        Change the elbow bias of the N9

        :param bias: bias to use, one of: C9Controller.BIAS_MIN_SHOULDER, C9Controller.BIAS_MAX_SHOULDER, C9Controller.BIAS_CLOSEST
        :return: current elbow bias
        """
        args = [bias] if bias is not None else []
        return int(self.request_command('BIAS', args).strip())

    def swap_elbow(self):
        """
        Move the N9 to same effector position but with a different elbow position, changing elbow bias if needed
        """
        self.request_command('SWEL')
        self.wait_for_axes([1, 2])

    def axis_positions(self, *axes: int, units: bool=False, motor: bool=False) -> List[float]:
        """
        Return a list of current positions for the given axes

        :param axes: axes to find positions for
        :param units: use units instead of counts for positions if True
        :param motor: find actual position from motor controller instead of internal C9 value
        :return: list of axis positions
        """
        scale = 1000 if units else 1
        return [float(p)/scale for p in self.request_command('POS', list(axes), {'U': units, 'M': motor}).split(' ')]

    def axis_position(self, axis: int, units: bool=False, motor: bool=False) -> float:
        """
        Return the position of the given axis

        :param axis: axis number
        :param units: use units instead of counts for positions if True
        :param motor: find actual position from motor controller instead of internal C9 value
        :return: axis position
        """
        scale = 1000 if units else 1
        return float(self.request_command('POS', [axis], {'U': units, 'M': motor})) / scale

    def axis_velocity(self, axis: int) -> float:
        """
        Return the actual (not the target) velocity of the given axis

        :param axis: axis number
        :return: axis velocity in counts / s
        """
        return float(self.request_command('VEL', [axis]))

    def axis_current(self, axis: int, max_current: Optional[int]=None, max: bool=False) -> int:
        """
        Return the actual or max current for the given axis, setting the max current if given

        :param axis: axis number
        :param max_current: optional new max current value
        :param max: return max current instead of actual if True
        :return: actual or max current
        """
        if max_current is not None:
            max = True
        return int(self.request_command('CURR', [axis, max_current], flags={'M': max}))

    def cartesian_position(self, retries: Optional[int] = None) -> List[float]:
        """
        Return the x, y, z position of the N9

        :return: list containing x, y and z positions in mm
        """
        if retries == 0:
            raise C9ResponseError(f'Invalid response for cartesian_position()')
        elif retries is None:
            retries = self.retries

        position = [float(p)/1000 for p in self.request_command('POS', flags={'C': True}).split(' ')]

        if len(position) != 3:
            time.sleep(0.01)
            return self.cartesian_position(retries=retries-1)

        return position

    def axes_moving(self, axes: List[int]) -> List[bool]:
        """
        Returns a list of moving statuses for the given axes (True if moving)

        :param axes: list of axis numbers
        :return: list of axis moving states
        """
        return [a == '1' for a in self.request_command('MVNG', axes).split(' ')]

    def axis_moving(self, axis: int) -> bool:
        """
        Returns given axis moving state

        :param axis: axis number
        :return: axis moving state (True if moving)
        """
        return self.request_command('MVNG', [axis]) == '1'

    def wait_for_axes(self, axes, poll_interval=0.01, verbose: bool=False):
        """
        Pauses until the given axes have stopped moving

        :param axes: list of axes numbers to wait for
        :param poll_interval: axis moving polling interval (defaults to 0.01 sec)
        :param verbose: controller verbosity while polling axes (defaults to False)
        """
        old_verbose = self.verbose
        if not verbose:
            self.verbose = False
        while True in self.axes_moving(axes):
            time.sleep(poll_interval)
        if not verbose:
            self.verbose = old_verbose

    def wait_for_axis(self, axis, poll_interval=0.01, verbose: bool=False):
        """
        Pause until the given axis has stopped moving

        :param axis: axis number
        :param poll_interval: axis moving polling interval (defaults to 0.01 sec)
        :param verbose: controller verbosity while polling axes (defaults to False)
        """
        self.wait_for_axes([axis], poll_interval, verbose)

    def wait_for_main_axes(self):
        """
        Pause until main axes / robot has stopped moving
        """
        self.wait_for_axes([0, 1, 2, 3])

    def output(self, output: int, state: Optional[bool]=None) -> bool:
        """
        Get or set the state of given output

        :param output: output number
        :param state: optional output state (True is on)
        :return: output state
        """

        if state is None:
            return self.request_command('OUTP', [output]) == '1'

        value = 1 if state else 0
        self.request_command('OUTP', [output, value])
        self.dispatch_output_event('state', output, state)
        return state

    def output_toggle(self, output: int) -> bool:
        """
        Toggle the state of the given output

        :param output: output number
        :return: output state
        """
        state = self.output(output)
        return self.output(output, not state)

    def outputs(self, pins: List[int]=[], all: bool=False) -> List[bool]:
        """
        Get the state for the given output pins

        :param pins: output pin numbers
        :param all: get state of all outputs
        :return: bool list of output states
        """
        outputs = self.request_command('OUTP', pins, {'A': all}).split(' ')
        return [bool(int(value)) for value in outputs]

    def analog(self, pin: int) -> float:
        """
        Get the voltage on an analog input pin

        :param pin: analog pin number
        :return: voltage
        """
        return float(self.request_command('ADC', [pin])) / 1000

    def analog_inputs(self, pins: List[int]=[], all: bool=False) -> List[float]:
        """
        Get the value of the given analog inputs

        :param pins: analog input pins
        :param all: get value of all analog inputs
        :return: list of analog input values
        """
        inputs = self.request_command('ADC', pins, {'A': all}).split(' ')
        return [float(value) / 1000 for value in inputs]

    def digital(self, pin: int) -> bool:
        """
        Get the state of a digital input

        :param pin: digital input pin
        :return: digital input state
        """
        return bool(int(self.request_command('INP', [pin])))

    def digital_inputs(self, pins: List[int]=[], all: bool=False) -> List[bool]:
        """
        Get the state of the given digital inputs

        :param pins: digital input pins
        :param all: get state of all digital inputs
        :return: list of digital input states
        """
        inputs = self.request_command('INP', pins, {'A': all}).split(' ')
        return [bool(int(value)) for value in inputs]

    def carousel(self, index: int, wait: bool=True, carousel: int=0):
        """
        Move attached carousels to the given index position (0 is the "home" position)

        :param index: carousel index
        :param wait: wait for carousel to stop (defaults to True)
        :param carousel: carousel index (defaults to 0)
        """
        self.request_command('CRSL', [carousel, index])

        if wait:
            self.wait_for_axis(self.AXIS_CAROUSEL)

    def weigh_scale(self, tare: bool=False) -> float:
        """
        Returns a measurement (in mg) from the attached weigh scale

        :param tare: tare the scale before measuring if True (default is False)
        :return: weight in mg
        """
        return float(self.request_command('WEIG', [], {'T': tare}))

    def elbow_length(self, length: Optional[float]=None) -> float:
        """
        Change the length of the last robot link, used for moving the robot probe

        :param length: length offset
        :return: current length offset
        """
        if length is None:
            return float(self.request_command('JLEN', []))
        else:
            return float(self.request_command('JLEN', [round(length * 1000)]))

    def use_probe(self, probe: bool=True, probe_offset: float=41.5):
        """
        Use the robot probe when moving

        :param probe: use probe if True (defaults to True)
        :param probe_offset: elbow length offset for probe (defaults to 41.5)
        """
        self.elbow_length(probe_offset if probe else 0)

    def speed(self, velocity: Optional[int]=None, acceleration: Optional[int]=None) -> Tuple[int, int]:
        """
        Get or sets the default velocity and acceleration for movements

        :param velocity: optional velocity in counts / s
        :param acceleration: optional acceleration in counts / s^2
        """
        velocity, acceleration = self.request_command('SPED', [velocity, acceleration]).split(' ')
        return int(velocity), int(acceleration)

    def move(self, axis_positions: Dict[int, float], velocity: Optional[int]=None, acceleration: Optional[int]=None,
             relative: bool=False, units: bool=False, wait: bool=True) -> List[float]:
        """
        Move axes to a relative or absolute position

        :param axis_positions: dictionary mapping axis numbers to target positions
        :param velocity: optional velocity during movement in counts / s
        :param acceleration: optional acceleration during movement in counts / s^2
        :param relative: use relative movements if True (defaults to False or absolute movements)
        :param units: positions are in units instead of counts (defaults to False)
        :param wait: wait for axes to stop moving (defaults to True)
        :return: list of final axis positions after move
        """
        if (velocity is None or acceleration is None) and velocity != acceleration:
            raise C9Error('Both acceleration and velocity need to be set or None')

        args = []

        for axis, position in axis_positions.items():
            args += [axis, position * 1000 if units else position]

        flags = {'V': velocity, 'A': acceleration, 'R': relative, 'U': units}
        response = self.request_command('MOVE', args, flags)
        start_time = time.time()
        duration, *positions = response.strip().split(' ')
        self.dispatch_position_events(axis_positions.keys(), positions)
        if wait:
            if self.move_prediction:
                duration = float(duration) * self.move_wait_scale / 1000 - (time.time() - start_time) - self.move_wait_delay
                time.sleep(max(duration, 0))
            self.wait_for_axes(axis_positions.keys())

        return positions

    def move_axis(self, axis: int, position: float, velocity: Optional[int]=None, acceleration: Optional[int]=None,
                  relative: bool=False, units: bool=False, wait: bool=True) -> float:
        """
        Moves an axis to an absolute or relative position

        :param axis: axis number
        :param position: target position
        :param velocity: optional velocity to use during move
        :param acceleration: optional acceleration to use during move
        :param relative: use relative movement if True (defaults to False)
        :param units: position is in units instead of counts if True (defaults to False)
        :param wait: wait for axis to stop moving if True (defaults to True)
        :return: final position after move
        """
        return self.move({axis: position}, velocity, acceleration, relative, units, wait)[0]

    def spin_axis(self, *axes: int, velocity: Optional[int]=None, acceleration: Optional[int]=None, stop: bool=False):
        """
        Start (or stop) spinning axes

        :param axes: axis numbers to spin
        :param velocity: velocity of spin
        :param acceleration: acceleration during spin
        :param stop: stops spin instead of starting if True (defaults to False)
        """
        self.request_command('SPIN', axes, {'V': velocity, 'A': acceleration, 'H': stop})

    def spin_axis_stop(self, *axes: int):
        """
        Stop spinning axes

        :param axes: axis numbers to stop
        """
        self.spin_axis(*axes, stop=True)

    def move_arm(self, x: Optional[float]=None, y: Optional[float]=None, z: Optional[float]=None,
                 gripper: Optional[float]=None, velocity: Optional[float]=None, acceleration: Optional[float]=None,
                 elbow_bias: Optional[int]=None, relative: bool=False, wait: bool=True) -> List[int]:
        """
        Move robot arm to a cartesian position, most positions are optional and the minimum number of axes will be moved

        :param x: optional x position in mm (x and y must be set as a pair)
        :param y: optional y position in mm (x and y must be set as a pair)
        :param z: optional z position in mm
        :param gripper: optional gripper position in degrees
        :param velocity: optional velocity during move in counts / s
        :param acceleration: optional acceleration during move in counts / s^2
        :param relative: perform a relative movement if True (defaults to False)
        :param wait: wait for movement to complete if True (defaults to False)
        :return: final positions of main axes after move
        """
        if (velocity is None or acceleration is None) and velocity != acceleration:
            raise C9Error('Both acceleration and velocity need to be set or None')

        axes = []
        flags = {'V': velocity, 'A': acceleration, 'R': relative}

        if x is not None and x is not False:
            flags['X'] = x * 1000
            axes += [1, 2]

        if y is not None and y is not False:
            flags['Y'] = y * 1000
            if 1 not in axes:
                axes += [1, 2]

        if z is not None and z is not False:
            flags['Z'] = z * 1000
            axes.append(3)

        if gripper is not None and gripper is not False:
            flags['G'] = gripper * 1000
            axes.append(0)

        if elbow_bias is not None and elbow_bias is not False:
            flags['B'] = elbow_bias

        response = self.request_command('ARM', [], flags)
        start_time = time.time()
        duration, *positions = response.strip().split(' ')
        self.dispatch_position_events([0, 1, 2, 3], positions)
        if wait:
            if self.move_prediction:
                duration = float(duration) * self.move_wait_scale
                time.sleep(max(float(duration) / 1000 - (time.time() - start_time) - self.move_wait_delay, 0))
            self.wait_for_axes(axes)

        return positions

    def com_init(self, port: int, baudrate: int):
        """
        Initialize an aux COM port on the C9 with the given baudrate

        :param port: COM port to initialize (matches COM number labelled on C9)
        :param baudrate: baudrate to to use (eg. 9600)
        """
        self.request_command('COM', [port, baudrate], {'I': True})

    def com_flush(self, port: int):
        """
        Flush the input buffer for the given aux COM port

        :param port: COM port to flush
        """
        self.request_command('COM', [port], {'F': True})

    def com_rx_size(self, port: int, retries: int=5) -> int:
        """
        Return the number of characters in the given aux COM port input buffer

        :param port: COM port to check
        :return: number of characters in input buffer
        """
        response = self.request_command('COM', [port], {'S': True})

        if not response:
            if retries <= 0:
                raise C9ResponseError(f'Invalid com_rx_size response: {response}')

            self.logger.warning(f'Invalid com_rx_size response: {response}')
            return self.com_rx_size(port, retries - 1)

        return int(response)

    def com_read(self, port: int, num_bytes: int=-1, timeout=1000) -> bytes:
        """
        Read bytes from the given aux COM port

        :param port: COM port to read from
        :param num_bytes: optional number of bytes to read (defaults to -1, which reads all bytes in input buffer)
        :return: bytes of data read from COM port
        """
        try:
            self.request_command('COM', [port, timeout, num_bytes], {'R': True})
        except C9Error as err:
            # simulate a SerialReadTimeoutException if we get a CRC error when trying to read serial data
            if err.error_number == C9Error.INVALID_CRC:
                raise SerialReadTimeoutException('Read timeout')
            else:
                raise err

        try:
            data = self.connection.read(num_bytes)
        except SerialReadTimeoutException:
            data = b''

        self.logger.debug(f'Received COM data: {data}')
        return data

    def com_write(self, port: int, data: bytes):
        """
        Write data to the given aux COM port

        :param port: COM port to write to
        :param data: data to write
        """

        self.request_command('COM', [port, len(data)], {'W': True})
        time.sleep(0.01)
        self.connection.write(data)
        self.logger.debug(f'Sent COM data: {data}')
        time.sleep(0.1)

    def com(self, port: int, baudrate: int=9600) -> Serial:
        """
        Create a new Serial class instance for the given aux COM port

        :param port: COM port to proxy serial data to
        :param baudrate: baudrate to use for COM port proxy
        :return: Serial instance
        """
        from north_c9.serial import C9SerialDevice
        return Serial(C9SerialDevice(self, port), baudrate=baudrate)

    def axis_state(self, axis: int) -> int:
        """
        Return the state of the given axis

        :param axis: axis to check
        :return: state of axis (-1 if in fault state)
        """
        return int(self.request_command('STAT', [axis]))

    def axis_error(self, axis: int) -> str:
        """
        Return the fault error code for the given axis

        :param axis: axis to check for errors
        :return: axis error code (0000 if no error)
        """
        return self.request_command('STAT', [axis], {'E': True})

    def axis_errors(self) -> Dict[int, int]:
        """
        Return a list of axis fault errors

        :return: list of (<axis number>, <fault code>) tuples, empty if no faults
        """
        raw_errors = self.request_command('STAT', [], {'F': True})
        axis_errors = raw_errors.split('\n')
        errors = {}

        for axis_error in axis_errors:
            axis, error = axis_error.split(' ')
            errors[int(axis)] = error.strip()

        return errors

    def uncap(self, pitch_mm: float, rotations: float=1.5) -> List[float]:
        """
        Perform an uncap movement. This will spin the gripper counter-clockwise for the given number of rotations while
        moving the z axis upwards at a rate matching the thread pitch (the cap displacement after one rotation).

        The arm should be in a position with the gripper closed on the cap before `uncap` is called.

        The position returned should be saved for recapping.

        :param pitch_mm: thread pitch in mm of the cap (this is the displacement after one rotation)
        :param rotations: the number of rotations needed to uncap, defaults to 1.5
        :return: position of the arm after uncapping, this is the position needed for recapping
        """
        self.move({0: -rotations * 360, 3: pitch_mm * rotations}, relative=True, units=True)
        return self.cartesian_position()

    def recap(self, pitch_mm: float, rotations: float=1.5) -> List[float]:
        """
        Perform a recap movement. This will spin the gripper clockwise for the given number of rotations while moving
        the z axis downwards at a rate matching the thread pitch (the cap displacement after one rotation).

        The robot arm should be moved to the position returned from `uncap` before recapping, with the gripper still
        gripping the cap.

        :param pitch_mm: thread pitch in mm of the cap (this is the displacement after one rotation)
        :param rotations: the number of rotations needed to uncap, defaults to 1.5
        :return: position of the arm after recapping
        """
        self.move({0: rotations * 360, 3: -pitch_mm * rotations}, relative=True, units=True)
        return self.cartesian_position()
