from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import numpy as np
import time
from adcdata import *
import math
import comm

#setting up arrays from the data file 
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
#opening up the file and then reading and appending to arrays declared above
artemisPath= open("assets/NASA_ADC_Data_Update.csv", "r")  
for line in artemisPath:
    entries = line.split(",")
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

Sky(texture="assets/space")

#things for the timeline
is_paused = True
timeline_width = 12
start_x = -6
current_x = start_x
move_speed = 0.1

pos=0
rocketX=0
rocketY=0
rocketZ=0

window.title = "Astrovia"
window.icon = "assets/space.png"

max_frames = 60
window.fps_counter.max = 60

paused = False

light_angle = 0
light_radius = 40

moon_angle = 0
moon_radius = 4914.3


pathScale = 45

def update():
#controlle compabtitly probably wont use
    move_direction = Vec3(held_keys['gamepad right stick x'], held_keys['gamepad right stick y'], 0).normalized()
    player.position += move_direction * 1
    move_direction = Vec3(held_keys['gamepad left stick x'], held_keys['gamepad left stick y'], 0).normalized()
    player.position -= move_direction * 1
# setting some variables for the future.
    global moon_angle
    global light_angle
    global pos
    global rocketX
    global rocketY
    global rocketZ
    
    earth.rotation_y -= 0.1
    
    moon_angle += 0.0 
    
    light_angle += 0.1
    light_x = earth.x - moon_radius * np.cos(np.radians(moon_angle))
    light_z = earth.z - moon_radius * np.sin(np.radians(moon_angle))
    pivot.position = (light_x, 2, light_z)

    if not is_paused:
        pos = pos + 10
        if pos < len(rx):
            rocket.x = getAny(rx, pos) / pathScale
            rocket.z = getAny(rz, pos) / pathScale
            rocket.y = getAny(ry, pos) / pathScale

            # velocity display
            velocity_text.text = f"VX: {getAny(vx, pos):.2f}\nVY: {getAny(vy, pos):.2f}\nVZ: {getAny(vz, pos):.2f}"

            # Update timeline
            global current_x
            if not drag_timeline.dragging:
                # Calculate the x position based on the fill bar's scale
                current_x = start_x + fill_bar.scale_x * (abs(start_x * 2) / timeline_width)
                drag_timeline.x = current_x

    elif drag_timeline.dragging:
        current_x = drag_timeline.x
        # When dragging, update the pos and fill bar accordingly
        pos = int((drag_timeline.x - start_x) / (abs(start_x * 2) / timeline_width) * len(rx))
        fill_bar.scale_x = timeline_width * (pos / len(rx))
    
    update_time()
    update_fill_bar()
    #keeps updating time 
def update_time():
    if pos < len(mins):
        colorize_thingies(pos)
        time_box.text = f"Time: {mins[pos]}"
    #the green bar that fills up the red one 
def update_fill_bar():
     if pos < len(rx):
        relative_pos = pos / len(rx)
        fill_bar.scale_x = timeline_width * relative_pos
#link budget
def colorize_thingies(num):
    wpsa_text.color=color.gray
    ds24_text.color=color.gray
    ds34_text.color=color.gray
    ds54_text.color=color.gray
    triplets = comm.antennaSeq
    print("length: " + str(len(triplets)))
    print("index" + str(num))
    curr = triplets[num]
    one = curr[0]
    match one:
        case 'wpsa':
            wpsa_text.color=color.green
        case 'ds24':
            ds24_text.color=color.green
        case 'ds34':
            ds34_text.color=color.green
        case 'ds54':
            ds54_text.color=color.green
    two = curr[1]
    match two:
        case 'wpsa':
            wpsa_text.color=color.yellow
        case 'ds24':
            ds24_text.color=color.yellow
        case 'ds34':
            ds34_text.color=color.yellow
        case 'ds54':
            ds54_text.color=color.yellow
    three = curr[2]
    match three:
        case 'wpsa':
            wpsa_text.color=color.red
        case 'ds24':
            ds24_text.color=color.red
        case 'ds34':
            ds34_text.color=color.red
        case 'ds54':
            ds54_text.color=color.red
# how to restart 
def restart_program():
    global pos, is_paused, current_x
    
    # Reset rocket position
    pos = 0
    rocket.x = getAny(rx, pos) / pathScale
    rocket.z = getAny(rz, pos) / pathScale
    rocket.y = getAny(ry, pos) / pathScale
    
    # Reset timeline
    is_paused = True
    current_x = start_x
    drag_timeline.x = current_x
    fill_bar.scale_x = 0
    
    # Reset time and velocity displays
    time_box.text = "Time: 0.0"
    velocity_text.text = "VX: 0.0\nVY: 0.0\nVZ: 0.0"
    
    # Reset button text
    button.text = "play"

