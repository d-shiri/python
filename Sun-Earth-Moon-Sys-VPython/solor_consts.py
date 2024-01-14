'''
3D simulation of Sun-Earth-Moon motion
'''
import math

# Constants. Units are in SI.
G = 6.67384 * math.pow(10, -11)         # Gravitational constant
ME = 5.973 * math.pow(10, 24)           # Mass of the Earth (kg)
MM = 70.34767309 * math.pow(10, 22)     # Mass of the Moon (kg)
MS = 1.9891 * math.pow(10, 30)          # Mass of the Sun (kg)

EMD = 3.844 * math.pow(10, 8)           # Earth-Moon Distance (m)
SED = 149597870700                      # Sun-Earth Distance (m)
EMGF = G*(ME*MM)/math.pow(EMD, 2)       # Earth-Moon Gravitational Force (N)
SEGF = G*(MS*ME)/math.pow(SED, 2)       # Sun-Earth Gravitational Force (N)


THETA0 = 0                              # Initial angular position
DAYS = 365                              # An Earth Year
SIDE_MONTH = 27.3                       # Sidereal Month

# Sizes
EarthRadius = 6371                      # Earth Radius (km)
MoonRadius = 1737.4                     # Moon Radius (km)
