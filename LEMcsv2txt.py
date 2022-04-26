# parse Lemar 
# Author : Sankar Ramaiah
# Date: 10/21/20

import csv
import io

with open('lmr.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('lmr.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #desired_column = [6]
          for line in reader:
              #upcColumn = list(line[i] for i in desired_column)
              itemNColumn = line[2]
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              if  not itemNColumn:
                      print(line[0], line[2], 'has Column C empty String?')
                      line[2] = "*empty*"
              writer.writerow(line)
rf.close()
wf.close()
