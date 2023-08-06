from north_c9.controller import C9Controller

c9 = C9Controller(debug_protocol=True)
c9.home(skip=True)

c9.joystick.start_moving()