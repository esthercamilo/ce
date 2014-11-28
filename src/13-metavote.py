#################################
#AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################


#IMPORTANT
#Meta vote cannot handle multi-valued nominal class!

import os

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')
wekalocation = fcfg.readline().rstrip('\n')


types = ['auxo', 'rich', 'both']


def makedir(f):
    if not os.path.exists(f):
        os.makedirs(f)

for t in types:
    f1 = folder+'weka/'+t+'/vote_threshold'
    f2 = folder+'weka/'+t+'/vote_result'
    makedir(f1)
    makedir(f2)

#FOR EXPERIMENT

for t in types:

    for x in ['','_rnd']:
        for i in range(1,101):

            print "\nMETA VOTE ",i

            os.system('java -cp '+wekalocation+' -Xmx4000m weka.classifiers.meta.Vote  \
            -B "weka.classifiers.meta.Bagging -P 100 -I 20 -W weka.classifiers.trees.REPTree -- -M 2 -V 0.0010 -N 3 -L -1" \
            -B "weka.classifiers.meta.Bagging -P 100 -I 20 -W weka.classifiers.trees.NBTree" \
            -B "weka.classifiers.meta.Bagging -P 100 -I 20 -W weka.classifiers.trees.RandomTree -- -K 1 -M 1.0" \
            -B "weka.classifiers.meta.Bagging -P 100 -I 20 -W weka.classifiers.trees.RandomForest -- -I 10 -K 0" \
            -B "weka.classifiers.meta.Bagging -P 100 -I 20 -W weka.classifiers.trees.J48 -- -C 0.5 -M 32"\
            -B "weka.classifiers.meta.Bagging -P 100 -I 20 -W weka.classifiers.trees.BFTree -- -M 32 -N 5 -C 1.0 -P POSTPRUNED"\
            -R AVG -t '+folder+'weka/'+t+'/arff'+x+'/'+str(i)+'.arff -i > '+folder+'weka/'+t+'/vote_result'+x+'/'+str(i)+'-result.txt')






