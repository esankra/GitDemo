# parse homeroot.csv
# Author : Sankar Ramaiah
# 1-17-21 - convert finemod datasheet to fill empty cells
import csv
import io
i=0
with open('finemod_datasheet.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('finemod_datasheet_out.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #@writer = csv.writer(wf, delimiter='\t')
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
              for i in range(0,15):
                if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                      line[i] = "*Empty*"
              writer.writerow(line)
rf.close()
wf.close()
