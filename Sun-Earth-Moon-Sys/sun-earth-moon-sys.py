"""
Simulation of 3 body system with turtle lib
Author: D-Shiri
"""

import turtle
import math

class AstroEntity:
    """
    Represents a celestial body in a solar system.

    Args:
        name (str): The name of the celestial body.
        color (str): The color of the celestial body.
        radius (int): The radius of the celestial body.
        distance (int): The distance from the center of the system.
        speed (int): The rotational speed of the celestial body.
        texture (str, optional): The texture file for the body shape.
        shape (str, optional): The shape of the celestial body (default is "circle").
    """
    def __init__(self, name, color, radius, distance, speed, texture=None, shape="circle"):
        self.name = name
        self.body = turtle.Turtle()
        self.body.color(color)
        self.body.shape(shape)
        self.body.penup()
        self.body.shapesize(radius, radius)
        self.distance = distance
        self.speed = speed
        self.angle = 0
        self.x = 0
        self.y = 0
        if texture is not None:
            turtle.register_shape(texture)
            self.body.shape(texture)
            

    def update_position(self):
        """
        Update the position of the celestial body based on its current heading.
        """
        self.x = self.distance * math.cos(math.radians(self.body.heading()))
        self.y = self.distance * math.sin(math.radians(self.body.heading()))
        self.body.goto(self.x, self.y)
    
    def update_moon_position(self, planet):
        """
        Update the position of the moon relative to its parent planet.

        Args:
            planet (AstroEntity): The parent planet.
        """
        x = self.distance * math.cos(math.radians(self.body.heading())) + planet.x
        y = self.distance * math.sin(math.radians(self.body.heading())) + planet.y
        self.body.goto(x, y)

    def rotate(self):
        """
        Rotate the celestial body based on its rotational speed.
        """
        self.body.right(self.speed)


def create_astro_obj(name, color, radius, distance, speed, texture=None) -> AstroEntity:
    """
    Set up a celestial body with initial parameters and return it.

    Args:
        name (str): The name of the celestial body.
        color (str): The color of the celestial body.
        radius (int): The radius of the celestial body.
        distance (int): The distance from the center of the system.
        speed (int): The rotational speed of the celestial body.

    Returns:
        AstroEntity: The created celestial body.
    """
    body = AstroEntity(name, color, radius, distance, speed, texture)
    body.body.goto(distance, 0)
    return body

class SolarSystem:
    """
    Represents a solar system with multiple celestial bodies.

    Attributes:
        screen (turtle.Screen): The turtle screen object.
        sun (AstroEntity): The sun object in the solar system.
        earth (AstroEntity): The earth object in the solar system.
        moon (AstroEntity): The moon object in the solar system.
    """
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.title("Sun-Earth-Moon System")

        self.sun   = AstroEntity("Sun","orange", 7, 0, 0, "sun.gif")
        self.earth = create_astro_obj("Earth", "blue", 0.5, 400, 1, "earth.gif")
        self.moon  = create_astro_obj("Moon", "gray", 1, 120, 5, "moon.gif")



    def animate(self):
        """
        Animate the motion of celestial bodies within the solar system.
        """
        earth = self.earth
        earth.angle = math.radians(earth.body.heading())
        earth.update_position()
        earth.rotate()
    
        moon = self.moon
        moon.angle = math.radians(moon.body.heading())
        moon.update_moon_position(earth)
        moon.rotate()
    
        
        turtle.ontimer(self.animate, 10)


def main():
    """
    Main function to create and animate the solar system.
    """
    solar_system = SolarSystem()
    solar_system.animate()
    turtle.done()

if __name__ == "__main__":
    main()
