from enum import IntEnum

class set(IntEnum):
    unused = -1                     # combo wont show in game
    Eoc1 = 1
    Itf1 = 4
    Itf2 = 5
    Itf3 = 6
    Ur2700 = 10001                  # user rank unlocks
    Ur1450  = 10002
    Ur2150 = 10003

class effect(IntEnum):
    unit_attack = 0
    unit_health = 1
    unit_speed = 2
    cannon_starting_recharge = 3
    worker_starting_level = 4
    starting_money = 5
    cannon_attack = 6
    cannon_recharge_time = 7
    worker_efficiency_unused = 8
    wallet_size = 9
    base_health = 10
    research = 11
    accounting = 12
    xp = 13
    strong_against = 14
    massive_damage = 15
    resistant = 16
    knockback_distance = 17
    slow_time = 18
    freeze_time = 19
    weaken_time = 20
    berserk = 21
    unknown_1 = 22
    unknown_2 = 23
    critical_chance = 24
    unknown_3 = 25
    unknown_4 =  26
    unknown_5 = 27

class mult(IntEnum):
    sm = 0
    m = 1
    l = 2
    xl = 3
    down = 4
