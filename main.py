def move2start():
	x, y = get_pos_x(), get_pos_y()
	for i in range(x):
		move(West)
	for j in range(y):
		move(South)
		
def till_and_plant(type):
	if type in [Entities.Sunflower, Entities.Pumpkin, Entities.Carrot]:
		if get_ground_type() == Grounds.Grassland:
			till()
	else:  
	
		if get_ground_type() == Grounds.Soil:
			till()
	plant(type)

def get_plant_type():
	pos_x, pos_y = get_pos_x(), get_pos_y()
	half = get_world_size() // 2
	if pos_x < half and pos_y < half:
		return Entities.Pumpkin
	elif pos_x < half and pos_y > half:
		return Entities.Carrot
	elif pos_x > half and pos_y < half:
		return Entities.Tree
	elif pos_x > half and pos_y > half:
		return Entities.Grass
	else:
		return Entities.Sunflower
	print('错误')
	
harvest_pumkin = False
while True:
	move2start()
	if harvest_pumkin:
		harvest()
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			if get_water() <= 0.5: 
				use_item(Items.Water)
			if get_entity_type() == Entities.Dead_Pumpkin:
				till_and_plant(Entities.Pumpkin)
				harvest_pumkin = False
			if can_harvest():
				if get_entity_type() != get_plant_type() or get_entity_type() != Entities.Pumpkin:
					harvest()
					till_and_plant(get_plant_type())
			else:
				if get_entity_type() == None:
					till_and_plant(get_plant_type())
			move(North)
		move(East)
	harvest_pumkin = True

