import cv2
import numpy as np
import time
# Settings
center_x = 300
center_y = 200
dot_radius = 10
border_thickness = 2
button_flash_time = -1
  # time.time() when button was last clicked
color_to_hex = {
    'white': "#ffffff",  # or "w" if you really want a symbol
    'yellow': "#ffcf00",
    'blue': "#00008f",
    'green': "#009f0f",
    'orange': "#ff6f00",
    'red': "#cf0000"
}

# Color to face mapping based on center
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
button_size = (610, 40)
capture_enabled = False
capr = []
captured_faces = []
f = 1
wh = []
ye = []
re = []
or2 = []
gr = []
bl = []
center_color = 'white'
inst = [
    '                    capture white and click here',
    'rotate cube upwards and click',
    'rotate the cube so that '+center_color+' face is on the left and then click',
    'rotate the cube so that '+center_color+' face is on the left and then click',
    'rotate the cube so that '+center_color+' face is on the left and then click',
    '                capture '+center_color+'and click here',
    'done'
]

def get_color_name(bgr):
    global r,g,b
    b, g, r = bgr
    colors = {
        "white": (125, 125, 125),
        "yellow": (175, 160, 65),
        "orange": (198, 99, 35),
        "red": (255, 60, 40),
        "red": (165, 45, 32),
        "green": (75, 165, 75),
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
    global f, capture_enabled, button_flash_time
    bx, by = button_pos
    bw, bh = button_size
    if event == cv2.EVENT_LBUTTONDOWN:
        if bx <= x <= bx + bw and by <= y <= by + bh:
            button_flash_time = time.time()  # Set time of press
            capture_enabled = True


# Start camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("Rubik's Cube Color Detection")
cv2.setMouseCallback("Rubik's Cube Color Detection", mouse_callback)
cv2.createTrackbar("Spacing", "Rubik's Cube Color Detection", 80, 160, lambda x: None)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get spacing from slider
    spacing = cv2.getTrackbarPos("Spacing", "Rubik's Cube Color Detection")

    # Generate grid points based on current spacing
    grid_points = [
        (center_x + (col - 1) * spacing, center_y + (row - 1) * spacing)
        for row in range(3)
        for col in range(3)
    ]

    current_face = []
    for (x, y) in grid_points:
        roi = frame[y - 5:y + 5, x - 5:x + 5]
        if roi.size == 0:
            continue

        avg_bgr = np.mean(roi.reshape(-1, 3), axis=0).astype(int)
        color_name = get_color_name(avg_bgr)
        current_face.append(color_name)

        # Draw border
        cv2.circle(frame, (x, y), dot_radius + border_thickness, (0, 0, 0), -1)
        # Draw inner circle
        cv2.circle(frame, (x, y), dot_radius, tuple(map(int, avg_bgr)), -1)
        # Draw label
        text_size = cv2.getTextSize(color_name, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        text_x = x - text_size[0] // 2
        cv2.putText(frame, color_name, (text_x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Handle capture
# Delay capture by 0.3 seconds
    if capture_enabled and (time.time() - button_flash_time >= 0.3):
        capture_enabled = False  # Disable again immediately

        current_face_copy = current_face.copy()
        captured_faces.append(current_face_copy)
        capr.append(current_face_copy)
        center_color = current_face_copy[4]
        inst = [
            'capture white',
            'rotate cube upwards and click',
            'rotate the cube so that ' + center_color + ' face is on the left and click',
            'rotate the cube so that ' + center_color + ' face is on the left and  click',
            'rotate the cube so that ' + center_color + ' face is on the left and click',
            '                capture '+center_color+'and click here',
            'done'
        ]
        if center_color == 'white':
            wh = current_face_copy
        elif center_color == 'yellow':
            ye = np.array(current_face_copy).reshape((3, 3))
            ye = np.rot90(ye, k=1).flatten()
        elif center_color == 'red':
            re = current_face_copy
        elif center_color == 'orange':
            or2 = current_face_copy
        elif center_color == 'green':
            gr = current_face_copy
        elif center_color == 'blue':
            bl = current_face_copy

        print('white', wh)
        print('yellow', ye)
        print('red', re)
        print('orange', or2)
        print('green', gr)
        print('blue', bl)
        print('f', f)
        print("  ")
        
        time.sleep(0.2)  # Slight extra pause after capture
        if f != 7:
            f += 1

    if time.time() - button_flash_time < 0.3:
        color = (0, 200, 0)  # Flash green
    else:
        color = (0, 0, 0)    # Default black
    # Draw capture button
    bx, by = button_pos
    bw, bh = button_size


    cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), color, -1)
    if 1 <= f <= 7:
        cv2.putText(frame, str(inst[f - 1]), (bx + 10, by + 27), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    #print(current_face[4])
    # Show frame    
    
    cv2.imshow("Rubik's Cube Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\nAll captured faces:")
        for i, face in enumerate(captured_faces):
            print(f"Face {i + 1}: {face}")
        break

cap.release()
cv2.destroyAllWindows()
