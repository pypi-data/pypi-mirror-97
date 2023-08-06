import logging
from north_c9.controller import C9Controller

logging.basicConfig(level=logging.WARNING)

c9 = C9Controller(device_serial='FT3FM1O1')
c9.home()

c9.speed(45000, 90000)

while True:
    c9.move_arm(150, 200, 200)
    c9.move_arm(-150, 150, 250)
