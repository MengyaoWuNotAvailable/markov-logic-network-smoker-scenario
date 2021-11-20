'''
la  lb  lc
    e   fa fb
ra  rb  rc
'''
import random

numSample = 30
samples = []
goL = 0
goR = 0
goF = 0
for num in range(1,numSample+1):

    blocks = {'la':0,'lb':0,'lc':0,'ra':0,'rb':0,'rc':0,'fa':0,'fb':0}

    for block in blocks:
        rand = random.randint(0,2)
        blocks[block] = rand


    FOL_str = ['lefta(Ego{},La{})'.format(num,num),
               'leftb(Ego{},Lb{})'.format(num,num),
               'leftc(Ego{},Lc{})'.format(num,num),
               'frontlb(Lb{},Lc{})'.format(num,num),
               'behindlb(Lb{},La{})'.format(num,num),
               
               'righta(Ego{},Ra{})'.format(num,num),
               'rightb(Ego{},Rb{})'.format(num,num),
               'rightc(Ego{},Rc{})'.format(num,num),
               'frontrb(Rb{},Rc{})'.format(num,num),
               'behindrb(Rb{},Ra{})'.format(num,num),
               
               'fronta(Ego{},Fa{})'.format(num,num),
               'frontb(Ego{},Fb{})'.format(num,num),
               'frontfa(Fa{},Fb{})'.format(num,num)
               ]


    if blocks['la'] == 0:
        FOL_str.append('lahas(La{},Free)'.format(num))
    elif blocks['la'] == 1:
        FOL_str.append('lahas(La{},Speedlow)'.format(num))
    else:
        FOL_str.append('lahas(La{},Speedhigh)'.format(num))
        

    if blocks['lb'] == 0:
        FOL_str.append('lbhas(Lb{},Free)'.format(num))
    elif blocks['lb'] == 1:
        FOL_str.append('lbhas(Lb{},Speedlow)'.format(num))
    else:
        FOL_str.append('lbhas(Lb{},Speedhigh)'.format(num))


    if blocks['lc'] == 0:
        FOL_str.append('lchas(Lc{},Free)'.format(num))
    elif blocks['lc'] == 1:
        FOL_str.append('lchas(Lc{},Speedlow)'.format(num))
    else:
        FOL_str.append('lchas(Lc{},Speedhigh)'.format(num))
        
    if blocks['ra'] == 0:
        FOL_str.append('rahas(Ra{},Free)'.format(num))
    elif blocks['ra'] == 1:
        FOL_str.append('rahas(Ra{},Speedlow)'.format(num))
    else:
        FOL_str.append('rahas(Ra{},Speedhigh)'.format(num))
        
        
    if blocks['rb'] == 0:
        FOL_str.append('rbhas(Rb{},Free)'.format(num))
    elif blocks['rb'] == 1:
        FOL_str.append('rbhas(Rb{},Speedlow)'.format(num))
    else:
        FOL_str.append('rbhas(Rb{},Speedhigh)'.format(num))
        
    if blocks['rc'] == 0:
        FOL_str.append('rchas(Rc{},Free)'.format(num))
    elif blocks['rc'] == 1:
        FOL_str.append('rchas(Rc{},Speedlow)'.format(num))
    else:
        FOL_str.append('rchas(Rc{},Speedhigh)'.format(num))
        
        
    if blocks['fa'] == 0:
        FOL_str.append('fahas(Fa{},Free)'.format(num))
    elif blocks['fa'] == 1:
        FOL_str.append('fahas(Fa{},Speedlow)'.format(num))
    else:
        FOL_str.append('fahas(Fa{},Speedhigh)'.format(num))
        
        
    if blocks['fb'] == 0:
        FOL_str.append('fbhas(Fb{},Free)'.format(num))
    elif blocks['fb'] == 1:
        FOL_str.append('fbhas(Fb{},Speedlow)'.format(num))
    else:
        FOL_str.append('fbhas(Fb{},Speedhigh)'.format(num))
        



    safeL = False
    safeR = False
    safeF = False

    if (blocks['lb'] ==0 and blocks['la'] <= 1 and blocks['lc'] !=1):
        safeL = True
        
    if (blocks['rb'] ==0 and blocks['ra'] <= 1 and blocks['rc'] !=1):
        safeR = True
        
    if (blocks['fa'] ==0 and blocks['fb'] != 1):
        safeF = True
        

    if safeF:
        FOL_str.append('betterfa(Fa{})'.format(num))
        FOL_str.append('!betterlb(Lb{})'.format(num))
        FOL_str.append('!betterrb(Rb{})'.format(num))
        goF += 1
    elif safeL:
        FOL_str.append('betterlb(Lb{})'.format(num))
        FOL_str.append('!betterfa(Fa{})'.format(num))
        FOL_str.append('!betterrb(Rb{})'.format(num))
        goL += 1
    elif safeR:
        FOL_str.append('betterrb(Rb{})'.format(num))
        FOL_str.append('!betterfa(Fa{})'.format(num))
        FOL_str.append('!betterlb(Lb{})'.format(num))
        goR += 1
    else:
        FOL_str.append('betterfa(Fa{})'.format(num))
        FOL_str.append('!betterlb(Lb{})'.format(num))
        FOL_str.append('!betterrb(Rb{})'.format(num))
        goF += 1
    
    samples.append(FOL_str)

print(samples[-1])
print('goF = {}'.format(goF))
print('goL = {}'.format(goL))
print('goR = {}'.format(goR))

file = open('temp_data.txt','w')
for sample in samples:
    for element in sample:
        file.write(element + '\n')
    file.write('\n\n\n')
file.close()
        