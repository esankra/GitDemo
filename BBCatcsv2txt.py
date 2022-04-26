# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 5/13/21
# just convert BrybellyCatalog.csv (as downloaded) to txt due to commas in name
#
import csv
import io

with open('BrybellyCatalog.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('BrybellyCatalog.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
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
