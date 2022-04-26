# parse homeroot.csv
# Author : Sankar Ramaiah
# -2-12-22 - extract all recrods added before Oct21st - added date validation 
import csv
import io
#
import datetime
import time
from dateutil import parser
#
processedCount=0
recCount=0
Oct21str="Thu, 28 Oct 2021 19:26:03 +0000"  # oct 28th 2021
Oct21Dt=parser.parse(Oct21str)
#CurrentDtstr="Thu, 09 Dec 2021 19:26:03 +0000" #current when script modified overwritten later
#CurrentDt=parser.parse(CurrentDtstr)
i=0
with open('products.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('cars.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              recCount +=1
              #if len(line) == 0:
              #   print('length of line is 0?')
              #   continue
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[0]    # sku
              #line[4] = "***NULLIFIED-Not Used***"
              #if len(itemNColumn) == 0:
              #if not upcColumn.strip():
              skuOut=line[2] # 3rd row sku
              line[6] = "NA"
              for i in range(0,30):
                if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                      line[i] = "NA"
              VendorDtStr=line[24] # Date Added in vendor feed 
              # validate the date and skip invalid dates 2/12/22
              try:
                  #
                  VendorAddDt=parser.parse(VendorDtStr)
              except ValueError:
                  print ("SKU= ",skuOut,"dt= ",VendorDtStr,"Invalid date range.. skipping this row ...")
                  continue
              VendorAddDt=parser.parse(VendorDtStr)
              # write records that is < Oct21Dt 
              if  VendorAddDt < Oct21Dt:  # OCt 28th 2021 
                  processedCount +=1
                  writer.writerow(line)
#              
print("total records in vendor feed = ",recCount)
print("records for Monitoring = ",processedCount)
#
rf.close()
wf.close()
######################################
