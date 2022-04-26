# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 07/26/20

import csv
import io

with open('koleimp.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('koleimp.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #desired_column = [6]
          for line in reader:
              #upcColumn = list(line[i] for i in desired_column)
              upcColumn = line[6]
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              if  not upcColumn:
                      print(line[0], line[6], 'has upc empty String?')
                      line[6] = "*UPCempty*"
              writer.writerow(line)
rf.close()
wf.close()
