# Programming Assignment 2
# Class: CS 330-01
# Term: Fall 2025
# Author: Deanna Deylami & Lucas Geiger
# Date: 10/26/2025
# Purpose: Implement & Test the dynamic Follow path behavior. 

import math

# Initialize classes
class Vector:
    def __init__(self, vector: list):
        self.vector = vector

    # Support Section | Vector and geometry functions 
    # Calculate length of 2D vector
    # Formula: |v| = √(x² + z²)
    def length(self):
        length = math.sqrt((self.vector[0]**2) + (self.vector[1]**2))
        return length

    # Normalize a 2D vector (vector should be a list here).
    # Formula: (x/|v|, z/|v|)
    def normalize(self):
        vector_len = self.length()
        if (vector_len != 0):
            self.vector[0] = self.vector[0] / vector_len
            self.vector[1] = self.vector[1] / vector_len
        return self
    
    # Calculate scalar dot product of two 2D vectors
    # Formula: A · B 
    def vector_dot(A,B):
        sum = (A[0] * B[0]) + (A[1] * B[1])
        return (sum)

    # Calculate distance between two points in 2D.
    # Formula used: d = √[(x₂ - x₁)² + (y₂ - y₁)²]
    def distance_points(A, B):
        distance1 = (B[0] - A[0]) ** 2
        distance2 = (B[1] - A[1]) ** 2
        distance = math.sqrt(distance1 + distance2)
        return (distance)
    
    def closest_point(Q, A, B):
        Q_A = (Q[0] - A[0], Q[1] - A[1])
        B_A = (B[0] - A[0], B[1] - A[1])
        numerator = Vector.vector_dot(Q_A, B_A)
        denominator = Vector.vector_dot(B_A, B_A)
        T = numerator / denominator
        return ((A[0] + (T * B_A[0])), (A[1] + (T * B_A[1])))

class SteeringOutput:
    def __init__(self):
        self.linear = Vector([0,0])
        self.angular = 0.0
    
class Character:
    def __init__(self, char_id: int, steer: str, position: Vector, 
                 velocity: Vector, orientation: float, max_vel: int, 
                 max_accel: float, path_to_follow: int, path_offset: float):
        self.char_id = char_id
        self.steer = steer
        self.position = position
        self.velocity = velocity
        self.orientation = orientation
        self.max_vel = max_vel
        self.max_accel = max_accel
        self.path_to_follow = path_to_follow
        self.path_offset = path_offset
        self.rotation = 0.0

class Path:
    def __init__(self):
        self.ID = 0
        self.x = []
        self.z = []
        self.params = []
        self.distance = []
        self.segments = 0

    def path_assemble(self, ID, X, Z):
        self.ID = ID
        self.x = X
        self.z = Z
        self.segments = len(X) - 1
        
        self.distance = [0] * (self.segments + 1)
        for i in range(1, self.segments + 1):
            XZ_1 = (X[i-1], Z[i-1])
            XZ_2 = (X[i], Z[i]) 
            XZ_distance = Vector.distance_points(XZ_1, XZ_2)
            self.distance[i] = self.distance[i-1] + XZ_distance
        
        self.param = [0] * (self.segments + 1)
        for i in range(1, self.segments + 1):
            self.param[i] = self.distance[i] / max(self.distance)




    def get_params(self, position):
        # LUCAS here
        return
    
    def get_position(self, param):
        # LUCAS here
        return

# Initalize 1 character w/ parameters from assignment
character1 = Character(char_id=2701, 
                       steer=11, 
                       position=Vector([20,95]), 
                       velocity=Vector([0,0]), 
                       orientation=0.0, 
                       max_vel=4, 
                       max_accel=2.0, 
                       path_to_follow=1, 
                       path_offset=0.04)

# Path Vertices parameters given by assignment.
path_vertices = [
    (0, 90),
    (-20, 65),
    (20, 40),
    (-40, 15),
    (40, -10),
    (-60, -35),
    (60, -60),
    (0, -85)
]

# Move Section
def compute_steer(character: Character):
    if character.steer == 1:
        steering = steer_continue(character)
    if character.steer == 6:
        steering = steer_seek(character, character1)
    if character.steer == 7:
        steering = steer_flee(character, character1)
    if character.steer == 8:
        steering = steer_arrive(character, character1)
    if character.steer == 11:
        steering = steer_follow(character, character1)
    return steering

def steer_follow(character: Character):
    result = SteeringOutput()
    # LUCAS here
    return result

def steer_continue(character: Character): 
    result = SteeringOutput()
    return result

