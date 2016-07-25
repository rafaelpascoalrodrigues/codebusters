import sys
import math
import random


def distanceFrom1D(position, distance):
    if (position > distance):
        return (position - distance)
    elif (position < distance):
        return (distance - position)
    return 0


def distanceFrom2D(position1, distance1, position2, distance2):
    return (distanceFrom1D(position1, distance1) + distanceFrom1D(position2, distance2))

# Turns trying to pursue an invisible ghost
pursue = 3

# Base position
safe_distance_to_release = 1600
safe_distance_to_release = int((safe_distance_to_release // 2) * 0.9)
base = [
    {'pos_x' :     0, 'pos_y' :    0},
    {'pos_x' : 16000, 'pos_y' : 9000}
]

buster_template = {
    'id'          : -1,
    'visible'     : False,
    'type'        : 'BUSTER',
    'action'      : 'IDLE',
    'state'       : 'EMPTY',
    'pursue'      : -1,
    'stun'        : -1,
    'strategy_id' : -1, 
    'strategy'    : -1,
    'step'        : -1,
    'pos_x'       : -1,
    'pos_y'       : -1,
    'bond'        : -1,
    'move_x'      : -1,
    'move_y'      : -1
}

entity_template = {
    'id'      : -1,
    'visible' : False,
    'type'    : 'GHOST',
    'action'  : 'HAUNTING',
    'pos_x'   : -1,
    'pos_y'   : -1,
    'bond'    : -1,
    'move_x'  : -1,
    'move_y'  : -1
}


strategies = [
    [
        [15000, 1125],
        [ 1000, 1125]
    ], [
        [15000, 3375],
        [ 1000, 3375]
    ], [
        [15000, 5625],
        [ 1000, 5625]
    ], [
        [15000, 7875],
        [ 1000, 7875]
    ]
]


busters_per_player = int(input())
ghost_count        = int(input())
my_team_id         = int(input())
ad_team_id         = 1 if (my_team_id == 0) else 0
my_team_base       = [
    distanceFrom1D(base[my_team_id]['pos_x'], safe_distance_to_release),
    distanceFrom1D(base[my_team_id]['pos_y'], safe_distance_to_release)
] 
busters            = [buster_template.copy() for i in range(busters_per_player * 2)]
adversaries        = [buster_template.copy() for i in range(busters_per_player * 2)]
ghosts             = [entity_template.copy() for i in range(ghost_count)]

# game loop
while True:
    # Gathering map situation
    for i in range(ghost_count):
        ghosts[i]['visible'] = False

    for i in range(busters_per_player * 2):
        adversaries[i]['visible'] = False


    entities_visible = int(input())
    for i in range(entities_visible):
        entity_data   = input().split()
        entity_id     = int(entity_data[0])
        entity_x      = int(entity_data[1])
        entity_y      = int(entity_data[2])
        entity_type   = int(entity_data[3])
        entity_state  = int(entity_data[4])
        entity_value  = int(entity_data[5])

        if (entity_type == -1):
            # Ghost found
            ghosts[entity_id]['visible'] = True
            ghosts[entity_id]['id']      = entity_id
            ghosts[entity_id]['pos_x']   = entity_x
            ghosts[entity_id]['pos_y']   = entity_y
            if (ghosts[entity_id]['bond'] != -1 and busters[ghosts[entity_id]['bond']]['bond'] != entity_id):
                ghosts[entity_id]['bond'] = -1
            
 
        elif (entity_type == my_team_id):
            # Buster found
            if (busters[entity_id]['action'] == 'IDLE'):
                busters[entity_id]['action'] = 'EXPLORING'
            if (busters[entity_id]['action'] == 'DISTURB'):
                busters[entity_id]['action'] = 'EXPLORING'
            if (busters[entity_id]['action'] == 'STUN'):
                busters[entity_id]['action'] = 'EXPLORING' 
            busters[entity_id]['visible']  = True
            busters[entity_id]['id']       = entity_id
            busters[entity_id]['pos_x']    = entity_x
            busters[entity_id]['pos_y']    = entity_y
            busters[entity_id]['stun']    -= 1
            busters[entity_id]['state']    = 'EMPTY' if (entity_state == 0) else 'FULL'
            if (busters[entity_id]['strategy'] == -1):
                if ((entity_id % busters_per_player) == 0):
                    busters[entity_id]['strategy_id'] = 0
                elif ((entity_id % busters_per_player) == 1):
                    busters[entity_id]['strategy_id'] = 2
                elif ((entity_id % busters_per_player) == 2):
                    busters[entity_id]['strategy_id'] = 1
                else:
                    busters[entity_id]['strategy_id'] = 3
                busters[entity_id]['strategy']    = strategies[busters[entity_id]['strategy_id']]
                busters[entity_id]['step']        = 0
                
            if (entity_state == 2):
                busters[entity_id]['action'] = 'STUNNED'
                busters[entity_id]['state'] = 'EMPTY'
                if (busters[entity_id]['bond'] != -1):
                    ghosts[busters[entity_id]['bond']]['bond'] = -1
                    busters[entity_id]['bond']                 = -1
                
            elif (busters[entity_id]['action'] == 'STUNNED'):
                busters[entity_id]['action'] = 'EXPLORING'
                
                
        else:
            # Adversary Buster Found
            adversaries[entity_id]['visible'] = True
            adversaries[entity_id]['id']      = entity_id
            adversaries[entity_id]['pos_x']   = entity_x
            adversaries[entity_id]['pos_y']   = entity_y
            if (entity_state == 2):
                adversaries[entity_id]['action'] = 'STUNNED'
            else:
                adversaries[entity_id]['action'] = 'DISTURGING'


    for i in range(busters_per_player):
        i += (ad_team_id * busters_per_player)
        if (not adversaries[i]['visible'] or adversaries[i]['action'] == 'STUNNED'):
            continue

        deploy = {'id' : -1, 'distance' : (16001 + 9001)}
        for j in range(busters_per_player):
            j += (my_team_id * busters_per_player)
            if (busters[j]['action'] != 'EXPLORING'):
                # That Buster is busy
                continue;

            distance = abs(abs(busters[j]['pos_x']) - abs(adversaries[i]['pos_x'])) + abs(abs(busters[j]['pos_y']) - abs(adversaries[i]['pos_y']))
            if (distance < deploy['distance']):
                deploy['id']       = busters[j]['id']
                deploy['distance'] = distance

        if (deploy['id'] != -1):
            adversaries[i]['bond']          = deploy['id']
            busters[deploy['id']]['action'] = 'DISTURB'
            busters[deploy['id']]['bond']   = adversaries[i]['id']


    for i in range(ghost_count):
        if (not ghosts[i]['visible'] or ghosts[i]['bond'] != -1):
            continue

        deploy = {'id' : -1, 'distance' : (16001 + 9001)}
        for j in range(busters_per_player):
            j += (my_team_id * busters_per_player)
            if (busters[j]['action'] != 'EXPLORING'):
                # That Buster is busy
                continue;
            
            distance = distanceFrom2D(busters[j]['pos_x'], ghosts[i]['pos_x'], busters[j]['pos_y'], ghosts[i]['pos_y'])
            if (distance < deploy['distance']):
                deploy['id']       = busters[j]['id']
                deploy['distance'] = distance

        if (deploy['id'] != -1):
            ghosts[i]['bond']               = deploy['id']
            busters[deploy['id']]['action'] = 'PURSUIT'
            busters[deploy['id']]['bond']   = ghosts[i]['id']
            busters[deploy['id']]['pursue'] = pursue


    for j in range(busters_per_player):
        j += (my_team_id * busters_per_player)
        if (busters[j]['action'] == 'IDLE'):
            continue

        if (busters[j]['action'] == 'IDLE'):
            pass

        elif (busters[j]['action'] == 'DISTURB'):
            if (busters[j]['bond'] == -1):
                busters[j]['action'] = 'EXPLORING'

            distance = distanceFrom2D(busters[j]['pos_x'], adversaries[busters[j]['bond']]['pos_x'], busters[j]['pos_y'], adversaries[busters[j]['bond']]['pos_y'])
            if (adversaries[busters[j]['bond']]['visible']):
                if (adversaries[busters[j]['bond']]['action'] == 'STUNNED'):
                    busters[j]['action'] = 'EXPLORING'
                elif (distance <= 1760 and busters[j]['stun'] < 0):
                    busters[j]['action'] = 'STUN'
                    busters[j]['stun']   = 20
                else:
                    busters[j]['action'] = 'EXPLORING'
            else:
                if (busters[j]['pursue'] < 0):
                    adversaries[busters[j]['bond']]['bond'] = -1
                    busters[j]['bond']                      = -1
                    busters[j]['action']                    = 'EXPLORING'



        elif (busters[j]['action'] == 'RETURN'):
            distance = distanceFrom2D(busters[j]['pos_x'], my_team_base[0], busters[j]['pos_y'], my_team_base[1])
            if (distance == 0):
                busters[j]['action'] = 'RELEASE'


        elif (busters[j]['action'] == 'BUST'):
            if (busters[j]['state'] == 'FULL'):
                busters[j]['action'] = 'RETURN'
            else:
                if (ghosts[busters[j]['bond']]['bond'] != -1):
                    ghosts[busters[j]['bond']]['bond'] = -1
                    busters[j]['bond']                 = -1
                busters[j]['action'] = 'EXPLORING'


        elif (busters[j]['action'] == 'PURSUIT'):
            if (busters[j]['bond'] == -1):
                busters[j]['action'] = 'EXPLORING'

            distance = distanceFrom2D(busters[j]['pos_x'], ghosts[busters[j]['bond']]['pos_x'], busters[j]['pos_y'], ghosts[busters[j]['bond']]['pos_y'])
            if (ghosts[busters[j]['bond']]['visible']):
                busters[j]['pursue'] = pursue
                if (distance <= 1760):
                    busters[j]['action'] = 'BUST'
            else:
                busters[j]['pursue'] -= 1
                if (busters[j]['pursue'] < 0):
                    ghosts[busters[j]['bond']]['bond'] = -1
                    busters[j]['bond']                 = -1
                    busters[j]['action']               = 'EXPLORING'


        else:
            busters[j]['action'] = 'EXPLORING'

        if (busters[j]['action'] == 'EXPLORING'):
            pos_x  = busters[j]['pos_x']
            pos_y  = busters[j]['pos_y']
            move_x = busters[j]['strategy'][busters[j]['step']][0]
            move_y = busters[j]['strategy'][busters[j]['step']][1]

            if (distanceFrom2D(pos_x, move_x, pos_y, move_y) < 400):
                busters[j]['step'] += 1
                if (busters[j]['step'] >= len(busters[j]['strategy'])):
                    busters[j]['step']         = 0
                    busters[j]['strategy_id'] += 1
                    if (busters[j]['strategy_id'] >= len(strategies)):
                        busters[j]['strategy_id'] = 0
                    busters[j]['strategy'] = strategies[busters[j]['strategy_id']]

        # Take the actions
        if (busters[j]['action'] == 'EXPLORING'):
            move_x = busters[j]['strategy'][busters[j]['step']][0]
            move_y = busters[j]['strategy'][busters[j]['step']][1]
            print("MOVE", move_x, move_y, busters[j]['action'])
        elif (busters[j]['action'] == 'PURSUIT'):
            move_x = ghosts[busters[j]['bond']]['pos_x']
            move_y = ghosts[busters[j]['bond']]['pos_y']
            print("MOVE", move_x, move_y, busters[j]['action'])
        elif (busters[j]['action'] == 'BUST'):
            bond = busters[j]['bond']
            print("BUST", bond, busters[j]['action'])
        elif (busters[j]['action'] == 'RETURN'):
            move_x = my_team_base[0]
            move_y = my_team_base[1]
            print("MOVE", move_x, move_y, busters[j]['action'])
        elif (busters[j]['action'] == 'RELEASE'):
            bond = busters[j]['bond']
            print("RELEASE", bond, busters[j]['action'])
        elif (busters[j]['action'] == 'STUN'):
            bond = busters[j]['bond']
            print("STUN", bond, busters[j]['action'])
        else:
            # Something goes wrong!
            print("MOVE", random.randrange(0, 16000), random.randrange(0, 9000), "Something goes wrong!")
