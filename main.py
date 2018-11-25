import matplotlib.pyplot as plt
import random
from PIL import Image
from PIL import ImageOps 
import time
import pandas as pd 

NUM_IMAGES = 10000
NUM_TRAJECTORIES_PER_IMAGE = 1

IMAGE_WIDTH, IMAGE_HEIGHT = 500, 500

dt = .01
G = 1000
EARTH_ACCEL = -9.8

def getXYAccel(x, y, obj):
    dist = ((obj["x"] - x)**2 + (obj["y"] - y)**2)**.5
    x_dist = obj["x"] - x
    y_dist = obj["y"] - y
    
    accel_mag = G*obj["m"]/(dist**2)
    x_accel = accel_mag * x_dist/dist
    y_accel = accel_mag * y_dist/dist

    return x_accel, y_accel


def getInitialParameters():
    x = 0
    y = 50 + random.random()*(IMAGE_HEIGHT - 50)
    vx = random.random()*50 + 20
    # vy = random.random()*100 + 30
    vy = 0
    return (x,y,vx,vy)
    

def getTrajectory(initial_parameters, objects):
    x, y, vx, vy = initial_parameters

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

initial_parameters_for_csv = []

tic = time.clock()
for iter in range(NUM_IMAGES):
    # Draw objects
    for obj in objects:
        circle = plt.Circle((obj["x"], obj["y"]), radius=obj["m"] * .1, fc='y')
        plt.gca().add_patch(circle)

    # initialize parameters
    initial_parameters = getInitialParameters()
    initial_parameters_for_csv.append(initial_parameters)
    traj_points = getTrajectory(initial_parameters, objects)
    line = plt.Polygon(traj_points, closed=None, fill=None, linewidth=10)
    plt.gca().add_line(line)

    if iter % 100 == 0:
        toc = time.clock()
        print ("Created " + str(iter) + " of " + str(NUM_IMAGES) + ". Its been " + "{0:.2f}".format(toc - tic) + " seconds.")


    plt.axis('off')
    plt.axis('scaled')
    plt.xlim(0, IMAGE_WIDTH)
    plt.ylim(0, IMAGE_HEIGHT)

    folder_name = "vx_h"
    image_file_name = folder_name + "/images/example_" + str(iter) + ".png"
    plt.savefig(image_file_name, bbox_inches='tight', pad_inches=0)
 
    plt.gcf().clear()
        
    
    #Resize images to 28x28
    img = Image.open(image_file_name)
    img = img.resize((28, 28), Image.ANTIALIAS)
    img.save(image_file_name, format='PNG')

initial_parameters_for_csv = [["{0:.2f}".format(el) for el in row] for row in initial_parameters_for_csv]
df = pd.DataFrame(initial_parameters_for_csv)
df.to_csv(folder_name +"/initial_parameters.csv", header=None, index=None)