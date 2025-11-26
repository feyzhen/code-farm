from __builtins__ import *


# ==================== 移动模块 ====================
def move_to_start():
    """移动到起点 (0,0)"""
    x, y = get_pos_x(), get_pos_y()
    for i in range(x):
        move(West)
    for j in range(y):
        move(South)


def snake_move(direction):
    """蛇形移动，返回新的方向"""
    if direction == North:
        move(North)
        if get_pos_y() == 0:  # 到达北边界
            move(East)
            return South
    else:  # South
        move(South)
        if get_pos_y() == get_world_size() - 1:  # 到达南边界
            move(East)
            return North
    return direction


# ==================== 种植模块 ====================
def get_plant_type():
    """根据位置决定种植什么"""
    x, y = get_pos_x(), get_pos_y()
    half = get_world_size() // 2

    if x < half and y < half:
        return Entities.Pumpkin
    elif x < half and y >= half:
        return Entities.Carrot
    elif x >= half and y < half:
        return Entities.Tree
    else:
        return Entities.Grass


def prepare_ground(plant_type):
    """准备合适的土地"""
    needs_soil = plant_type in [Entities.Pumpkin, Entities.Carrot, Entities.Sunflower]
    current_ground = get_ground_type()

    if needs_soil and current_ground == Grounds.Grassland:
        till()
    elif not needs_soil and current_ground == Grounds.Soil:
        till()


def plant_crop(plant_type):
    """种植作物"""
    prepare_ground(plant_type)
    plant(plant_type)


# ==================== 处理单个地块 ====================
def process_tile():
    """处理当前地块的所有操作"""
    # 浇水
    if get_water() < 0.5 and num_items(Items.Water) > 0:
        use_item(Items.Water)

    current_entity = get_entity_type()
    target_plant = get_plant_type()

    # 处理死南瓜
    if current_entity == Entities.Dead_Pumpkin:
        harvest()
        plant_crop(Entities.Pumpkin)
        return

    # 如果可以收获且不是目标植物（南瓜除外）
    if can_harvest():
        if current_entity != target_plant and current_entity != Entities.Pumpkin:
            harvest()
            plant_crop(target_plant)
    # 如果地块为空，种植目标植物
    elif current_entity is None:
        plant_crop(target_plant)


# ==================== 主程序 ====================
def main():
    """主循环"""
    move_to_start()
    direction = North

    while True:
        # 处理当前地块
        process_tile()

        # 蛇形移动
        direction = snake_move(direction)

        # 每完成一轮扫描打印一次
        if get_pos_x() == 0 and get_pos_y() == 0:
            quick_print("完成一轮扫描")


# 运行程序
main()