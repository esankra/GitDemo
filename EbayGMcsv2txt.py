# parse homeroot.csv
# Author : Sankar Ramaiah
# Date: 11-5-20 
# converts active price qty report downloaded from EBAY to txt file - titles have comma and offsets processing
import csv
import io
i=0
with open('mws/data/ebay_Active_GRAND_MASTER.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('ebay_Active_GRAND_MASTER.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #desired_column = [6]
          for line in reader:
              for i in range(0,10):
                if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                      line[i] = "NA"
              writer.writerow(line)
rf.close()
wf.close()
#
