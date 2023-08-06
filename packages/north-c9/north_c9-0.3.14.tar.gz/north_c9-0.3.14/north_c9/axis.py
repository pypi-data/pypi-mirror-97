from typing import Optional
import time
from north_utils.motion import degrees_to_counts, counts_to_degrees, mm_to_counts, counts_to_mm, cps_to_rpm, rpm_to_cps
from north_c9.controller import C9Controller


class Output:
    """
    The Output class is used to control outputs on the North C9 with an easy-to-use interface. It provides a low-level
    :func:`~north_c9.Output.set_state` method, along with higher-level :func:`~north_c9.Output.on`,
    :func:`~north_c9.Output.off` and :func:`~north_c9.Output.toggle` methods.

    >>> from north_c9.controller import C9Controller
    >>> from north_c9.axis import Output
    >>> c9 = C9Controller()
    >>> output = Output(c9, 0)  # output number 0
    >>> output.on()
    >>> output.toggle()
    >>> output.state
    False
    """
    def __init__(self, controller: C9Controller, output_number: int):
        """
        Create an instance of the Output class

        :param controller: connection to the C9Controller
        :param output_number: the output that you would like to control (the first output is number ``0``)
        """
        self.controller = controller
        self.output_number = output_number

    @property
    def state(self) -> bool:
        """
        Get the current state of the Output

        :return: ``True`` if the output is on, ``False`` if it is off
        """
        return self.controller.output(self.output_number)

    def set_state(self, state: bool):
        """
        Set the output state

        :param state: New output state, ``True`` is on, ``False`` is off
        """
        self.controller.output(self.output_number, state)

    def on(self):
        """
        Turn on the output
        """
        self.set_state(True)

    def off(self):
        """
        Turn off the output
        """
        self.set_state(False)

    def toggle(self):
        """
        Toggle the output, turning it on if it is off, and off if it is on
        """
        self.set_state(not self.state)


class OpenOutput(Output):
    """
    The OpenOutput class is a simple wrapper around the normal Output class that provides extra open and close methods
    that may be more intuitive in certain situations. The output state used when the output is "open" is configurable,
    defaulting to ``on`` / ``True``.
    """
    def __init__(self, controller: C9Controller, output_number: int, open_state: bool=True):
        """
        Create an OpenOutput instance

        :param controller: connection to the C9Controller
        :param output_number: the output that you would like to control (the first output is number ``0``)
        :param open_state: the state to use when open is called (defaults to ``on`` / ``True``)
        """
        Output.__init__(self, controller, output_number)
        self.open_state = open_state

    def open(self):
        """
        Open the output (sets the Output state to the ``open_state``, defaults to ``True``)
        """
        self.set_state(self.open_state)

    def close(self):
        """
        Close the output (sets the Output state to the opposite of ``open_state``, defaults to ``False``)
        """
        self.set_state(not self.open_state)


