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
    bw, bh = button_size
    if event == cv2.EVENT_LBUTTONDOWN:
        if bx <= x <= bx + bw and by <= y <= by + bh:
            capture_enabled = True
            if f != 6:
                f+=1
            else:
                f = 6
cap = cv2.VideoCapture(0)
cv2.namedWindow("Rubik's Cube Color Detection")
cv2.setMouseCallback("Rubik's Cube Color Detection", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Do NOT flip the frame — keep orientation correct
    # frame = cv2.flip(frame, 1)  ← REMOVED

    current_face = []
    for (x, y) in grid_points:
        # Get average color from 10x10 patch
        roi = frame[y - 5:y + 5, x - 5:x + 5]
        if roi.size == 0:
            continue  # Avoid errors if ROI goes out of frame

        avg_bgr = np.mean(roi.reshape(-1, 3), axis=0).astype(int)
        color_name = get_color_name(avg_bgr)
        current_face.append(color_name)

        # Draw black border circle
        cv2.circle(frame, (x, y), dot_radius + border_thickness, (0, 0, 0), -1)

        # Draw inner colored circle
        color_bgr = tuple(map(int, avg_bgr))
        cv2.circle(frame, (x, y), dot_radius, color_bgr, -1)

        # 
