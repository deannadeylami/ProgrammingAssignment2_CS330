# Programming Assignment 2
# Class: CS 330-01
# Term: Fall 2025
# Author: Deanna Deylami & Lucas Geiger
# Date: 10/26/2025
# Purpose: Implement & Test the dynamic Follow path behavior. 

import numpy as np # For vector math
import math

# Support Section | Vector and geometry functions 
# Calculate length of 2D vector
# Formula: |v| = √(x² + z²)
def length(self):
    length = math.sqrt((self[0]**2) + (self[1]**2))
    return length

# Normalize a 2D vector (vector should be a list here).
# Formula: (x/|v|, z/|v|)
def normalize(self):
    vector_len = length(self)
    if (vector_len != 0):
        self[0] = self[0] / vector_len
        self[1] = self[1] / vector_len
    return self

# Calculate distance between two points in 2D.
# Formula used: d = √[(x₂ - x₁)² + (y₂ - y₁)²]
def distance_points(A, B):
    distance1 = (B[0] - A[0]) ** 2
    distance2 = (B[1] - A[1]) ** 2
    distance = math.sqrt(distance1 + distance2)
    return (distance)

# Find point on line closest to query point Q, with A and B as the line endpoint vectors
def closest_point(Q, A, B):
    q_a = np.array([Q[0] - A[0], Q[1] - A[1]])
    b_a = np.array([B[0] - A[0], B[1] - A[1]])
    numerator = np.dot(q_a, b_a)
    denominator = np.dot(b_a, b_a)
    t = numerator / denominator
    if (t <= 0):
        return A
    elif (t >= 1):
        return B
    else:
        return np.array([(A[0] + (t * b_a[0])), (A[1] + (t * b_a[1]))])

# Initialize classes
class SteeringOutput:
    def __init__(self):
        self.linear = np.array([0.0, 0.0])
        self.angular = 0.0
    
class Character:
    def __init__(self):
        self.char_id = 0
        self.steer = 2
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.orientation = 0.0
        self.max_vel = 0.0
        self.max_accel = 0.0
        self.path_to_follow = 0
        self.path_offset = 0
        self.rotation = 0.0

class Path:
    def __init__(self):
        self.ID = 0
        self.x = np.array([])
        self.z = np.array([])
        self.params = np.array([])
        self.distance = np.array([])
        self.segments = 0

    def path_assemble(self, ID, X, Z):
        self.ID = ID
        self.x = X
        self.z = Z
        self.segments = len(X) - 1
        
        # Find distance between points on path
        self.distance = [0] * (self.segments + 1)
        for i in range(1, self.segments + 1):
            xz_1 = np.array([X[i-1], Z[i-1]])
            xz_2 = np.array([X[i], Z[i]]) 
            xz_distance = distance_points(xz_1, xz_2)
            self.distance[i] = self.distance[i-1] + xz_distance
        
        # Create parameters for those points
        self.params = [0] * (self.segments + 1)
        for i in range(1, self.segments + 1):
            self.params[i] = self.distance[i] / max(self.distance)

    def get_param(self, position):
        # Find point on path closest to given position
        closestDistance = 9999999 # Really big number since no infinite
        for i in range(0, self.segments):
            a = np.array([self.x[i], self.z[i]])
            b = np.array([self.x[i+1], self.z[i+1]])
            checkPoint = closest_point(position, a, b)
            checkDistance = distance_points(position, checkPoint)
            if (checkDistance < closestDistance):
                closestPoint = checkPoint
                closestDistance = checkDistance
                closestSegment = i
        
        # Calculate path parameter of closest point
        a = np.array([self.x[closestSegment], self.z[closestSegment]])
        paramA = self.params[closestSegment]
        b = np.array([self.x[closestSegment+1], self.z[closestSegment+1]])
        paramB = self.params[closestSegment+1]
        c = closestPoint
        c_a = np.subtract(c, a)
        b_a = np.subtract(b, a)
        t = length(c_a) / length(b_a)
        paramC = paramA + (t * (paramB - paramA))
        return paramC
    
    def get_position(self, param):
        # Find closest parameter less than given param
        paramIndexes = list()
        for p in self.params:
            if (param > p):
                paramIndexes.append(self.params.index(p))
        i = max(paramIndexes)

        # Calculate position
        a = np.array([self.x[i], self.z[i]])
        b = np.array([self.x[i+1], self.z[i+1]])
        t = (param - self.params[i]) / (self.params[i+1] - self.params[i])
        b_a = np.subtract(b, a)
        t_b_a = np.array([t * b_a[0], t * b_a[1]])
        position = np.add(a, t_b_a)
        return position