class Axis:
    """
    The Axis class is a low-level class for controlling axes on the North Robotics C9. Higher-level RevoluteAxis and
    PrismaticAxis classes are also available.

    Axis positions use *counts* as a (somwhat arbitrary) unit, and there are 1000 counts per revolution of the axis.
    """
    def __init__(self,
                 controller: C9Controller,
                 axis_number: int,
                 velocity_counts: Optional[int]=None,
                 acceleration_counts: Optional[int]=None,
                 max_position: Optional[int]=None,
                 max_current: Optional[int]=None,
                 home_velocity_counts: Optional[int]=None,
                 home_acceleration_counts: Optional[int]=None,
                 home_max_current: Optional[int]=None,
                 home_to_block: bool=True,
                 main: bool=False,
                 reversed: bool=False,
                 **kwargs) -> None:
        """
        :param controller: connection to the C9Controller
        :param axis_number: the axis you would like to control
        :param velocity_counts: the movement velocity in *counts/s*
        :param acceleration_counts: the movement acceleration in *counts/s^2*
        :param max_position: the maximum position of this axis, used when homing to a block
        :param max_current: the max current to use when driving the motor for this axis in *mA*
        :param home_velocity_counts: the velocity to use while homing in *counts/s*
        :param home_acceleration_counts: the acceleration to use while homing in *counts/s^2*
        :param home_max_current: the max current to use while homing in *mA*
        :param home_to_block: if True, homing will move axis in reverse for ``max_position`` counts
        :param main: if True, this will be considered a *main* axis that cannot be homed separate from the robot
        :param reversed: if True, the position and movement of the axis will be reversed
        """
        self.controller = controller
        self.axis_number = axis_number
        self.velocity = velocity_counts
        self.acceleration = acceleration_counts
        self.max_current = max_current
        self.max_position = max_position
        self.reversed = reversed
        self.sign = -1 if reversed else 1
        self.main = main
        self.home_velocity = home_velocity_counts if home_velocity_counts is not None else velocity_counts or 0 / 2
        self.home_acceleration = home_acceleration_counts if home_acceleration_counts is not None else velocity_counts or 0 / 2
        self.home_max_current = home_max_current
        self.home_to_block = home_to_block and self.max_position is not None

        self.write_axis_settings()

    @property
    def position(self) -> float:
        """
        Get the current position of the axis in *counts*
        """
        return self.controller.axis_position(self.axis_number)

    @property
    def current_velocity(self) -> float:
        """
        Get the current velocity of the axis in *counts/s*
        """
        return self.controller.axis_velocity(self.axis_number)

    def write_axis_settings(self):
        """
        Write axis settings to the C9
        """
        if self.max_current is not None:
            self.set_max_current(self.max_current)

    def set_max_current(self, current, update: bool=True):
        """
        Set the max current and write it to the C9

        :param update: don't update self.max_current if False
        """
        self.controller.axis_current(self.axis_number, current, max=True)
        if update:
            self.max_current = current

    def home(self):
        """
        Performs a homing procedure for the axis. If ``home_to_block`` is ``True``, the axis will be moved in reverse
        for ``max_position`` counts.
        """
        if self.main:
            raise AxisError('Only aux axis can be homed manually')

        if self.home_max_current is not None:
            self.set_max_current(self.home_max_current)

        if self.home_to_block:
            self.move(-self.max_position * self.sign, velocity=self.home_velocity, acceleration=self.home_acceleration, relative=True, wait=True)

        self.controller.home(self.axis_number)

        if self.home_max_current is not None:
            self.set_max_current(self.max_current)

    def moving(self) -> bool:
        """
        Get the moving status of this axis

        :return: True if the axis is moving, False otherwise
        """
        return self.controller.axis_moving(self.axis_number)

    def wait(self):
        """
        Wait for the axis to stop moving
        """
        self.controller.wait_for_axis(self.axis_number)

    def move(self, counts: int, velocity: Optional[int]=None, acceleration: Optional[int]=None, relative: bool=False,
             wait: bool=True):
        """
        Start moving the axis. *Absolute* moves (the default) will move the axis until it reaches the given ``counts``
        position, while *relative* moves will move the axis to the current position plus the given number of ``counts``.
        For relative moves, a positive ``counts`` value will move the axis "forward" and a negative ``counts`` value will
        move it backwards.

        :param counts: the number of counts to move
        :param velocity: optional velocity during the movement in *counts/s*
        :param acceleration: optional acceleration during the movement in *counts/s^s*
        :param relative: performs a relative move if True, an absolute move if False (defaults to False)
        :param wait: wait for the movement to complete (defaults to True)
        """
        if velocity is None:
            velocity = self.velocity

        if acceleration is None:
            acceleration = self.acceleration

        if velocity is None and acceleration is None:
            raise AxisMoveError('Error moving joint, no velocity or acceleration given (and no defaults set for joint)')

        self.controller.move_axis(self.axis_number, counts, velocity, acceleration, wait=wait, units=self.main, relative=relative)


