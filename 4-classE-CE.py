from string import *
import re
import xlrd

outputAux = open('files/ceaux.tab','w')
outputRic = open('files/cerich.tab','w')
outputBot = open('files/ceboth.tab','w')

#return a dictionary key=GeneName,value=BlatnerName
def geneBlatner(fileName):
	file = open(fileName)
	labelfileGNB = file.readline()
	dicGNB={}
	for line in file:
		line = line.replace('"','').replace(" ","") #remove spaces and commas
		data = line.rstrip().split(",")
		names = data[3].split("//")
		dicGNB[data[0].lower()]=data[1]
		for elem in names:
			dicGNB[elem.lower()]=data[1]
	file.close()
	return dicGNB
	
	
dicGNB=geneBlatner('data/GeneNames.csv') #(GNB=GeneNameBlatner)

#READ XLS FILE

workbook = xlrd.open_workbook('data/NIHMS261392-supplement-04.xls')
worksheet = workbook.sheet_by_name('Sheet1')

listRich=[]
for i in range(2,118): 
	gene = str(worksheet.cell_value(i, 0))
	listRich.append(gene)

listAux=[]
for i in range(2,104): 
	gene = str(worksheet.cell_value(i, 1))
	listAux.append(gene)

bListRich=[] #bname
bListAux=[] #bname

for elem in listRich:
	data = elem.split('-')
	try:
		g=dicGNB[data[1].lower()]
		bListRich.append(g)
	except Exception as e:
		print e

for elem in listAux:
	data = elem.split('-')
	try:
		g=dicGNB[data[1].lower()]
		bListAux.append(g)
	except Exception as e:
		print e

bBoth = set(bListAux) | set(bListRich)
#remove empty elements:
bListBoth = [x for x in bBoth if x!='']

#Save files

def save(list,name):
	for elem in list:
		name.write(elem+'\n')

		
save(bListBoth,outputBot)		
save(bListAux,outputAux)		
save(bListRich,outputRic)	

#Generate list of ESSENTIALS
outputE = open('files/essential.tab','w')
workbookE = xlrd.open_workbook('data/msb4100050-s8.xls')
worksheet = workbookE.sheet_by_index(0)

listE=[]
for i in range(4,304): 
	gene = str(worksheet.cell_value(i, 6))
	listE.append(gene)
	outputE.write(gene+'\n')





	