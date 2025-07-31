import cv2
import numpy as np

# Settings
center_x = 300
center_y = 200
spacing = 40  # Distance between dots
dot_radius = 10
border_thickness = 2

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
        "w": (125, 125, 125),
        "yel": (175, 160, 65),
        "red": (150, 48, 36),
        "orange": (198, 99, 35),
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

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip frame horizontally
    frame_width = frame.shape[1]

    cube_face = []
    for (x, y) in grid_points:
        flipped_x = frame_width - x  # Mirror x-coordinate

        # Get average color from 10x10 patch
        roi = frame[y - 5:y + 5, flipped_x - 5:flipped_x + 5]
        avg_bgr = np.mean(roi.reshape(-1, 3), axis=0).astype(int)
        color_name = get_color_name(avg_bgr)
        cube_face.append(color_name)

        # Draw black circle as border
        cv2.circle(frame, (flipped_x, y), dot_radius + border_thickness, (0, 0, 0), -1)

        # Draw inner circle with the detected color
        color_bgr = tuple(map(int, avg_bgr))
        cv2.circle(frame, (flipped_x, y), dot_radius, color_bgr, -1)

        # Draw flipped color name
        cv2.putText(frame, color_name, (flipped_x - 25, y -30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        print(b,g,r)
    cv2.imshow("Rubik's Cube Color Detection", cv2.flip(frame,1))
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Detected colors:", cv2.flip(cube_face,1))
        break

cap.release()
cv2.destroyAllWindows()
