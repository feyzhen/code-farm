from __builtins__ import *



def move_back(direction):
	reDir = {
		South: North,
		North: South,
		East: West,
		West: East
	}
	move(reDir[direction])

def move2start():
	x, y = get_pos_x(), get_pos_y()
	for i in range(x):
		move(West)
	for j in range(y):
		move(South)

def move2end():
	size = get_world_size()
	x, y = get_pos_x(), get_pos_y()
	for i in range(size - 1 - x):
		move(East)
	for j in range(size - 1 - y):
		move(North)

def till_and_plant(plant_type):
	if plant_type in [Entities.Sunflower, Entities.Pumpkin, Entities.Carrot]:
		if get_ground_type() == Grounds.Grassland:
			till()
	else:
		if get_ground_type() == Grounds.Soil:
			till()
	plant(plant_type)

def get_plant_type():
	pos_x, pos_y = get_pos_x(), get_pos_y()
	half = get_world_size() // 2
	if pos_x < half and pos_y < half:
		return Entities.Pumpkin
	elif pos_x < half < pos_y:
		return Entities.Carrot
	elif pos_x > half > pos_y:
		return Entities.Tree
	elif pos_x > half and pos_y > half:
		return Entities.Grass
	else:
		return Entities.Sunflower

def main():
	no_dead_pumpkin = False
	# move2start()
	while True:
		dead_pumpkin_num = 0
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				# print(i, j)
				entity_type = get_entity_type()

				if get_water() <= 0.5:
					use_item(Items.Water)
				if can_harvest():
					if get_plant_type() == Entities.Pumpkin:
						if no_dead_pumpkin == True:
							harvest()
							till_and_plant(Entities.Pumpkin)
					else:
						harvest()
						till_and_plant(get_plant_type())

				else:
					if entity_type == Entities.Dead_Pumpkin:
						no_dead_pumpkin = False
						dead_pumpkin_num += 1
					till_and_plant(get_plant_type())
				move(North)
			move(East)
		if dead_pumpkin_num == 0:
			no_dead_pumpkin = True
		# break


main()

