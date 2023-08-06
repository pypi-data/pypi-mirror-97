# Made By Snehashish Laskar
# Made on 06-03-2021
# This can be used to calculate usefull things using physics formulae
# This can be used By teachers if they want to correct the exam pappers easily and without doing any calculations! 
'''
	Instructions:
	-> Please follow the notes written below for help!
	-> Please do not enter the Units of the numbers below!

'''

def calculate_acceleration_with_force(force, mass):
	# Please enter the net force and mass as parameters
	# it can be used to calculate acceleration from net force and mass
	equation1 = force/mass
	print(f"The acceleratin is equal to : {equation1} m/s squared")

def calculate_acceleration_with_velocity(velocity, time):
	# Please enter the change in velocity with the time intervals as parameters
	# Please give the velocity in m/s
	# This can be used to calculate the acceleration from change in velocity and time intervals
	equation2 = velocity/time 
	print(f"acceleration is equal to {equation2} m/s squared")

def calculate_avg_speed(distance, time):
	# Please enter the toatal distance and time intervals as parameters 
	# Please give the distance in meters only
	# This can be used to calculate average speed from toatl distamce and time
	equation3 = distance/time
	print(f" the average speed is equal to {equation3}m/s ")

def calculate_momentum(mass, velocity):
	# Please pass the mass and the velocity as parameters
	# Please give mass on Kg's only!
	# this Function can be used to calaculate the momentum of an object from its velocity and mass!
	equation4 = mass*velocity
	print(f"The momentum of this object is {equation4} kg m/s")

def calculate_distance(avg_speed, time):
	# Please pass the average speed and time as parameters
	# Please give speed in m/s only!
	# This Function can be used to calculate the distance from Average speed and time
	equation5 = avg_speed*time
	print(f"disctance covered id equal to {equation5}m")

def calculate_distance_from_acceleration(acceleration, time):
	# Please pass the acceleration and time as parameters
	# Please give the acceleration in m/s
	# This Function can be used to calculate the distance from acceleration and time
	equation6  = (acceleration*(time*time))/2
	print(f"disctance covered is equal to {equation6}m ")

def calculate_impulse(force, time):
	# Please pass the force and time as parameters
	# This function can be used to calculate the impulse applied on an object 
	equation7 = force*time
	print(f"Impulse is equal to {equation7}N ")






