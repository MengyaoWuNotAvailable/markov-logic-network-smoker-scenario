import os

from pracmln import MLN, Database
from pracmln import query, learn
from pracmln.mlnlearn import EVIDENCE_PREDS
import time

from pracmln.utils import locs


from pracmln import MLN
from pracmln import Database
from pracmln import MLNQuery, query
from pracmln.mlnlearn import MLNLearn
import os
from pracmln.utils.config import global_config_filename
from pracmln.utils.project import PRACMLNConfig
from pracmln.utils import config, locs

from pracmln import query, learn

def read_predicate(paths):
    predicate = []
    base_path = os.getcwd()
    file = open(base_path + '/' + paths,'r',encoding = 'utf8')
    predicate = file.read()
    predicate = predicate.split('\n')
    predicate_list = [x.split('(')[0] for x in predicate]
    predicate_list2 = [x.split('(')[1].replace(' ','').lower() for x in predicate]
    predicate = []
    for i in zip(predicate_list,predicate_list2):
        predicate.append(i[0] + '(' + i[1])
    return predicate



def read_formula(paths,predicates):
    predicate_list = [x.split('(')[0] for x in predicates]
    predicate_list = predicate_list + ['!'+x for x in predicate_list]
    predicate_list = [' '+x for x in predicate_list]
    predicate_list = [(x.lower(),x) for x in predicate_list]
    formula = []
    base_path = os.getcwd()
    file = open(base_path + '/' + paths,'r',encoding = 'utf8')
    formula = file.read()
    formula = formula.split('\n')
    formula = [x for x in formula if x !='']
    formula = [x.replace(' or ',' v ').replace(' and ',' ^ ').replace(':','') for x in formula]
    #exist_list = [x for x in formula if 'Exists ' in x]
    formula = [x for x in formula if 'Exists ' not in x] 
    return formula


def read_data(paths, predicate=None):      # 读txt数据用
    content = []
    base_path = os.getcwd()
    file = open(base_path + '/' + paths,'r',encoding = 'utf8')
    pre_content = file.read()
    pre_content = pre_content.split('###')
    pre_content = [x for x in pre_content if x !='']
    for i in pre_content:
        element = i.split('\n')
        element = [x.replace(':','_') for x in element if x !='']
        for j in element[1::]:
            splited = j.split('(')
            content.append((element[0],splited[0]+'('+splited[1].upper()))    
            # pracmln 要求 证据数据库db中的格式為 Predicate(CONTANT_1), 即谓语首字及谓语内
            # 变量contant首字為大写, 还有不可以有空格. 这里单纯方便而把变量大写
            # 另外暂不支持中文输入.        
    return content


def write_db(data_file):
    db = Database(mln)

    data_str = read_data(data_file)

    try:
        for i in enumerate(data_str):
            db << i[1][1]
            print('input database successful : ' + i[1][0] + ' : ' +i[1][1])
    except :
        for j in data_str[i[0]::]:
            db << j[1]
            
    return db
 
        
mln = MLN(grammar='StandardGrammar', logic='FirstOrderLogic')

predicates = read_predicate('predicate_LRF.txt')

for p in predicates:
    mln << p
mln << 'speed={Free,Speedhigh,Speedlow}'


formulas = read_formula('formula_LRF.txt',predicates)

for f in formulas:
    if f.endswith('.'):
        f = f.replace('.','')
        ###CHANGE THIS!!!!!! used for hard constraint
        mln.formula(f,weight=100.0,fixweight=True)
    else:
        mln.formula(f,weight=0.0,fixweight=False)


mln.write()
#db_train = write_db('temp_data.txt')

p = os.path.join('drive','debug.pracmln')
#mln = MLN(mlnfile=('%s:debug.mln' % p), grammar='StandardGrammar')
#mln.write()
db = Database(mln, dbfile='%s:20samples.db' % p)

db.write()
learn(method='BPLL_CG',
      mln=mln,
      db=db,
      verbose=True,
      multicore=True).run()   




infer = '1'
while infer != '0':
    infer = input('0 to stop, 1 to continue inference:')
    if infer == '0':
        confirm = input('Are you sure to stop infer? Type yes to confirm:')
        if confirm == 'yes':
            break
    
    db_test = write_db('data_LRF_test.txt')
    db_test.write()
    inference_str('betterfa(FA1),betterlb(LB1),betterrb(RB1)', mln=learnt_mln, db=db_test)

