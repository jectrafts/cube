import cv2
import numpy as np

# Settings
center_x = 300
center_y = 200
spacing = 70  # Distance between dots
dot_radius = 10
border_thickness = 2
# Based on center sticker colors:
ctof = {
    'white': 'U',
    'red': 'R',
    'green': 'F',
    'yellow': 'D',
    'orange': 'L',
    'blue': 'B'
}

# Button settings
button_pos = (20, 20)
button_size = (120, 40)
capture_enabled = False
capr = []
captured_faces = []
f=0
wh = []
ye = []
re= []
or2= []
gr= []
bl= []
r = []
inst = [
    'capture white',
    'capture red',
    'capture green',
    'capture yellow',
    'capture orange',
    'capture blue' ,
]

# Generate 3x3 grid points centered around (center_x, center_y)
grid_points = [
    (center_x + (col - 1) * spacing, center_y + (row - 1) * spacing)
    for row in range(3)
    for col in range(3)
]

def get_color_name(bgr):
    global b, g, r
    b, g, r = bgr
    colors = {
        "white": (125, 125, 125),
        "yellow": (175, 160, 65),
        "orange": (198, 99, 35),
        "green": (75, 165, 75),
        "red": (255, 60, 40),
        "red": (165, 45, 32),
        "blue": (42, 92, 138)
    }
    min_dist = float('inf')
    closest = "unknown"
    for name, val in colors.items():
        dist = np.linalg.norm(np.array(val) - np.array((r, g, b)))
        if dist < min_dist:
            min_dist = dist
            closest = name
    return closest

def mouse_callback(event, x, y, flags, param):
    global f
    global capture_enabled
    bx, by = button_pos
    bw, bh = button_s