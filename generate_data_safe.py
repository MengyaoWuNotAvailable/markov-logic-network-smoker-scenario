'''
la  lb  lc
    e   fa fb
ra  rb  rc
'''
import random

numSample = 50
samples = []
goL = 0
goR = 0
goF = 0
for num in range(1,numSample+1):

    blocks = {'B':0,'T':0,'F':0}

    for block in blocks:
        rand = random.randint(0,2)
        blocks[block] = rand


    FOL_str = ['front(T{},F{})'.format(num,num), 'behind(T{},B{})'.format(num,num)]


    if blocks['B'] == 0:
        FOL_str.append('bhas(B{},Free)'.format(num))
    elif blocks['B'] == 1:
        FOL_str.append('bhas(B{},Speedlow)'.format(num))
    else:
        FOL_str.append('bhas(B{},Speedhigh)'.format(num))
        

    if blocks['T'] == 0:
        FOL_str.append('free(T{})'.format(num))
    else:
        FOL_str.append('!free(T{})'.format(num))


    if blocks['F'] == 0:
        FOL_str.append('fhas(F{},Free)'.format(num))
    elif blocks['F'] == 1:
        FOL_str.append('fhas(F{},Speedlow)'.format(num))
    else:
        FOL_str.append('fhas(F{},Speedhigh)'.format(num))
        



    if (blocks['T'] ==0 and blocks['B'] <= 1 and blocks['F'] !=1):
        FOL_str.append('safe(T{})'.format(num))
        goL += 1
    else:
        FOL_str.append('!safe(T{})'.format(num))


    
    samples.append(FOL_str)

print(samples[-1])
print('goL = {}/{}'.format(goL,numSample))

file = open('temp_data.txt','w')
for sample in samples:
    for element in sample:
        file.write(element + '\n')
    file.write('\n\n\n')
file.close()
        