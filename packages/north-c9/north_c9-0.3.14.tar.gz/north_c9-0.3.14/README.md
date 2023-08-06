# North C9

The North C9 library is a low level library wrapping the North C9 Controller protocol.


## Installation

Install the `north_c9` library
```bash
pip install git+https://gitlab.com/north-robotics/north_c9
```

Import the `C9Controller` class at the top of a Python file, or inside a Python console
```python
from north_c9.controller import C9Controller
```
   
Create a new `C9Controller` instance to connect to the C9 controller
```python     
controller = C9Controller()
```

Now you can move axes, toggle outputs and move the N9 (if available)
```python
# move axis 5 to 0 counts
controller.move_axis(5, 0, velocity=1000, acceleration=5000)
# rotate axis 5 once (motors have 1000 counts / revolution)
controller.move_axis(5, 1000, velocity=1000, acceleration=5000, relative=True)
# start spin axis 5
controller.spin_axis(5, velocity=1000, acceleration=5000)
# stop spinning axis 5
controller.spin_axis_stop(5)

# turn output 0 on and off
controller.output(0, True)
controller.output(0, False)
controller.output_toggle(0)

# home the N9
controller.home()
# move the N9 to x=0 mm, y=150 mm, z=150 mm and gripper=90 deg
controller.move_arm(0, 150, 150, gripper=90)
```