# Move Section
def steer_seek(character: Character, target) -> SteeringOutput:
    # Create output structure
    result = SteeringOutput()

    # Get the direction to the target
    result.linear[0] = target[0] - character.position[0]
    result.linear[1] = target[1] - character.position[1]

    # Accelerate at maximum rate
    result.linear = normalize(result.linear)
    result.linear[0] *= character.max_accel
    result.linear[1] *= character.max_accel

    # Output steering
    result.angular = 0
    return result

def steer_follow(character: Character, path: Path) -> SteeringOutput:
    # Find current position on path
    currentParam = path.get_param(character.position)

    # Offset it
    targetParam = min(1.0, currentParam + character.path_offset)

    # Get the target position
    targetPosition = path.get_position(targetParam)

    # Delegate to seek
    return steer_seek(character, targetPosition)
        
def update(character: Character, steering: SteeringOutput, time: float):
    # Update the position and orientation
    character.position[0] += character.velocity[0] * time
    character.position[1] += character.velocity[1] * time
    character.orientation += character.rotation * time

    # Update the velocity and rotation
    character.velocity[0] += steering.linear[0] * time
    character.velocity[1] += steering.linear[1] * time
    character.rotation += steering.angular * time

    # Check for speed above max and clip
    if (length(character.velocity) > character.max_vel):
        character.velocity = normalize(character.velocity)
        character.velocity[0] *= character.max_vel
        character.velocity[1] *= character.max_vel

# Initalize 1 character w/ parameters from assignment
character = Character()
character.char_id = 2701
character.steer = 11
character.position = np.array([20.0, 95.0])
character.velocity = np.array([0.0, 0.0])
character.orientation = 0
character.max_vel = 4
character.max_accel = 2
character.path_to_follow = 1
character.path_offset = 0.04

# Make path to follow
path = Path()
X = (0, -20, 20, -40, 40, -60, 60, 0)
Z = (90, 65, 40, 15, -10, -35, -60, -85)
path.path_assemble(1, X, Z)

# Print out to text file
def record(sim_time, char_id, pos_x, pos_z, vel_x, vel_z, lin_acc_x, lin_acc_z, orientation, steer_behavior, coll_status):
    with open("output.txt", "a") as file:
        file.write(f"{sim_time}, {char_id}, {pos_x}, {pos_z}, {vel_x:}, {vel_z}, {lin_acc_x}, {lin_acc_z}, {orientation}, {steer_behavior}, {coll_status}\n")

time_step = 0.5
start_time = 0
end_time = 125

# Run the thang!!! (from 0 to 50 with 0.5 as increment)
open("output.txt", "w").close()
while (start_time <= end_time):
    steering = steer_follow(character, path)
    record(sim_time=start_time, 
            char_id=character.char_id, 
            pos_x=character.position[0], 
            pos_z=character.position[1], 
            vel_x=character.velocity[0], 
            vel_z=character.velocity[1], 
            lin_acc_x=steering.linear[0], 
            lin_acc_z=steering.linear[1], 
            orientation=character.orientation, 
            steer_behavior=character.steer, 
            coll_status="FALSE")
    update(character, steering, time_step)

    start_time += time_step