# make sure to import * from vectors
from vectors import *


# create new vector (a vector can have 1 to 4 dimensions)
speed = Vector(3, 2, 4) 
speed = Vector((3, 2, 4))

# print vector
print(speed)


# print vector type
print(speed.type)
print(vtype(speed))
print(vectortype(speed))


# print the value corresponding to any of a vector's dimensions
print(speed.x)


# create a new vector
accel = Vector(2, 2, 2)


# add up vectors
newspeed = speed + accel
speed += accel
speed += 1
speed += (1,2,3)
speed += [1,2,3]
# subtraction, multiplication, division and so on are similar


# reassign any of the vector's values
speed.x = 5
speed[0] = 5


# or reassign all using a tuple
speed = Vector(5,6,7) 
# be sure to use Vector() !


# convert vector to tuple
newtuple = unvector(speed)
newtuple = unv(speed)


# get magnitude of vector
my_mag = magnitude(speed)
my_mag = mag(speed)
my_mag = speed.magnitude()
my_mag = speed.mag()


# get normalized vector
my_norm = normalized(speed)
my_norm = norm(speed)
my_norm = speed.normalized()
my_norm = speed.norm()


# get positive vector
my_pos_vec = positive(speed)
my_pos_vec = speed.positive()