# parse homeroot.csv
# Author : Sankar Ramaiah
# Date: 8/10/20

import csv
import io

with open('homeroots.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=';')
     with open('homerootsC.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='>>')
          #desired_column = [6]
          for line in reader:
              #upcColumn = list(line[i] for i in desired_column)
              itemNColumn = line[0]
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              if  itemNColumn.strip():
                      #print(line[0] 'has NO SKU - empty String?')
                      #line[2] = "*itemNOempty*"
                      writer.writerow(line)
rf.close()
wf.close()