class RevoluteAxis(Axis):
    """
    The RevoluteAxis class is a higher-level class for controlling revolute axes, which are axes that can spin continuously.
    It inherits from the Axis class, so it can take the same parameters and provides the same methods. Additionally, the
    RevoluteAxis class provides additional methods to work with movements in degrees and RPM.
    """
    def __init__(self,
                 controller: C9Controller,
                 axis: int,
                 counts_per_revolution: float=1000.0,
                 zero_position_degrees: float=0.0,
                 position_degrees: float=0,
                 velocity_degrees: float=None,
                 acceleration_degrees: float=None,
                 inverted: bool=False,
                 **kwargs) -> None:
        kwargs['position'] = kwargs.get('position', degrees_to_counts(position_degrees, counts_per_revolution))
        kwargs['velocity'] = kwargs.get('velocity', degrees_to_counts(velocity_degrees, counts_per_revolution))
        kwargs['acceleration'] = kwargs.get('acceleration', degrees_to_counts(acceleration_degrees, counts_per_revolution))
        Axis.__init__(self, controller, axis, inverted=inverted, **kwargs)

        self.zero_position_degrees = zero_position_degrees
        self.counts_per_revolution = counts_per_revolution
        self.angle_sign = -1 if inverted else 1

    @property
    def position_degrees(self) -> float:
        """
        Get or set the current position of the axis in *degrees*
        """
        return counts_to_degrees(self.position, self.counts_per_revolution, sign=self.angle_sign) - self.zero_position_degrees

    @property
    def velocity_degrees(self) -> float:
        """
        Get or set the velocity of the axis in *degrees/s*
        """
        return counts_to_degrees(self.velocity, self.counts_per_revolution) or 0

    @property
    def current_velocity_degrees(self) -> float:
        """
        Get or set the current velocity of the axis in *degrees/s*
        """
        return counts_to_degrees(self.current_velocity, self.counts_per_revolution) or 0

    @property
    def current_velocity_rpm(self) -> float:
        """
        Get or set the current velocity of the axis in *RPM*
        """
        return cps_to_rpm(self.current_velocity, self.counts_per_revolution) or 0

    @velocity_degrees.setter
    def velocity_degrees(self, velocity: float):
        self.velocity = degrees_to_counts(velocity, self.counts_per_revolution) or 0

    @property
    def acceleration_degrees(self) -> float:
        return counts_to_degrees(self.acceleration, self.counts_per_revolution) or 0

    @acceleration_degrees.setter
    def acceleration_degrees(self, acceleration: float):
        self.acceleration = degrees_to_counts(acceleration, self.counts_per_revolution)

    def move_degrees(self, degrees: float, velocity_degrees: Optional[float]=None,
                     acceleration_degrees: Optional[float]=None, relative: bool=False, wait: bool=True):
        """
        Start moving the axis using *degrees* as the unit. *Absolute* moves (the default) will move the axis until it
        reaches the given ``degrees`` position, while *relative* moves will move the axis to the current position plus
        the given number of ``degrees``. For relative moves, a positive ``degrees`` value will move the axis clockwise
        and a negative ``degrees`` value will move it counter-clockwise.

        :param degrees: the number of degrees to move
        :param velocity_degrees: optional velocity during the movement in *degrees/s*
        :param acceleration_degrees: optional acceleration during the movement in *degrees/s^s*
        :param relative: performs a relative move if True, an absolute move if False (defaults to False)
        :param wait: wait for the movement to complete (defaults to True)
        """

        if not relative:
            degrees += self.zero_position_degrees

        counts = degrees_to_counts(degrees * self.angle_sign, self.counts_per_revolution) or 0
        velocity = degrees_to_counts(velocity_degrees, self.counts_per_revolution)
        acceleration = degrees_to_counts(acceleration_degrees, self.counts_per_revolution)

        self.move(counts, velocity, acceleration, relative=relative, wait=wait)

    def spin(self, velocity_rpm: float, acceleration_rpm: float, duration: Optional[float]=None):
        """
        Start spinning the axis

        :param velocity_rpm: velocity to spin at in *RPM*
        :param acceleration_rpm: acceleration to use for spinning in *RPM*
        :param duration: optional duration to spin the axis for, defaults to spinning indefinitely
        """

        velocity_counts = rpm_to_cps(velocity_rpm, self.counts_per_revolution)
        acceleration_counts = rpm_to_cps(acceleration_rpm, self.counts_per_revolution)

        self.controller.spin_axis(self.axis_number, velocity=velocity_counts, acceleration=acceleration_counts)

        if duration is not None:
            time.sleep(duration)
            self.spin_stop()

    def spin_stop(self, wait: bool=False):
        """
        Stop spinning the axis

        :param wait: wait for the axis to stop spinning (defaults to False)
        """
        self.controller.spin_axis(self.axis_number, stop=True)

        if wait:
            self.controller.wait_for_axis(self.axis_number)


