# parse HR csv file txt format downloaded directly from HR 
# prepare only relevant data from original csv file and create sku,qty and price files 
# Author : Sankar Ramaiah
# 12/13/21 - copy of original LEM prep qty prc module
import csv
import io
i=0
DefQty=1 # if row in vendor feed product is available, qty not provided 
markupPct=0.42 # may not use this here
INSTK='available'
recCount=0
filenameTxt="homeroots.txt"
#
##
with open(filenameTxt, 'r') as rf: # origianl vendor feed 
     reader = csv.reader(rf, delimiter='\t')
     with open('HRQtyPrc.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              recCount +=1
              #for i in range(0,35):
                #if not line[i].strip():
                     #print(line[i], 'has NO value - empty String?')
                      #line[i] = "NA"
                #else
              skuIn=line[0]
              leadTIn=line[12]  # leadtime days
              #line[0]=skuIn
              ##print(line[0])
              #print(line[35])
              try:
                 int(leadTIn)
              except ValueError:
                 print (skuIn,leadTIn,"Lead Time Not integer..skipping this row ...")
                 continue # skip row and continue loop
              qtyIn=line[13]
              try:
                  int(qtyIn)
              except ValueError:
                  print (skuIn,qtyIn,"Qty not integer.. skipping this row ...")
                  continue
              qtyOut=int(qtyIn)
              # validate price
              Spricestr=line[14] # Dropship cost in vendor 
              try:
                 float(Spricestr)
                 #print('float')
              except ValueError:
                 print (skuIn,Spricestr,"price Not a float.. skipping this row ...")
                 continue # loop
              Sprice=float(Spricestr)   ## sale price in vendor
              #UnitPriceOut = round(Sprice,2)
              #if status == INSTK:
              #    qty=1
              #else:
              #    qty=0
              lines = [skuIn,qtyIn,Spricestr,leadTIn]
              writer.writerow(lines)
              #writer.writelines(lines)
print("Total records in feed = ",recCount)
rf.close()
wf.close()
##############################
