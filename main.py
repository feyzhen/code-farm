from __builtins__ import *

def back(direction):
	dir = {
		South: North,
		North: South,
		East: West,
		West: East
	}
	move(dir[direction])

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
	h_dir = East
	v_dir = North
	while True:
		if get_pos_x() == 0 and get_pos_y() == 0:
			no_dead_pumpkin = True

		move2start()
		if no_dead_pumpkin:
			harvest()
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				if get_water() <= 0.5:
					use_item(Items.Water)
				if get_entity_type() == Entities.Dead_Pumpkin:
					till_and_plant(Entities.Pumpkin)
					no_dead_pumpkin = False
				if can_harvest():
					if get_entity_type() != get_plant_type() or get_entity_type() != Entities.Pumpkin:
						harvest()
						till_and_plant(get_plant_type())
				else:
					if get_entity_type() is None:
						till_and_plant(get_plant_type())
				move(North)
			move(East)
		no_dead_pumpkin = True


main()

