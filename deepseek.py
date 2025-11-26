from __builtins__ import *

# 全局变量记录死南瓜状态
has_dead_pumpkin = False


def move_to_start():
    """移动到起点 (0,0)"""
    x, y = get_pos_x(), get_pos_y()
    for i in range(x):
        move(West)
    for j in range(y):
        move(South)


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
    needs_soil = plant_type in [Entities.Pumpkin, Entities.Carrot]
    current_ground = get_ground_type()

    if needs_soil and current_ground == Grounds.Grassland:
        till()
    elif not needs_soil and current_ground == Grounds.Soil:
        till()


def process_tile():
    """处理当前地块"""
    global has_dead_pumpkin

    # 浇水
    if get_water() < 0.5 and num_items(Items.Water) > 0:
        use_item(Items.Water)

    current_entity = get_entity_type()
    target_plant = get_plant_type()

    # 记录死南瓜
    if current_entity == Entities.Dead_Pumpkin:
        has_dead_pumpkin = True

    # 处理死南瓜（立即清除）
    if current_entity == Entities.Dead_Pumpkin:
        harvest()
        prepare_ground(Entities.Pumpkin)
        plant(Entities.Pumpkin)
        return

    # 南瓜收获逻辑：只有在没有死南瓜的情况下才收获
    if current_entity == Entities.Pumpkin and can_harvest():
        if not has_dead_pumpkin:  # 本轮扫描没有发现死南瓜
            harvest()
            prepare_ground(target_plant)
            plant(target_plant)
        return

    # 其他植物的收获逻辑
    if can_harvest() and current_entity != target_plant:
        harvest()
        prepare_ground(target_plant)
        plant(target_plant)
    elif current_entity is None:
        prepare_ground(target_plant)
        plant(target_plant)


# 主循环
def main():
    global has_dead_pumpkin

    move_to_start()
    direction = North
    scan_count = 0

    while True:
        # 每轮扫描开始时重置死南瓜状态
        if get_pos_x() == 0 and get_pos_y() == 0:
            has_dead_pumpkin = False
            scan_count += 1
            quick_print(f"开始第{scan_count}轮扫描")

        # 处理当前地块
        process_tile()

        # 蛇形移动
        if direction == North:
            move(North)
            if get_pos_y() == 0:
                move(East)
                direction = South
        else:
            move(South)
            if get_pos_y() == get_world_size() - 1:
                move(East)
                direction = North


# 运行程序
main()