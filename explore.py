import gym
import highway_env
from matplotlib import pyplot as plt
import numpy as np
'''
ACTIONS_ALL = {
        0: 'LANE_LEFT',
        1: 'IDLE',
        2: 'LANE_RIGHT',
        3: 'FASTER',
        4: 'SLOWER'
    }
'''

'''
                      l0 l1  l2 l3 l4 l5
                         ego f1 f2 f3 f4
                      r0 r1  r2 r3 r4 r5
'''

'''
                    l1 l2 l3 l4 l5  l6 l7 l8 l9
                                ego f6 f7 f8 f9
                    r1 r2 r3 r4 r5  r6 r7 r8 r9
'''

# abstractedEnv = {'l2':0, 'l3':0, 'l4':0, 'l5':0, 'l6':0, 'l7':0, 'l8':0,
                                                 # 'f6':0, 'f7':0, 'f8':0,
                 # 'r2':0, 'r3':0, 'r4':0, 'r5':0, 'r6':0, 'r7':0, 'r8':0,
                # }
LANE_LEFT  = 0
IDLE       = 1
LANE_RIGHT = 2
FASTER     = 3
SLOWER     = 4

absL = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
absF = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
absR = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}

# def decideAction(obs, allowedActions, speed):
    # #get occupancy grid
    # grid = obs[0,:,:]
    # speed_x = obs[3,:,:]
    # #basedon 3 lanes, determine which lanes ego is in
    # if LANE_LEFT in allowedActions and LANE_RIGHT in allowedActions:
        # currLane = 'middle'
    # elif LANE_LEFT in allowedActions:
        # currLane = 'right'
    # else:
        # currLane = 'left'
 
    # l1, l2, l3 = (grid[3][3] or grid[3][4]), (grid[3][5] or grid[3][6]), (grid[3][7] or grid[3][8])
    # f1, f2     =                             (grid[4][5] or grid[4][6]), (grid[4][7] or grid[4][8])
    # r1, r2, r3 = (grid[5][3] or grid[5][4]), (grid[5][5] or grid[5][6]), (grid[5][7] or grid[5][8])
    
    # action = 4
    # #check front
    # if f1:
        # action = 4
    # elif f2:
        # if (l1 or l2) and (r1 or r2):
            # action = 4 #slower
        # elif (l1 or l2):
            # action = 2 #right lane
        # elif (r1 or r2):
            # action = 0 # left lane
        # else:
            # if l3 and r3:
                # action = 0 #tie, go left
                # if action not in allowedActions:    
                    # action = 2
            # elif l3:
                # action = 2 #go right
            # elif r3:
                # action = 0 #go left
            # else:
                # action = 0 #tie, go left
                # if action not in allowedActions:
                    # action = 2
    # else:
        # if speed < 30:
            # action = 3 #faster
        
    # if action not in allowedActions:
        # action = 4
    
    # return action
                 
def abstractEnv(obs):
    #get occupancy gridPos
    gridPos = obs[0,:,:]
    gridVx = obs[3,:,:]

    for pos in absL:
        j = int(pos)-1
        if int(gridPos[3][j]):
            if gridVx[3][j] <=0:
                absL[pos] = 1 #Speedlow
            else:
                absL[pos] = 2 #Speedhigh
        else:
            absL[pos] = 0 #Free

    for pos in absF:
        j = int(pos)-1
        if int(gridPos[4][j]):
            if gridVx[4][j] <=0:
                absF[pos] = 1 #Speedlow
            else:
                absF[pos] = 2 #Speedhigh
        else:
            absF[pos] = 0 #Free
            
    for pos in absR:
        j = int(pos)-1
        if int(gridPos[5][j]):
            if gridVx[5][j] <=0:
                absR[pos] = 1 #Speedlow
            else:
                absR[pos] = 2 #Speedhigh
        else:
            absR[pos] = 0 #Free
    # print('****************************')
    # print(gridPos)
    # print(absF)
    # print('****************************')
    return absL,absF,absR
 
