# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 07/26/20
# 3/23/22 
## fixed bug checking correct column for item number (now col 0)
## added date logic to skip records with any date in future for the transit column (Coming back : dt) 
import csv
import io
# for date handling 
import datetime
from datetime import date
import time
from dateutil import parser
##a
recCtr=0
skipCtr=0
chkStr="coming back"
today = datetime.datetime.now()
print("Today's date:", today)

with open('dropship.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('dropship.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #desired_column = [6]
          for line in reader:
              skuIn=line[1] # sku in vendor feed
              transitCol=line[10] # item in transit or Coming Back :
              if chkStr in transitCol.lower():
                  recCtr +=1
                  myDtStr=transitCol[13:] # take date portion
                  # validate the date 
                  try:
                      #
                      VendorAddDt=parser.parse(myDtStr)
                  except ValueError:
                      print ("Sku = ",skuIn,"dt= ",myDtStr,"Invalid date skipping this row ...")
                      continue
                  VendorAddDt=parser.parse(myDtStr)
                  #print ("converted date = ", VendorAddDt)
                  if VendorAddDt > today:
                      #
                      skipCtr +=1
                      print (skuIn,"Vendor date is in future skipping this record..",VendorAddDt)
                      continue
#
              itemNColumn = line[0]  # first column in vendor feed
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              if  not itemNColumn:
                      print(line[0], skuIn, 'has itemNO empty String?')
                      line[0] = "*itemNOempty*"
              writer.writerow(line)

# print summary counts
print ("Total records with coming back in transit col = ",recCtr)
print ("Total records with future date in transit col = ",skipCtr)
##
rf.close()
wf.close()
