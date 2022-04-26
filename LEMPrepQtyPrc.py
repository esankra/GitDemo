# parse Lemar csv file converted from xls->xlsx-Csv
# prepare only relevant data from original csv file and create sku,qty and price files 
# Author : Sankar Ramaiah
# 12/12/21 - copy of original BD load prep program modified
import csv
import io
i=0
DefQty=1 # if row in vendor feed product is available, qty not provided 
markupPct=0.42 # may not use this here
INSTK='available'
recCount=0
filenameCsv="LeeMarPet.com_Inventory.csv"
#
rStr='Restricted'
aStr='Allowed'
dStr='Discontinued'
##
with open('mws/data/'+filenameCsv, 'r') as rf: # origianl vendor feed 
     reader = csv.reader(rf, delimiter=',')
     with open('LEMQtyPrc.csv', 'w') as wf:
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
              amznR=line[6]
              wlmtR=line[7]
              ebayR=line[8]
              # revisit following checks later as it is not providing expected result
              #if rStr or aStr or dStr not in amznR:
              #    print("Unexpected value in Amazon Restricted Column...skipping row",skuIn,amznR)
              #    continue
              #if rStr or aStr or dStr not in wlmtR:
              #    print("Unexpected value in Walmart Restricted Column...skipping row",skuIn,wlmtR)
              #    continue
              #if rStr or aStr or dStr not in ebayR:
              #    print("Unexpected value in ebay Restricted Column...skipping row",skuIn,ebayR)
              #    continue
              #line[0]=skuIn
              ##print(line[0])
              #print(line[35])
              #try:
              #   float(shipWtstr)
              #   #print('float')
              #except ValueError:
              #   print (skuIn,shipWtstr,"ship wt Not a float..skipping this row ...")
              #   continue # skip row and continue loop
              #shipWt=float(shipWtstr)
              ##shipWt=float(line[35])
              #print(shipWt*shipFeePerLb)
              #shipCost=(shipWt*shipFeePerLb)
              #totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              ####print('total ship fee for sku= ',skuIn, totalShipCost)
              qtyIn=line[1]
              try:
                  int(qtyIn)
              except ValueError:
                  print (skuIn,qtyIn,"Qty not integer.. skipping this row ...")
                  continue
              qtyOut=int(qtyIn)
              # validate price
              Spricestr=line[2] # 
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
              lines = [skuIn,qtyIn,Spricestr,amznR,wlmtR,ebayR]
              writer.writerow(lines)
              #writer.writelines(lines)
print("Total records in feed = ",recCount)
rf.close()
wf.close()
##############################
