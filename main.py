from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import numpy as np
import random
import time
from adcdata import *

app = Ursina(borderless=True)
window.cog_button.enabled = True
window.fullscreen = True



# Window  
window.title = "Astrovia"
window.icon = "assets/space.png"

max_frames = 60

window.fps_counter.max = 60 

paused = False

light_angle = 0
light_radius = 40

# define variables for the moon
moon_angle = 0
moon_radius = 4914.3  # distance from the Earth to the moon

timeSkib = time.time()
txt_TimeOfMission = Text(text = "Time: " ,position=(-0.8,0.4), origin=(0,0), scale=1)
txt_PositionOfRocket = Text(text = "Position: " ,position=(-0.8,0.45), origin=(0,0), scale=1)
txt_time = Text(text = "Time: " + str(timeSkib), position=(-0.8,0.), origin=(0,0), scale=1)


def update():

    txt_time.text = "Time " + str(timeSkib)
    move_direction = Vec3(held_keys['gamepad right stick x'], held_keys['gamepad right stick y'], 0).normalized()
    player.position += move_direction * .1
    move_direction = Vec3(held_keys['gamepad left stick x'], held_keys['gamepad left stick y'], 0).normalized()
    player.position -= move_direction * .1


    global moon_angle
    global light_angle
    
    # rotate Earth
    earth.rotation_y -= 0.1
    
    # update the moon's position to revolve around the Earth
    moon_angle += 0.01  # Adjust speed of revolution here
    moon.x = earth.x + moon_radius * np.cos(np.radians(moon_angle))
    moon.z = earth.z + moon_radius * np.sin(np.radians(moon_angle))
    
    # position the light on the opposite side of the Earth relative to the moon
    light_angle += 0.01
    light_x = earth.x - moon_radius * np.cos(np.radians(moon_angle))
    light_z = earth.z - moon_radius * np.sin(np.radians(moon_angle))
    pivot.position = (light_x, 2, light_z)  # set the light's position

 

def input(key):
    if held_keys['space']:
        player.y += 1200 * time.dt
    if held_keys['control']:
        player.y -= 1200 * time.dt
    if key == 'escape':
        quit()

class Planet(Entity):   
    def __init__(self, x, y, z, scale, texture, name):
        super().__init__()
        self.model = load_model('earthModel.blend')
        self.collider = 'sphere'
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.shader = lit_with_shadows_shader
        self.texture = texture
        self.name = name

class Moon(Entity):
    def __init__(self, x, y, z, scale, texture, name):
        super().__init__()
        self.model = load_model('earthModel.blend')  
        self.collider = 'sphere'
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.shader = lit_with_shadows_shader
        self.texture = texture
        self.name = name 

class Rocket(Entity):
    def __init__(self, x, y, z, scale, texture, name):
        super().__init__()
        self.model = load_model('rocket.blend')
        self.collider = 'cube'
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.shader = lit_with_shadows_shader
        self.texture = texture
        self.name = name 

# Creates Earth
earth = Planet(0, -.1, 0, 911.162428571, 'assets/8k_earth_daymap', "Earth")

# Creates moon
moon = Moon(4914.3, 500, 0, 248.2, 'assets/8k_moon', "Moon")
rocketX = 2000
# Creates rocket
rocket = Rocket((4000), 500, 0, 200, 'assets/Solid20Neon20Green-600x400', "Rocket") 

Sky(texture="assets/space")

player = FirstPersonController(position=(-150, 300, -3500), gravity=0, speed=1000) #camera

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True)


app.run()