def steer_seek(character: Character, target: Character): # kept the naming convention to be consistent
    # Create output structure
    result = SteeringOutput()

    # Get the direction to the target
    result.linear.vector[0] = target.position.vector[0] - character.position.vector[0]
    result.linear.vector[1] = target.position.vector[1] - character.position.vector[1]

    # Accelerate at maximum rate
    result.linear.normalize()
    result.linear.vector[0] *= character.max_accel
    result.linear.vector[1] *= character.max_accel

    # Output steering
    result.angular = 0
    return result

def steer_flee(character: Character, target: Character):
    # Create output structure
    result = SteeringOutput()

    # Get the direction to the target
    result.linear.vector[0] = character.position.vector[0] - target.position.vector[0]
    result.linear.vector[1] = character.position.vector[1] - target.position.vector[1]

    # Accelerate at maximum rate
    result.linear.normalize()
    result.linear.vector[0] *= character.max_accel
    result.linear.vector[1] *= character.max_accel


    # Output steering
    result.angular = 0
    return result

def steer_arrive(character: Character, target: Character):
    # Create output structure
    result = SteeringOutput()

    # Time over which to achieve target speed
    timeToTarget = character.time_to_target
    
    # Arrival radius & slowing-down radius
    targetRadius = character.arrive_radius
    slowRadius = character.slow_radius
    direction = Vector([0,0])

    # Get the direction and distance to the target
    direction.vector[0] = target.position.vector[0] - character.position.vector[0]
    direction.vector[1] = target.position.vector[1] - character.position.vector[1]

    distance = direction.length()

    # Test for arrival
    if distance < targetRadius:
        result = SteeringOutput()
        return result
    
    # Outside slowing-down (outer) radius, move at max speed
    if distance > slowRadius:
        targetSpeed = character.max_vel

    # Between radii, scale speed to slow down
    else: 
        targetSpeed = character.max_vel * distance / slowRadius
    
    # Target velocity combines speed and direction 
    targetVelocity = Vector([direction.vector[0], direction.vector[1]])
    targetVelocity.normalize()
    targetVelocity.vector[0] *= targetSpeed
    targetVelocity.vector[1] *= targetSpeed

    # Accelerate to target velocity
    result.linear.vector[0] = targetVelocity.vector[0] - character.velocity.vector[0]
    result.linear.vector[1] = targetVelocity.vector[1] - character.velocity.vector[1]

    result.linear.vector[0] /= timeToTarget
    result.linear.vector[1] /= timeToTarget

    # Test if too fast acceleration
    if result.linear.length() > character.max_accel:
        result.linear.normalize()
        result.linear.vector[0] *= character.max_accel
        result.linear.vector[1] *= character.max_accel

    # Output steering 
    result.angular = 0
    return result
        

def update(character: Character, steering: SteeringOutput, time: float):
    # Update the position and orientation
    character.position.vector[0] += character.velocity.vector[0] * time
    character.position.vector[1] += character.velocity.vector[1] * time
    character.orientation += character.rotation * time

    # Update the velocity and rotation
    character.velocity.vector[0] += steering.linear.vector[0] * time
    character.velocity.vector[1] += steering.linear.vector[1] * time
    character.rotation += steering.angular * time

    # Check for speed above max and clip
    if (character.velocity.length() > character.max_vel):
        character.velocity = character.velocity.normalize()
        character.velocity.vector[0] *= character.max_vel
        character.velocity.vector[1] *= character.max_vel

# Print out to text file
def record(sim_time, char_id, pos_x, pos_z, vel_x, vel_z, lin_acc_x, lin_acc_z, orientation, steer_behavior, coll_status):
    with open("output.txt", "a") as file:
        file.write(f"{sim_time}, {char_id}, {pos_x}, {pos_z}, {vel_x:}, {vel_z}, {lin_acc_x}, {lin_acc_z}, {orientation}, {steer_behavior}, {coll_status}\n")

characters = [character1]

time_step = 0.5
start_time = 0
end_time = 125

# Run the thang!!! (from 0 to 50 with 0.5 as increment)
open("output.txt", "w").close()
while (start_time <= end_time):
    for character in characters:
        steering = compute_steer(character)
        record(sim_time=start_time, 
               char_id=character.char_id, 
               pos_x=character.position.vector[0], 
               pos_z=character.position.vector[1], 
               vel_x=character.velocity.vector[0], 
               vel_z=character.velocity.vector[1], 
               lin_acc_x=steering.linear.vector[0], 
               lin_acc_z=steering.linear.vector[1], 
               orientation=character.orientation, 
               steer_behavior=character.steer, 
               coll_status="FALSE")
        update(character, steering, time_step)

    start_time += time_step