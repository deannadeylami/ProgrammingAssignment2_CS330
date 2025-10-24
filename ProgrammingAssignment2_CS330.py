# Programming Assignment 1
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

class SteeringOutput:
    def __init__(self):
        self.linear = Vector([0,0])
        self.angular = 0.0
    
class Character:
    def __init__(self, char_id: int, steer: str, position: Vector, 
                 velocity: Vector, orientation: float, max_vel: int, 
                 max_accel: float, target: int, arrive_radius: int, 
                 slow_radius: int, time_to_target: int):
        self.char_id = char_id
        self.steer = steer
        self.position = position
        self.velocity = velocity
        self.orientation = orientation
        self.max_vel = max_vel
        self.max_accel = max_accel
        self.target = target
        self.arrive_radius = arrive_radius
        self.slow_radius = slow_radius
        self.time_to_target = time_to_target
        self.rotation = 0.0

# Initalize 4 characters w/ parameters from assignment
character1 = Character(char_id=2601, 
                       steer=1, 
                       position=Vector([0,0]), 
                       velocity=Vector([0,0]), 
                       orientation=0.0, 
                       max_vel=0, 
                       max_accel=0.0, 
                       target=0, 
                       arrive_radius=0, 
                       slow_radius=0, 
                       time_to_target=0)
character2 = Character(char_id=2602, 
                       steer=6, 
                       position=Vector([-30, -50]), 
                       velocity=Vector([2,7]), 
                       orientation=(math.pi)/4, 
                       max_vel=8, 
                       max_accel=1.5, 
                       target=1, 
                       arrive_radius=0, 
                       slow_radius=0, 
                       time_to_target=0)
character3 = Character(char_id=2603, 
                       steer=7, 
                       position=Vector([-50,40]), 
                       velocity=Vector([0,8]), 
                       orientation=(3*(math.pi))/2, 
                       max_vel=8, 
                       max_accel=2.0, 
                       target=1, 
                       arrive_radius=0, 
                       slow_radius=0,
                       time_to_target=0)
character4 = Character(char_id=2604, 
                       steer=8, 
                       position=Vector([50,75]), 
                       velocity=Vector([-9,4]), 
                       orientation=math.pi, 
                       max_vel=10, 
                       max_accel=2.0, 
                       target=1, 
                       arrive_radius=4, 
                       slow_radius=32, 
                       time_to_target=1)

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

    return steering

# continue whatever character is doing 
# but currently it just does nothing so idk 
# named it this cuz just "continue" is a reserved word BOOOO
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

characters = [character1, character2, character3, character4]

time_step = 0.5
start_time = 0
end_time = 50

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