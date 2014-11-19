# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com #
#################################

import os

types = ['rich', 'both', 'auxo']

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

wekalocation = fcfg.readline().rstrip('\n')


def convert():
    print '***********CONVERTING FROM CSV TO ARFF - remove gene\n'
    os.system(
        "java -cp " + wekalocation + " weka.filters.unsupervised.attribute.Remove -R 1 -i " + folder + "weka/rich/oversampling/over_CE_rich.csv -o " + folder + "weka/rich/oversampling/over_CE_rich.arff")
    os.system(
        "java -cp " + wekalocation + " weka.filters.unsupervised.attribute.Remove -R 1 -i " + folder + "weka/both/oversampling/over_CE.csv -o " + folder + "weka/both/oversampling/over_CE.arff")
    os.system(
        "java -cp " + wekalocation + " weka.filters.unsupervised.attribute.Remove -R 1 -i " + folder + "weka/auxo/oversampling/over_CE_aux.csv -o " + folder + "weka/auxo/oversampling/over_CE_aux.arff")


def J48():
    f1 = folder + "weka/rich/oversampling/over_CE_rich.arff"
    f2 = folder + "weka/both/oversampling/over_CE.arff"
    f3 = folder + "weka/auxo/oversampling/over_CE_aux.arff"
    nLeaves = '800'
    os.system(
        "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M " + nLeaves + " -t " + f1 + " -i > " + f1.replace(
            ".arff",
            "result.txt"))
    os.system(
        "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M " + nLeaves + " -t " + f2 + " -i > " + f2.replace(
            ".arff",
            "result.txt"))
    os.system(
        "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M " + nLeaves + " -t " + f3 + " -i > " + f3.replace(
            ".arff",
            "result.txt"))
    os.system(
        "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -g -M " + nLeaves + " -t " + f1 + " -i > " + f1.replace(
            ".arff",
            "result.dot"))
    os.system(
        "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -g -M " + nLeaves + " -t " + f2 + " -i > " + f2.replace(
            ".arff",
            "result.dot"))
    os.system(
        "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -g -M " + nLeaves + " -t " + f3 + " -i > " + f3.replace(
            ".arff",
            "result.dot"))


def drawtree():
    f1 = folder + "weka/rich/oversampling/over_CE_richresult.dot"
    f2 = folder + "weka/both/oversampling/over_CEresult.dot"
    f3 = folder + "weka/auxo/oversampling/over_CE_auxresult.dot"
    os.system("dot -Tpng " + f1 + " -o " + f1.replace('.dot', '.png'))
    os.system("dot -Tpng " + f2 + " -o " + f2.replace('.dot', '.png'))
    os.system("dot -Tpng " + f3 + " -o " + f3.replace('.dot', '.png'))


convert()
J48()
drawtree()
