


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
    
collection = [
[{'2': 0, '3': 0, '4': 0, '5': 0, '6': 1, '7': 0, '8': 0}, False],
[{'2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}, True],
[{'2': 0, '3': 0, '4': 0, '5': 0, '6': 1, '7': 0, '8': 0}, False],
             ]
             
writeAbsEnvToFile(collection)




# lcbehind(t,lc)
# lbbehind(t,lb)
# labehind(t,la)
# target(t)
# fcfront(t,fc)
# fbfront(t,fb)
# fafront(t,fa)