def input(key):
    #how to move around up and down 
    if held_keys['space']:
        player.y += 1200 * time.dt
    if held_keys['control']:
        player.y -= 1200 * time.dt
    if key == 'escape':
        quit()     #ends programs
    
    global is_paused
    #actually how to start the the game
    if key == 't':
        is_paused = not is_paused
        button.text = "play" if is_paused else "pause"
        print("Button clicked - State:", "paused" if is_paused else "playing")
        # restarts but have to press t after the run 
    if key == 'r':
        restart_program()
# creating class for each major entity: Earth, Moon, Rocket
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
       # self.shader = lit_with_shadows_shader
        self.texture = texture
        self.name = name 

button = Button(
    text="pause",
    color=color.black,
    scale=(0.1, 0.1),
    position=(-0.71, -0.37,1),
    on_click=input
)

# Timeline container
timeline_width = 0.8 * window.aspect_ratio  # Width as a fraction of screen width
timeline_height = 0.03  # Height as a fraction of screen height
timeline_y_position = -0.45  # Adjust vertical position
#creation of timeline
fill_box = Entity(
    parent=camera.ui,
    model='quad',
    color=color.red,
    scale=(timeline_width, timeline_height),  # Adjust width and height dynamically
    position=(0, timeline_y_position),  # Centered horizontally
)

# Timeline progress bar 
fill_bar = Entity(
    parent=camera.ui,
    model='quad',
    color=color.green,
    scale=(0.01, timeline_height),  # Initially narrow, matches `fill_box` height
    position=(-timeline_width / 2, timeline_y_position),  # Align left edge
    origin=(-0.5, 0.5),  # Grow from the left
)

# Draggable marker
drag_timeline = Draggable(
    parent=camera.ui,
    model='quad',
    color=color.white,
    scale=(0.07, timeline_height * .5),  # Visible marker
    position=(-timeline_width / 2, timeline_y_position),  # Start at the left of the timeline
    lock=(0, 1, 0),  # Restrict dragging along X
)
#text for on screen
time_box = Text(
    text="Time: 0.0",
    position=(-0.1, -0.4),  # Raised higher
    scale=1.5,
    color=color.white,
    # parent = camera.ui
)
velocity_text = Text(
    text="VX: 0.0\nVY: 0.0\nVZ: 0.0",
    position=(-0.7, 0.45),  # Top-left corner
    scale=1.5,
    color=color.white,
    parent=camera.ui
)

wpsa_text = Text(
    text="WPSA",
    position=(.7, 0.45),  # Raised higher
    scale=1.5,
    color=color.white,
    parent = camera.ui
)
ds24_text = Text(
    text="DS24",
    position=(.7, 0.4),  # Raised higher
    scale=1.5,
    color=color.white,
    parent = camera.ui
)
ds34_text = Text(
    text="DS34",
    position=(.7, 0.35),  # Raised higher
    scale=1.5,
    color=color.white,
    parent = camera.ui
)
ds54_text = Text(
    text="DS54",
    position=(.7, 0.3),  # Raised higher
    scale=1.5,
    color=color.white,
    parent = camera.ui
)
#position of earth mooon and rocket and their models
earth = Planet(0, -.1, 0, 151.860404762, 'assets/8k_earth_daymap', "Earth")#911.162428571
moon = Moon(-8470, -2935, -1380, 41.00230928574, 'assets/8k_moon', "Moon")
rocket = Rocket(rocketX, rocketY, rocketZ, 1, 'assets/Solid20Neon20Green-600x400' ,"Rocket") 

#Orbit
size = len(rx) - 3

points = []
secondPoints = []
pathScale2 = 45

half = 6488

for i in range(1, size - half):
    points.append(Vec3(float(rx[i])/pathScale2, float(ry[i])/pathScale2, float(rz[i])/pathScale2))
# first half of the rocket path
curve_renderer = Entity(
    model=Mesh(vertices=points, mode='line', thickness=2.5), 
    color=color.yellow, 
    unlit=True  # This ensures the color is not affected by lighting
)


for i in range(size - half, size):
    secondPoints.append(Vec3(float(rx[i])/pathScale2, float(ry[i])/pathScale2, float(rz[i])/pathScale2))

# second half of the rocket path
Secondcurve_renderer = Entity(
    model=Mesh(vertices=secondPoints, mode='line', thickness=2.5), 
    color=color.cyan, 
    unlit=True  # This ensures the color is not affected by lighting
)

player = FirstPersonController(position=(-150, 300, -3500), gravity=0, speed=1000)

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True)

app.run()
