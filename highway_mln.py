import gym
import highway_env
from matplotlib import pyplot as plt
import numpy as np

import os
import time
from pracmln import MLN, Database
from pracmln import query


'''
ACTIONS_ALL = {
        0: 'LANE_LEFT',
        1: 'IDLE',
        2: 'LANE_RIGHT',
        3: 'FASTER',
        4: 'SLOWER'
    }
'''

LANE_LEFT  = 0
IDLE       = 1
LANE_RIGHT = 2
FASTER     = 3
SLOWER     = 4

absL = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
absF = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
absR = {'2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0}
               
def abstractEnv(obs):
    #get occupancy gridPos
    gridPos = obs[0,:,:]
    gridVx = obs[3,:,:]

    speedThreshold = 0.05
    for pos in absL:
        j = int(pos)-1
        if int(gridPos[3][j]):
            if abs(gridVx[3][j]) <=speedThreshold:
                absL[pos] = 3 #Speedsame
            elif gridVx[3][j] < -speedThreshold:
                absL[pos] = 1 #Speedlow
            else:
                absL[pos] = 2 #Speedhigh
        else:
            absL[pos] = 0 #Free

    for pos in absF:
        j = int(pos)-1
        if int(gridPos[4][j]):
            if abs(gridVx[4][j]) <=speedThreshold:
                absF[pos] = 3 #Speedsame
            elif gridVx[4][j] < -speedThreshold:
                absF[pos] = 1 #Speedlow
            else:
                absF[pos] = 2 #Speedhigh
        else:
            absF[pos] = 0 #Free
            
    for pos in absR:
        j = int(pos)-1
        if int(gridPos[5][j]):
            if abs(gridVx[5][j]) <=speedThreshold:
                absR[pos] = 3 #Speedsame
            elif gridVx[5][j] < -speedThreshold:
                absR[pos] = 1 #Speedlow
            else:
                absR[pos] = 2 #Speedhigh
        else:
            absR[pos] = 0 #Free
            
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
        elif dic[lc] == 3:
            FOL_str.append('lchas(Lc{},Speedsame)'.format(index))
        else:
            FOL_str.append('lchas(Lc{},Speedhigh)'.format(index))
            
        if dic[lb] == 0:
            FOL_str.append('lbhas(Lb{},Free)'.format(index))
        elif dic[lb] == 1:
            FOL_str.append('lbhas(Lb{},Speedlow)'.format(index))
        elif dic[lb] == 3:
            FOL_str.append('lbhas(Lb{},Speedsame)'.format(index))
        else:
            FOL_str.append('lbhas(Lb{},Speedhigh)'.format(index))
            
        if dic[la] == 0:
            FOL_str.append('lahas(La{},Free)'.format(index))
        elif dic[la] == 1:
            FOL_str.append('lahas(La{},Speedlow)'.format(index))
        elif dic[la] == 3:
            FOL_str.append('lahas(La{},Speedsame)'.format(index))
        else:
            FOL_str.append('lahas(La{},Speedhigh)'.format(index))

        if dic[t] == 0:
            FOL_str.append('thas(T{},Free)'.format(index))
        elif dic[t] == 1:
            FOL_str.append('thas(T{},Speedlow)'.format(index))
        elif dic[t] == 3:
            FOL_str.append('thas(T{},Speedsame)'.format(index))
        else:
            FOL_str.append('thas(T{},Speedhigh)'.format(index))      
    #####
        if dic[fc] == 0:
            FOL_str.append('fchas(Fc{},Free)'.format(index))
        elif dic[fc] == 1:
            FOL_str.append('fchas(Fc{},Speedlow)'.format(index))
        elif dic[fc] == 3:
            FOL_str.append('fchas(Fc{},Speedsame)'.format(index))
        else:
            FOL_str.append('fchas(Fc{},Speedhigh)'.format(index))
            
        if dic[fb] == 0:
            FOL_str.append('fbhas(Fb{},Free)'.format(index))
        elif dic[fb] == 1:
            FOL_str.append('fbhas(Fb{},Speedlow)'.format(index))
        elif dic[fb] == 3:
            FOL_str.append('fbhas(Fb{},Speedsame)'.format(index))
        else:
            FOL_str.append('fbhas(Fb{},Speedhigh)'.format(index))
            
        if dic[fa] == 0:
            FOL_str.append('fahas(Fa{},Free)'.format(index))
        elif dic[fa] == 1:
            FOL_str.append('fahas(Fa{},Speedlow)'.format(index))
        elif dic[fa] == 3:
            FOL_str.append('fahas(Fa{},Speedsame)'.format(index))
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
    
def makeEnv():    
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
    env.config["vehicles_density"] = 1
    env.config["lanes_count"] = 3
    env.config["other_vehicles_type"] = "highway_env.vehicle.behavior.IDMVehicle" #IDMVehicle #AggressiveVehicle #DefensiveVehicle
    
    return env



def considerLaneChange(absF,speed):

    if (absF['6'] != 0) or (absF['7'] == 1) or (absF['7'] == 3): # if speedlow
        action = SLOWER
    elif absF['8'] == 1 or (absF['7'] == 2):
        action = IDLE
    else:
        action = FASTER

    if (action == IDLE):
        print('Consider lane change\n')
        return True, None
        
    return False,action
    

def inference_obs(mln,obs_str_list):
    db = Database(mln)
    for e in obs_str_list:
        db << e
    #db.write()
    print('=== INFERENCE TEST:', 'EnumerationAsk', '===')
    result = query(queries='safe(T1)',
                  method='EnumerationAsk',
                  mln=mln,
                  db=db,
                  verbose=False,
                  multicore=False).run()
    return result.results
    
def load_mln():
    p = os.path.join('./drive', 'highway.pracmln')
    mln = MLN(mlnfile=('%s:test_3_trained.mln' % p),
              grammar='StandardGrammar',logic='FirstOrderLogic')
              
    return mln



def infer_lane_safe(mln,laneAbs):
    lc,lb,la,t,fa,fb,fc = '2','3','4','5','6','7','8'
    index = 1
    FOL_str = []
    FOL_str.append('lcbehind(T{},Lc{})'.format(index,index))
    FOL_str.append('lbbehind(T{},Lb{})'.format(index,index))
    FOL_str.append('labehind(T{},La{})'.format(index,index))
    FOL_str.append('target(T{})'.format(index))
    FOL_str.append('fcfront(T{},Fc{})'.format(index,index))
    FOL_str.append('fbfront(T{},Fb{})'.format(index,index))
    FOL_str.append('fafront(T{},Fa{})'.format(index,index))
    
    dic = laneAbs
    
    if dic[lc] == 0:
        FOL_str.append('lchas(Lc{},Free)'.format(index))
    elif dic[lc] == 1:
        FOL_str.append('lchas(Lc{},Speedlow)'.format(index))
    elif dic[lc] == 3:
        FOL_str.append('lchas(Lc{},Speedsame)'.format(index))
    else:
        FOL_str.append('lchas(Lc{},Speedhigh)'.format(index))
        
    if dic[lb] == 0:
        FOL_str.append('lbhas(Lb{},Free)'.format(index))
    elif dic[lb] == 1:
        FOL_str.append('lbhas(Lb{},Speedlow)'.format(index))
    elif dic[lb] == 3:
        FOL_str.append('lbhas(Lb{},Speedsame)'.format(index))
    else:
        FOL_str.append('lbhas(Lb{},Speedhigh)'.format(index))
        
    if dic[la] == 0:
        FOL_str.append('lahas(La{},Free)'.format(index))
    elif dic[la] == 1:
        FOL_str.append('lahas(La{},Speedlow)'.format(index))
    elif dic[la] == 3:
        FOL_str.append('lahas(La{},Speedsame)'.format(index))
    else:
        FOL_str.append('lahas(La{},Speedhigh)'.format(index))

    if dic[t] == 0:
        FOL_str.append('thas(T{},Free)'.format(index))
    elif dic[t] == 1:
        FOL_str.append('thas(T{},Speedlow)'.format(index))
    elif dic[t] == 3:
        FOL_str.append('thas(T{},Speedsame)'.format(index))
    else:
        FOL_str.append('thas(T{},Speedhigh)'.format(index))      
#####
    if dic[fc] == 0:
        FOL_str.append('fchas(Fc{},Free)'.format(index))
    elif dic[fc] == 1:
        FOL_str.append('fchas(Fc{},Speedlow)'.format(index))
    elif dic[fc] == 3:
        FOL_str.append('fchas(Fc{},Speedsame)'.format(index))
    else:
        FOL_str.append('fchas(Fc{},Speedhigh)'.format(index))
        
    if dic[fb] == 0:
        FOL_str.append('fbhas(Fb{},Free)'.format(index))
    elif dic[fb] == 1:
        FOL_str.append('fbhas(Fb{},Speedlow)'.format(index))
    elif dic[fb] == 3:
        FOL_str.append('fbhas(Fb{},Speedsame)'.format(index))
    else:
        FOL_str.append('fbhas(Fb{},Speedhigh)'.format(index))
        
    if dic[fa] == 0:
        FOL_str.append('fahas(Fa{},Free)'.format(index))
    elif dic[fa] == 1:
        FOL_str.append('fahas(Fa{},Speedlow)'.format(index))
    elif dic[fa] == 3:
        FOL_str.append('fahas(Fa{},Speedsame)'.format(index))
    else:
        FOL_str.append('fahas(Fa{},Speedhigh)'.format(index))
        
    result = inference_obs(mln,FOL_str)
    
    return result['safe(T1)']


env = makeEnv()
mln = load_mln()
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
        
            leftSafeP = infer_lane_safe(mln,absL)
            rightSafeP = infer_lane_safe(mln,absR)
            print('leftSafeP = {}'.format(leftSafeP))
            print('rightSafeP = {}'.format(rightSafeP))
            
            if LANE_LEFT not in allowedActions:
                leftSafeP = 0
            if LANE_RIGHT not in allowedActions:
                rightSafeP = 0          
                
            action = SLOWER
            if leftSafeP >0.7:
                if leftSafeP >= rightSafeP:
                    action = LANE_LEFT
                    print('action = LANE_LEFT')
                    
            if rightSafeP >0.7:
                if leftSafeP <= rightSafeP:
                    action = LANE_RIGHT
                    print('action = LANE_RIGHT')
            
            print('absL = {}'.format(absL))
            print('absR = {}'.format(absR))
            #input('a:')
        
        #action = decideAction(obs, allowedActions, speed)
        obs, reward, done, info = env.step(action)  # with manual control, these actions are ignored
        
        env.render()
