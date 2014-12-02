# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################

import os

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

wekalocation = fcfg.readline().rstrip('\n')


types = ['auxo', 'rich', 'both']


def clustering():
    for t in types:
        os.system(
            'java -cp '+wekalocation+' weka.clusterers.SimpleKMeans -p 0 -N 4 -t '+folder+'weka/' + t + '/matrix.csv > '+folder+'weka/' + t + '/cluster_assign.txt')


clustering()