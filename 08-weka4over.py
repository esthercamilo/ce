import os
types=['rich','both','auxo']
def convert():
	print '***********CONVERTING FROM CSV TO ARFF - remove gene\n'
	os.system("java weka.filters.unsupervised.attribute.Remove -R 1 -i weka/rich/oversampling/over_CE_rich.csv -o weka/rich/oversampling/over_CE_rich.arff")
	os.system("java weka.filters.unsupervised.attribute.Remove -R 1 -i weka/both/oversampling/over_CE.csv -o weka/both/oversampling/over_CE.arff")
	os.system("java weka.filters.unsupervised.attribute.Remove -R 1 -i weka/auxo/oversampling/over_CE_aux.csv -o weka/auxo/oversampling/over_CE_aux.arff")

#convert()
def J48():
	f1 = "weka/rich/oversampling/over_CE_rich.arff"
	f2 = "weka/both/oversampling/over_CE.arff"
	f3 = "weka/auxo/oversampling/over_CE_aux.arff"
	nLeaves = '800'
	os.system("java -Xmx1000m weka.classifiers.trees.J48 -M " + nLeaves + " -t " + f1 + " -i > " + f1.replace(".arff","result.txt"))
	os.system("java -Xmx1000m weka.classifiers.trees.J48 -M " + nLeaves + " -t " + f2 + " -i > " + f2.replace(".arff","result.txt"))
	os.system("java -Xmx1000m weka.classifiers.trees.J48 -M " + nLeaves + " -t " + f3 + " -i > " + f3.replace(".arff","result.txt"))
	os.system("java -Xmx1000m weka.classifiers.trees.J48 -g -M " + nLeaves + " -t " + f1 + " -i > " + f1.replace(".arff","result.dot"))
	os.system("java -Xmx1000m weka.classifiers.trees.J48 -g -M " + nLeaves + " -t " + f2 + " -i > " + f2.replace(".arff","result.dot"))
	os.system("java -Xmx1000m weka.classifiers.trees.J48 -g -M " + nLeaves + " -t " + f3 + " -i > " + f3.replace(".arff","result.dot"))

#J48()

def drawtree():
	f1 = "weka/rich/oversampling/over_CE_richresult.dot"
	f2 = "weka/both/oversampling/over_CEresult.dot"
	f3 = "weka/auxo/oversampling/over_CE_auxresult.dot"
	os.system("dot -Tpng " + f1 + " -o " + f1.replace('.dot','.png'))
	os.system("dot -Tpng " + f2 + " -o " + f2.replace('.dot','.png'))
	os.system("dot -Tpng " + f3 + " -o " + f3.replace('.dot','.png'))

drawtree()				
			
				