class PrismaticAxis(Axis):
    """
    The PrismaticAxis class is a higher-level class for controlling prismatic axes, which are axes that move linearly.
    It inherits from the Axis class, so it can take the same parameters and provides the same methods. Additionally, the
    PrismaticAxis class provides additional methods to work with movements in *mm*.
    """
    def __init__(self,
                 controller: C9Controller,
                 axis: int,
                 counts_per_mm: float=1.0,
                 position_mm: float=0.0,
                 zero_position_mm: float=0.0,
                 velocity_mm: Optional[float]=None,
                 acceleration_mm: Optional[float]=None,
                 inverted: bool=False,
                 **kwargs) -> None:
        kwargs['position'] = kwargs.get('position', mm_to_counts(position_mm, counts_per_mm))
        kwargs['velocity'] = kwargs.get('velocity', mm_to_counts(velocity_mm, counts_per_mm))
        kwargs['acceleration'] = kwargs.get('acceleration', mm_to_counts(acceleration_mm, counts_per_mm))
        Axis.__init__(self, controller, axis, **kwargs)

        self.counts_per_mm = counts_per_mm
        self.zero_position_mm = zero_position_mm
        self.sign = -1 if inverted else 1

    @property
    def position_mm(self) -> float:
        """
        Get the current position in mm
        """
        return counts_to_mm(self.position, self.counts_per_mm) * self.sign + self.zero_position_mm

    @property
    def velocity_mm(self) -> float:
        """
        Get or set the velocity in mm
        """
        return counts_to_mm(self.velocity, self.counts_per_mm) or 0

    @velocity_mm.setter
    def velocity_mm(self, velocity: float):
        self.velocity = mm_to_counts(velocity, self.counts_per_mm) or 0

    @property
    def acceleration_mm(self) -> float:
        """
        Get or set the acceleration in mm
        """
        return counts_to_mm(self.acceleration, self.counts_per_mm) or 0

    @acceleration_mm.setter
    def acceleration_mm(self, acceleration: float):
        self.acceleration = mm_to_counts(acceleration, self.counts_per_mm) or 0

    def move_mm(self, mm: float, velocity_mm: Optional[float]=None, acceleration_mm: Optional[float]=None,
                relative: bool=False, wait: bool=True):
        """
        Start moving the axis using *mm* as the unit. *Absolute* moves (the default) will move the axis until it
        reaches the given ``mm`` position, while *relative* moves will move the axis to the current position plus
        the given number of ``mm``. For relative moves, a positive ``mm`` value will move the axis forward
        and a negative ``mm`` value will move it backward.

        :param mm: the number of degrees to move
        :param velocity_mm: optional velocity during the movement in *mm/s*
        :param acceleration_mm: optional acceleration during the movement in *mm/s^s*
        :param relative: performs a relative move if True, an absolute move if False (defaults to False)
        :param wait: wait for the movement to complete (defaults to True)
        """
        if not relative:
            mm -= self.zero_position_mm

        counts = mm_to_counts(mm * self.sign, self.counts_per_mm) or 0
        velocity = mm_to_counts(velocity_mm, self.counts_per_mm)
        acceleration = mm_to_counts(acceleration_mm, self.counts_per_mm)

        self.move(counts, velocity, acceleration, relative=relative, wait=wait)


class AxisError(Exception):
    """ Base class for Axis exceptions """
    pass


class AxisMoveError(AxisError):
    """ Axis movement exception """
    pass
