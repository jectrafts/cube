from twophase import solver as tw

# Facelet data as given
white = ['yellow', 'red', 'white', 'yellow', 'white', 'red', 'green', 'white', 'blue']
yellow= ['red' ,'white', 'red', 'red', 'yellow', 'white', 'red' ,'yellow', 'orange']
red = ['white', 'red', 'yellow', 'blue', 'red', 'orange', 'yellow', 'blue', 'yellow']
orange = ['green', 'yellow', 'green', 'white', 'orange', 'orange', 'white', 'green', 'white']
green = ['orange', 'orange', 'red', 'green', 'green', 'yellow', 'blue', 'green', 'blue']
blue = ['orange', 'blue', 'orange', 'blue', 'blue', 'green', 'green', 'orange', 'blue']

# Ordered by URFDLB
faces = [white, blue, red, yellow, green, orange]

# Create color map based on center stickers
color_map = {
    white[4]: 'U',   # white center
    blue[4]: 'R',    # blue center
    red[4]: 'F',     # red center
    yellow[4]: 'D',  # yellow center
    green[4]: 'L',   # green center
    orange[4]: 'B'   # orange center
}

# Convert to 54-letter cube string
cube_str = ''.join(color_map[color] for face in faces for color in face)

# Solve
solution = tw.solve(cube_str)

# Output
print("Cube string:", cube_str)
print("Solution:", solution)
