# parse homeroot.csv
# prepare only relevant data from original csv file and create sku,qty and price file for DC
# Author : Sankar Ramaiah
# 12/25/21 - copy of original BD load prep program modified
import csv
import io
i=0
DefQty=1 # if row in vendor feed product is available, qty not provided 
markupPct=0.42
INSTK='available'
recCount=0
#
with open('cars.txt', 'r') as rf: # origianl vendor feed 
     reader = csv.reader(rf, delimiter='\t')
     with open('DCQtyPrc.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
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
              #line[6] = "NA"
              ## removing loop to set NA - not needed as we dont write out these columns
              #for i in range(0,35):
                #if not line[i].strip():
                     #print(line[i], 'has NO value - empty String?')
                      #line[i] = "NA"
                #else
              skuOut=line[0]
              sku2Out=line[2] # need col1 & 3 
              #line[0]=skuIn
              ##print(line[0])
              #print(line[35])
              #shipWtstr=line[35]
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
              Spricestr=line[7] # col 8 in vendor feed 
              try:
                 float(Spricestr)
                 #print('float')
              except ValueError:
                 print (sku2Out,Spricestr,"price Not a float.. skipping this row ...")
                 continue # loop
              Sprice=float(Spricestr)   ## sale price in vendor
              ##Sprice=float(line[11])   ## sale price in vendor
              ##print(Sprice)
              pctOfprice = (Sprice*markupPct) #price markup amount
              ourPrice = (Sprice+pctOfprice)
              ###print('ourPrice',ourPrice)
              priceOut = round(ourPrice,2) # final list price
              UnitPriceOut = round(Sprice,2)
              ##print('markuprice',line[10])
              ##print('OurPrice for sku= ',skuIn, line[10])
              # write out needed cols only
              #print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              ## output variables defined
              itemName=line[3]
              #lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              ##lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              # writeout relevant data for monitoring and translate status to qty available
              #if status == INSTK:
              #    qty=1
              #else:
              #    qty=0
              qtyOut=DefQty
              lines = [skuOut,sku2Out,priceOut,qtyOut,UnitPriceOut]
              writer.writerow(lines)
              #writer.writelines(lines)
print("Total records in feed = ",recCount)
rf.close()
wf.close()
##############################
