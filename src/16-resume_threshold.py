#################################
#AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################

import os
fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

types = ['rich', 'auxo', 'both']

for t in types:

    out_name = folder+'weka/'+t+'/vote_threshold_resume.txt'
    f_out = open(out_name,'w')
    f_out.write('FP_rate,TP_rate\n')

    for i in range(1,101):
        f_in = open(folder+'weka/'+t+'/vote_threshold/'+str(i)+'.csv')
        header = f_in.readline()
        for l in f_in:
            d = l.split(',')
            fp = d[4]
            tp = d[5]
            f_out.write('%s,%s\n' % (fp,tp))
        f_in.close()
    f_out.close()
    os.rename(out_name,folder+'R/'+t+'_threshold.txt')


"x"