def writeAbsEnvToFile(collection):
    samples = []
    index = 1
    lc,lb,la,t,fa,fb,fc = '2','3','4','5','6','7','8'
    posList = [lc,lb,la,t,fa,fb,fc]
    #FOL_str.append('fhas(F{},Speedlow)'.format(num))

    
    for c in collection:
        FOL_str = []
        FOL_str.append('lcbehind(T{},Lc{})'.format(index,index))
        FOL_str.append('lbbehind(T{},Lb{})'.format(index,index))
        FOL_str.append('labehind(T{},La{})'.format(index,index))
        FOL_str.append('target(T{})'.format(index))
        FOL_str.append('fcfront(T{},Fc{})'.format(index,index))
        FOL_str.append('fbfront(T{},Fb{})'.format(index,index))
        FOL_str.append('fafront(T{},Fa{})'.format(index,index))
        
        dic = c[0]
        label = c[1]
        
        if dic[lc] == 0:
            FOL_str.append('lchas(Lc{},Free)'.format(index))
        elif dic[lc] == 1:
            FOL_str.append('lchas(Lc{},Speedlow)'.format(index))
        else:
            FOL_str.append('lchas(Lc{},Speedhigh)'.format(index))
            
        if dic[lb] == 0:
            FOL_str.append('lbhas(Lb{},Free)'.format(index))
        elif dic[lb] == 1:
            FOL_str.append('lbhas(Lb{},Speedlow)'.format(index))
        else:
            FOL_str.append('lbhas(Lb{},Speedhigh)'.format(index))
            
        if dic[la] == 0:
            FOL_str.append('lahas(La{},Free)'.format(index))
        elif dic[la] == 1:
            FOL_str.append('lahas(La{},Speedlow)'.format(index))
        else:
            FOL_str.append('lahas(La{},Speedhigh)'.format(index))

        if dic[t] == 0:
            FOL_str.append('thas(T{},Free)'.format(index))
        elif dic[t] == 1:
            FOL_str.append('thas(T{},Speedlow)'.format(index))
        else:
            FOL_str.append('thas(T{},Speedhigh)'.format(index))      
    #####
        if dic[fc] == 0:
            FOL_str.append('fchas(Fc{},Free)'.format(index))
        elif dic[fc] == 1:
            FOL_str.append('fchas(Fc{},Speedlow)'.format(index))
        else:
            FOL_str.append('fchas(Fc{},Speedhigh)'.format(index))
            
        if dic[fb] == 0:
            FOL_str.append('fbhas(Fb{},Free)'.format(index))
        elif dic[fb] == 1:
            FOL_str.append('fbhas(Fb{},Speedlow)'.format(index))
        else:
            FOL_str.append('fbhas(Fb{},Speedhigh)'.format(index))
            
        if dic[fa] == 0:
            FOL_str.append('fahas(Fa{},Free)'.format(index))
        elif dic[fa] == 1:
            FOL_str.append('fahas(Fa{},Speedlow)'.format(index))
        else:
            FOL_str.append('fahas(Fa{},Speedhigh)'.format(index))   
    
        if label:
            FOL_str.append('safe(T{})'.format(index))
        else:
            FOL_str.append('!safe(T{})'.format(index))
            
        samples.append(FOL_str)
        index += 1
        
    file = open('temp_data.txt','w')
    for sample in samples:
        for element in sample:
            file.write(element + '\n')
        file.write('\n\n\n')
    file.close()
    
    
env = gym.make("highway-v0")

env.config["observation"] = {
    "type": "OccupancyGrid",
    "vehicles_count": 15,
    "features": ["presence", "x", "y", "vx", "vy", "cos_h", "sin_h"],
    "features_range": {
        "x": [-100, 100],
        "y": [-35, 35],
        "vx": [-20, 20],
        "vy": [-20, 20]
    },
    "grid_size": [[-22.5, 22.5], [-22.5, 22.5]],
    "grid_step": [5, 5],
    "absolute": False
}


env.config["simulation_frequency"] = 20
env.config["policy_frequency"] = 1
env.config["duration"] = 100 # default is 40, calculated based on steps (policy decision)
env.config["vehicles_density"] = 1.2
env.config["lanes_count"] = 3
env.config["other_vehicles_type"] = "highway_env.vehicle.behavior.IDMVehicle" #IDMVehicle #AggressiveVehicle #DefensiveVehicle


# demo = []

# done = False
# obs = env.reset()
# reward = 0
# while not done:
    # allowedActions = env.get_available_actions()
    # action, gridPos, reduced_gridPos = decideAction(obs, allowedActions)
    # pair = {}
    # pair[action] = reduced_gridPos
    # print('check below ......')
    # print(reduced_gridPos)
    # print(pair)
    # a = input('a:')
    # demo.append(pair)
    # obs, reward, done, info = env.step(action)
    # reward += reward
    # env.render()
# print('Total Reward: {}'.format(reward))




# env.configure({
    # "manual_control": True
# })
#absF = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
def considerLaneChange(absF,speed):

    if (absF['6'] != 0) or (absF['7'] == 1): # if speedlow
        action = SLOWER
    elif absF['8'] == 1 or (absF['7'] == 2):
        action = IDLE
    else:
        action = FASTER
    
    print(absF)
    print(action)
    
    if (action == IDLE):
        print('Consider lane change\n')
        return True, None
        
    return False,action

samples = []
count = 0
while True:
    toggleLR = True
    obs = env.reset()
    speed = 15
    done = False
    collection = []
    while not done:
        stateActionResult = []
        absL,absF,absR = abstractEnv(obs)
        #action = env.action_space.sample()
        laneChange, action = considerLaneChange(absF,speed)
        allowedActions = env.get_available_actions()
        if laneChange:
            count += 1
            if toggleLR:
                if LANE_LEFT in allowedActions:
                    action = LANE_LEFT
                else:
                    action = LANE_RIGHT
            else:
                if LANE_RIGHT in allowedActions:
                    action = LANE_RIGHT
                else:
                    action = LANE_LEFT
            toggleLR = not toggleLR

        #action = decideAction(obs, allowedActions, speed)
        obs, reward, done, info = env.step(action)  # with manual control, these actions are ignored
        speed = info['speed']
        #print('Speed = {}'.format(speed))
        
        if info['action'] == LANE_LEFT:
        
            stateActionResult.append(absL)
            
            if info['crashed']:
                stateActionResult.append(False)#not safe
            else:
                stateActionResult.append(True)
            collection.append(stateActionResult)
                
        elif info['action'] == LANE_RIGHT:
        
            stateActionResult.append(absR)
            
            if info['crashed']:
                stateActionResult.append(False)#not safe
            else:
                stateActionResult.append(True)
            
            collection.append(stateActionResult)
        
        #print(info)
        print(stateActionResult)
        # if laneChange:
            # input('a:')
        # if info['crashed']:
            # input('a:')
        #input('a:')
        env.render()
    
    
    samples += collection
    
    for c in collection:
        print(c)
    print('\n\n')

    if count >= 30:
        break
    
writeAbsEnvToFile(samples)
    