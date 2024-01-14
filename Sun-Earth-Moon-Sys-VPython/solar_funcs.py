
'''
3D simulation of Sun-Earth-Moon motion
'''
from solor_consts import THETA0, MoonRadius, EarthRadius
from vpython import (
        color, canvas, graph, gdots,
        sphere, simple_sphere,
        vector, label)


def setup_scene():
    scene = canvas(
                width=1000, height=600, title='<h1><center><b>\
                3D Multi-Body System</b></center></h1>'
            )

    scene.append_to_caption("""
        <style>
            body {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 10;
            }
        </style>
    """)
    scene.lights[1].color = color.red
    scene.background = color.black


def setup_graph():
    # display the gragh of movement
    gd = graph(
                width=1000,
                height=200,
                title='<b>Position Vs Time</b>',
                xtitle='<i>Time [s]</i>',
                ytitle='<i>position [Moon]</i>',
                foreground=color.black,
                background=color.black
                )
    return gdots(graph=gd, color=color.green)


def create_astro_obj(init_moon_dis):
    """_
    Creates astronamical objects such as Sun, Earth & etc.
    """
    sun = sphere(
                pos=vector(0, 0, 0), texture='sun.png',
                pickable=True, radius=3)
    earth = sphere(
                pos=vector(10, 0, 0), radius=1,
                make_trail=True, trail_color=color.red,
                texture='earth.png')
    moon = simple_sphere(
                pos=earth.pos+init_moon_dis, radius=round(
                    MoonRadius/EarthRadius, 3),
                make_trail=True, trail_color=color.yellow,
                trail_radius=0.05, texture='moon.png')
    # Earth's start point label
    _ = label(pos=earth.pos, text='Start', xoffset=20,
              yoffset=12, space=earth.radius, height=10,
              border=6, font='sans')
    return earth, moon, sun


def positionMoon(t, moon_angl_v):
    theta = THETA0 + moon_angl_v * t
    return theta


def positionEarth(t, earth_angle_v):
    theta = THETA0 + earth_angle_v * t
    return theta


def from_days_to_seconds(d):
    return d*24*60*60


def from_hours_to_seconds(h):
    return h*60*60
