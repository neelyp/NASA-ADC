from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import numpy as np
import random
import time
import adcdata
#reading file
from adcdata import *
mins = []
rx = []
ry  = []
rz = []
vx = []
vy = []
vz = []
mass = []
wpsa = []
wpsar = []
ds54 = []
ds54r = []
ds24 = []
ds24r = []
ds34 = []
ds34r = []
artemisPath= open("assets/NASA_ADC_Data_Update.csv", "r")  
for line in artemisPath:
    #get rids of the commas
    entries = line.split(",")
    #append to each array
    mins.append(entries[0])
    rx.append(entries[1])
    ry.append(entries[2])
    rz.append(entries[3])
    vx.append(entries[4])
    vy.append(entries[5])
    vz.append(entries[6])
    mass.append(entries[7])
    wpsa.append(entries[8])
    wpsar.append(entries[9])
    ds54.append(entries[10])
    ds54r.append(entries[11])
    ds24.append(entries[12])
    ds24r.append(entries[13])
    ds34.append(entries[14])
    ds34r.append(entries[15])
artemisPath.close() 
print(str(getAny(mins, 2)))

app = Ursina(borderless=True)
window.cog_button.enabled = True
window.fullscreen = True

pos=0
rocketX=0
rocketY=0
rocketZ=0
# Window  
window.title = "Astrovia"
window.icon = "assets/space.png"

max_frames = 120

window.fps_counter.max = 120

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

pathScale = 35


def update():
    txt_time.text = "Time " + str(timeSkib)
    move_direction = Vec3(held_keys['gamepad right stick x'], held_keys['gamepad right stick y'], 0).normalized()
    player.position += move_direction * .1
    move_direction = Vec3(held_keys['gamepad left stick x'], held_keys['gamepad left stick y'], 0).normalized()
    player.position -= move_direction * .1


    global moon_angle
    global light_angle
    global pos
    global rocketX
    global rocketY
    global rocketZ
    
    # rotate Earth
    earth.rotation_y -= 0.1
    
    # update the moon's position to revolve around the Earth
    moon_angle += 0.1  # adjust speed of revolution here
    moon.x = earth.x + moon_radius * np.cos(np.radians(moon_angle))
    moon.z = earth.z + moon_radius * np.sin(np.radians(moon_angle))
    
    # position the light on the opposite side of the Earth relative to the moon
    light_angle += 0.1
    light_x = earth.x - moon_radius * np.cos(np.radians(moon_angle))
    light_z = earth.z - moon_radius * np.sin(np.radians(moon_angle))
    pivot.position = (light_x, 2, light_z)  # set the light's position
    pos = pos+1
    rocket.x = getAny(rx,pos)/pathScale
    rocket.z = getAny(rz,pos)/pathScale
    rocket.y = getAny(ry,pos)/pathScale
    
    Circle(position=rocket.position)

 

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
        self.model = load_model('artemis 1.stl')
        self.collider = 'cube'
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.shader = lit_with_shadows_shader
        self.texture = texture
        self.name = name 

class Circle(Entity):
    def __init__(self, position):
        super().__init__()
        self.model = 'circle'  # Use a circle model
        self.color = color.white  # Set color to white
        self.scale = 0.1  # Adjust size as needed
        self.position = position  # Set the position to where the rocket touches

# Creates Earth
earth = Planet(0, -.1, 0, 911.162428571, 'assets/8k_earth_daymap', "Earth")

# Creates moon
moon = Moon(4914.3, 500, 0, 248.2, 'assets/8k_moon', "Moon")
 # i think we have to make a variable that hold the arrays from nasa then just adjust the position

# Creates rocket
rocket = Rocket(rocketX, rocketY, rocketZ, 1, 'assets/Solid20Neon20Green-600x400' ,"Rocket") 


Sky(texture="assets/space")

player = FirstPersonController(position=(-150, 300, -3500), gravity=0, speed=1000) #camera

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True)



app.run()