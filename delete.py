import os
import time
from pracmln import MLN, Database
from pracmln import query


# def test_inference_smokers(mln):
    # db = Database(mln, dbfile='%s:test_1.db' % p)
    # print('=== INFERENCE TEST:', 'EnumerationAsk', '===')
    # result = query(queries='safe(T1)',
                  # method='EnumerationAsk',
                  # mln=mln,
                  # db=db,
                  # verbose=False,
                  # multicore=False).run()
    # return result.results
    
    
    
def inference_obs(mln,obs_str_list):
    db = Database(mln)
    for e in obs_str_list:
        db << e
    print('=== INFERENCE TEST:', 'EnumerationAsk', '===')
    result = query(queries='safe(T1)',
                  method='EnumerationAsk',
                  mln=mln,
                  db=db,
                  verbose=False,
                  multicore=False).run()
    return result.results    
    
    

p = os.path.join('./drive', 'highway.pracmln')
mln = MLN(mlnfile=('%s:sample50-test.mln' % p),
          grammar='StandardGrammar',logic='FirstOrderLogic')
          
obs = [
            'lcbehind(T1,Lc1)',
            'lbbehind(T1,Lb1)',
            'labehind(T1,La1)',
            'target(T1)',
            'fcfront(T1,Fc1)',
            'fbfront(T1,Fb1)',
            'fafront(T1,Fa1)',
            'lchas(Lc1,Free)',
            'lbhas(Lb1,Free)',
            'lahas(La1,Free)',
            'thas(T1,Free)',
            'fchas(Fc1,Speedsame)',
            'fbhas(Fb1,Speedlow)',
            'fahas(Fa1,Free)'
          ]

start = time.time()
for i in range(50):
    print(i)
    result = inference_obs(mln,obs)
    print(result)
    print('\n\n')
end = time.time()
print('Time elapsed:{}'.format(end-start))