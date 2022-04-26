# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 07/26/20

import csv
import io

with open('dropship.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('dropship.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #desired_column = [6]
          for line in reader:
              #upcColumn = list(line[i] for i in desired_column)
              itemNColumn = line[2]
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              if  not itemNColumn:
                      print(line[0], line[2], 'has itemNO empty String?')
                      line[2] = "*itemNOempty*"
              writer.writerow(line)
rf.close()
wf.close()
