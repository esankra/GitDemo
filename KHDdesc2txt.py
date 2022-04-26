# parse homeroot.csv
# Author : Sankar Ramaiah
# 1-17-21 - convert finemod datasheet to fill empty cells
import csv
import io
i=0
#with open('/mnt/c/ubuntushare/Bonanza-automation/KGI_Inventory_Count-customcolumns-desc.csv', 'r') as rf:
with open('/mnt/c/tmp/wlmt-khd-descFix/KGIQ_Inventory_Count-customcolumns-desc.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('/mnt/c/tmp/wlmt-khd-descFix/KGIQ_Inventory_Count-customcolumns-desc.txt', 'w') as wf:
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
              for i in range(0,7):
                if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                      line[i] = "N/A*"
              writer.writerow(line)
rf.close()
wf.close()
