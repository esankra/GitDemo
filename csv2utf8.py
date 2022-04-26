# convert to utf8 for shopify uploading
# Author : Sankar Ramaiah
# Date: 12-18-21
##
import csv
import io
import sys
##
fileIn=(sys.argv[1])
fileOut=fileIn+"utf8"
print("File in = ",fileIn)
print("File Out = ",fileOut)
if  not fileIn:
    quit();

with open(fileIn+'.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open(fileOut+'.csv', 'w', encoding="utf-8") as wf:
          writer = csv.writer(wf)
          #desired_column = [6]
          for line in reader:
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[2]
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              #if  not itemNColumn:
              #        print(line[0], line[2], 'has itemNO empty String?')
              #        line[2] = "*itemNOempty*"
              writer.writerow(line)
rf.close()
wf.close()
