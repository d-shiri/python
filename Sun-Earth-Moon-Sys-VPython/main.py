'''
3D simulation of Sun-Earth-Moon motion
'''

import math
from vpython import (
    rate,
    rotate, mag, vector
)
from solar_funcs import (
    setup_scene,
    setup_graph,
    positionMoon,
    positionEarth,
    from_days_to_seconds,
    from_hours_to_seconds,
    create_astro_obj,
)
from solor_consts import (
    SED, SEGF, ME, DAYS, SIDE_MONTH
)


INIT_MOON_DIST = vector(2, 0, 0)
# Angular velocity of the moon in its orbit (rad/s)
MOON_ANGLE_VELO = 2*math.pi/from_days_to_seconds(SIDE_MONTH)
# Angular velocity of the Earth with respect to the Sun(rad/s)
EARTH_ANGLE_VELO = math.sqrt(SEGF/(ME * SED))


setup_scene()
Earth, Moon, Sun = create_astro_obj(INIT_MOON_DIST)
plot = setup_graph()
seconds = from_days_to_seconds(DAYS)
t = 0
dt = from_hours_to_seconds(2)
while t < seconds:
    rate(100)
    theta_earth = positionEarth(t+dt, EARTH_ANGLE_VELO) - positionEarth(
                t, EARTH_ANGLE_VELO)
    theta_moon = positionMoon(t+dt, MOON_ANGLE_VELO) - positionMoon(
                t, MOON_ANGLE_VELO)
    # Rotation only around z axis (0,0,1)
    Earth.pos = rotate(Earth.pos, angle=theta_earth, axis=vector(0, 0, 1))
    INIT_MOON_DIST = rotate(
                INIT_MOON_DIST, angle=theta_moon,
                axis=vector(0, 0, 1))
    Earth.rotate(angle=6.26, axis=vector(0, 1, 0))
    Sun.rotate(angle=157.07, axis=vector(0, 1, 0))
    Moon.pos = Earth.pos + INIT_MOON_DIST
    # ploting
    plot.plot(pos=(t, mag(Moon.pos)))
    t += dt
