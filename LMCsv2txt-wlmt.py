# parse homeroot.csv
# Author : Sankar Ramaiah
# 5/18/21 - convert Le daily catalog to text file with filling empty columns
import csv
import io
i=0
with open('Leemar.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('Leemar.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              #if len(line) == 0:
              #   print('length of line is 0?')
              #   continue
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[0]    # sku
              #line[4] = "***NULLIFIED-Not Used***"
              #if len(itemNColumn) == 0:
              #if not upcColumn.strip():
              for i in range(0,24):
                if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                      line[i] = "NA"
              writer.writerow(line)
rf.close()
wf.close()
