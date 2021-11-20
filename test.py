from pracmln import MLN
from pracmln import Database
from pracmln import MLNQuery, query
from pracmln.mlnlearn import MLNLearn
import os
from pracmln.utils.config import global_config_filename
from pracmln.utils.project import PRACMLNConfig
from pracmln.utils import config, locs

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
    print(data_str)

    try:
        for i in enumerate(data_str):
            db << i[1][1]
            print('input database successful : ' + i[1][0] + ' : ' +i[1][1])
    except :
        for j in data_str[i[0]::]:
            db << j[1]
            
    return db
    

def inference_str(query_str, db, mln):
    print(query(queries=query_str, method='EnumerationAsk', mln=mln, db=db, verbose=True, multicore=False, save = True, output_filename=r'learnt.dbpll_cg.student-new-train-student-new-2.mln').run().results)
#Other Methods: EnumerationAsk, MC-SAT, WCSPInference, GibbsSampler


def learn_with_config(database,mln):
    DEFAULT_CONFIG = os.path.join(locs.user_data, global_config_filename)
    conf = PRACMLNConfig(DEFAULT_CONFIG)
    
    config = {}
    config['verbose'] = True
    config['discr_preds'] = 0
    config['db'] = database
    config['mln'] = mln
    config['ignore_zero_weight_formulas'] = 0    #0
    config['ignore_unknown_preds'] = 0   #0
    config['incremental'] = 0   #0
    config['grammar'] = 'StandardGrammar'
    config['logic'] = 'FirstOrderLogic'
    config['method'] = 'BPLL_CG'    # BPLL, CLL (composite log..), BPLL_CG (fast conjunction)
    config['multicore'] = True
    config['profile'] = 0
    config['shuffle'] = 0
    config['prior_mean'] = 0
    config['prior_stdev'] = 5   # 5
    config['save'] = True
    config['use_initial_weights'] = True
    config['use_prior'] = 0
    #config['output_filename'] = 'learnt.dbpll_cg.student-new-train-student-new-2.mln'
    # 亲测无效, 此句没法储存.mln 档案
    #config['infoInterval'] = 500
    #config['resultsInterval'] = 1000
    conf.update(config)
    
    print('training...')
    learn = MLNLearn(conf, mln=mln, db=database)
    #learn.output_filename(r'C:\Users\anaconda3 4.2.0\test.mln')
    # 亲测无效, 此句没法储存.mln 档案
    mln_learnt = learn.run()
    print('finished...')
    #return mln_learnt which can be used for inference, but the file is not saved.
    return mln_learnt
        
        
        
        
        
mln = MLN(grammar='StandardGrammar', logic='FirstOrderLogic')

predicates = read_predicate('predicate_LRF.txt')

for p in predicates:
    mln << p
mln << 'speed={Free,Speedhigh,Speedlow}'

#mln << 'p={F1,F2,F3,F4,B1,B2,B3,B4}'
#mln << 't={T1,T2,T3,T4}'

print('Below are predicates:')
for p in mln.predicates:
    print(p)


formulas = read_formula('formula_LRF.txt',predicates)

print(formulas)

for f in formulas:
    if f.endswith('.'):
        f = f.replace('.','')
        ###CHANGE THIS!!!!!! used for hard constraint
        mln.formula(f,weight=100.0,fixweight=True)
    else:
        mln.formula(f,weight=0.0,fixweight=False)


print('Below are formulas:')
for f in mln.formulas:
    print(f)
    f.print_structure()
    
#mln = MLN(mlnfile='learnt.mln',grammar='StandardGrammar', logic='FirstOrderLogic')   
    

db_train = write_db('temp_data.txt')
db_train.write()

    
learnt_mln = learn_with_config(db_train,mln)
#learnt_mln = mln.learn([db_train])
learnt_mln.tofile(os.getcwd() + '/' + 'learnt.mln')
#learnt_mln.write()


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
