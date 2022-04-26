# parse homeroot.csv
# Author : Sankar Ramaiah
# Date: 8/10/20
# 10-31-20 - updated to nullify the description column as it causes offset due to delimiter chars in it
import csv
import io
i=0
with open('KHD_Image_Links_1020.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('KHD_images.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
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
              for i in range(0,5):
                if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                      line[i] = "*Empty*"
              writer.writerow(line)
rf.close()
wf.close()
