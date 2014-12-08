# ################################
# AUTHOR: ESTHER CAMILO          #
#e-mail: esthercamilo@gmail.com  #
##################################


import os
from threading import Thread

fcfg = open('config.txt')
folder = fcfg.readline().rstrip('\n')

wekalocation = fcfg.readline().rstrip('\n')

threads = []
end = 101

tipos = ['auxo','rich','both']

# Convert csv to arff
def convert():
    print '***********CONVERTING FROM CSV TO ARFF'
    os.system(
        "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "files/completeTraining.csv > " + folder + "weka/completeTraining.arff")
    for t in tipos:
        for i in range(1, end):
            #EXPERIMENT
            print '\nExp: ',i,' Type: ',t,'\n'
            os.system(
                "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "weka/"+t+"/csv/" + str(
                    i) + ".csv > " + folder + "weka/"+t+"/arff/" + str(i) + ".arff")
            #RANDOM
            os.system(
                "java -cp " + wekalocation + " weka.core.converters.CSVLoader " + folder + "weka/"+t+"/csv_rnd/" + str(
                    i) + ".csv > " + folder + "weka/"+t+"/arff_rnd/" + str(i) + ".arff")

#J48 output result, dot, model
def j48(tipo, nleaves):
    print '***********J48 output result, dot, mode for the type: ',tipo
    for x in ["","_rnd"]:
        for i in range(1, end):
            tstr1 = "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -d  " + folder + "weka/"+tipo+"/model/" + str(
                i) + ".model -M "+nleaves+" -t " + folder + "weka/"+tipo+"/arff"+x+"/" + str(
                i) + ".arff -i  > " + folder + "weka/"+tipo+"/result"+x+"/" + str(i) + "-result.txt"
            os.system(tstr1)
    print "result for dot"
    for i in range(1,end):
        tstr2 = "java -cp " + wekalocation + " -Xmx1000m weka.classifiers.trees.J48 -M "+nleaves+" -g -t " + folder + "weka/"+tipo+"/arff"+x+"/" + str(
                i) + ".arff -i  > " + folder + "weka/"+tipo+"/dot/" + str(i) + "-result.dot"
        os.system(tstr2)

def drawTrees(type):
    print '***********DRAWING TREES '
    for i in range(1, end):
        os.system("dot -Tpng " + folder + "weka/" + type + "/dot/" + str(
            i) + "-result.dot -o " + folder + "weka/" + type + "/png/" + str(
            i) + "result.png")


#It is important to keep the class order in training files
def setClassOrder(classe,tipo):
    namefile = folder + 'weka/completeTraining.arff'
    print "Setting class order"
    file = open(namefile)
    lines = file.readlines()
    s = [x for x in lines if '@attribute class' in x][0]
    index = lines.index(s)

    typeOfClass = '{'+classe+',ESSENTIAL,NORMAL}'
    newLine = s.replace('numeric', typeOfClass)
    lines[index] = newLine
    namefile1 = namefile.replace("weka","weka/"+tipo)
    output = open(namefile1.replace('.arff', '-'+classe+'.arff'), 'w')
    for i in range(len(lines)):
        output.write(lines[i])

    #correct the undersampling arff
    for i in range(1,101):
        name_f_in = folder + 'weka/'+tipo+'/arff/'+str(i)+'.arff'
        name_f_out = folder + 'weka/'+tipo+'/arff/'+str(i)+'.arff_o'
        f_under_in = open(name_f_in)
        f_under_out = open(name_f_out,'w')
        for l in f_under_in:
            if '{' in l and '@attribute class' not in l:
                s_replace = l[l.index('{'):len(l)-1]
                new_line = l.replace(s_replace,"{F,V}")
                f_under_out.write(new_line)
            elif '@attribute class' in l:
                new_line = '@attribute class {'+classe+',ESSENTIAL,NORMAL}\n'
                f_under_out.write(new_line)
            else:
                f_under_out.write(l)
        f_under_in.close()
        os.remove(name_f_in)
        os.rename(name_f_out,name_f_in)


# Convert from csv to arff
threadConvert = Thread(target=convert, args=())
threadConvert.start()
threadConvert.join()

threadj48aux = Thread(target=j48, args=('auxo','30'))
threadj48aux.start()
threadj48aux.join()

threadj48rich = Thread(target=j48, args=('rich','45'))
threadj48rich.start()
threadj48rich.join()

threadj48both = Thread(target=j48, args=('both','50'))
threadj48both.start()
threadj48both.join()

threadDrawTreesAux = Thread(target=drawTrees, args=(['auxo']))
threads.append(threadDrawTreesAux)
threadDrawTreesRich = Thread(target=drawTrees, args=(['rich']))
threads.append(threadDrawTreesRich)
threadDrawTreesBoth = Thread(target=drawTrees, args=(['both']))
threads.append(threadDrawTreesBoth)
[x.start() for x in threads]
[x.join() for x in threads]


tipos=[('CE-RICH','rich'),('CE-AUX','auxo'),('CE','both')]
for t in tipos:
    threadOrder = Thread(target=setClassOrder, args=(t[0],t[1]))
    threadOrder.start()
    threadOrder.join()

