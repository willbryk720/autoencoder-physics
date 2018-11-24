import matplotlib.pyplot as plt
import random
from PIL import Image
from PIL import ImageOps 

IMAGE_WIDTH, IMAGE_HEIGHT = 500, 500

dt = .01
G = 1000
EARTH_ACCEL = -9.8

NUM_IMAGES = 5000
NUM_TRAJECTORIES_PER_IMAGE = 1

def getXYAccel(x, y, obj):
    dist = ((obj["x"] - x)**2 + (obj["y"] - y)**2)**.5
    x_dist = obj["x"] - x
    y_dist = obj["y"] - y
    
    accel_mag = G*obj["m"]/(dist**2)
    x_accel = accel_mag * x_dist/dist
    y_accel = accel_mag * y_dist/dist

    return x_accel, y_accel


def getTrajectory(x, y, vx, vy, objects):
    trajectory = []
    t = 0
    while x >= 0 and x <= IMAGE_WIDTH and y >= 0 and y <= IMAGE_HEIGHT:
        # Get accelerations from objects 
        x_accel = 0
        y_accel = 0
        for obj in objects:
            x_acc, y_acc = getXYAccel(x, y, obj)
            x_accel += x_acc
            y_accel += y_acc
        
        # print x_accel, y_accel, EARTH_ACCEL

    
        # Update velocities with accelerations from objects
        vx = vx + dt*x_accel
        vy = vy + dt*y_accel

        # Update y velocity with Gravity
        vy = vy + dt*EARTH_ACCEL

        # Update position
        x = x + dt*vx
        y = y + dt*vy

        trajectory.append([x,y])
    return trajectory



planet1 = {"x": 300, "y": 400, "m": 100}
planet2 = {"x": 400, "y": 200, "m": 100}

# objects = [planet1, planet2]
objects = []

for iter in range(NUM_IMAGES):
    # Draw objects
    for obj in objects:
        circle = plt.Circle((obj["x"], obj["y"]), radius=obj["m"] * .1, fc='y')
        plt.gca().add_patch(circle)

    for i in range(NUM_TRAJECTORIES_PER_IMAGE):
        x = 0
        y = 0
        vx = random.random()*50 + 20
        vy = random.random()*100 + 30
        traj_points = getTrajectory(x, y, vx, vy, objects)
        line = plt.Polygon(traj_points, closed=None, fill=None, linewidth=6)
        plt.gca().add_line(line)

    # plt.axes()
    # plt.axis('scaled')
    plt.axis('off')
    plt.xlim(0, IMAGE_WIDTH)
    plt.ylim(0, IMAGE_HEIGHT)
    # plt.figure(figsize=(800/my_dpi, 800/my_dpi))

    image_file_name = "images/vx_vy/example_" + str(iter) + ".png"
    plt.savefig(image_file_name)

    # plt.show()
    plt.gcf().clear()
        
    
    # Resize images to 28x28
    img = Image.open(image_file_name)
    img = img.resize((28, 28), Image.ANTIALIAS)
    img.save(image_file_name, format='PNG')