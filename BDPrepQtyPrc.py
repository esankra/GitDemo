# parse homeroot.csv
# prepare only relevant data from original csv file and create sku,qty and price file
# Author : Sankar Ramaiah
# 11/25/21 - copy of original load prep program except we write out only limited data
# 12-5-21 updated price to add 3 if < 20 
import csv
import io
i=0
shipFeePerOrder=4.70
shipFeePerItem=0.30
shipFeePerLb=0.75
discountPct=0.20
markupPct=0.45
INSTK='in-stock'
lowPrice=20.00
addPrice=3.00
#
with open('bbd.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('bbdQtyPrc.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
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
              #line[6] = "NA"
              ## removing loop to set NA - not needed as we dont write out these columns
              #for i in range(0,35):
                #if not line[i].strip():
                     #print(line[i], 'has NO value - empty String?')
                      #line[i] = "NA"
                #else
              skuIn=line[0]
              line[0]='BD-'+skuIn
              ##print(line[0])
              #print(line[35])
              shipWtstr=line[35]
              try:
                 float(shipWtstr)
                 #print('float')
              except ValueError:
                 print (skuIn,shipWtstr,"ship wt Not a float..skipping this row ...")
                 continue # skip row and continue loop
              shipWt=float(shipWtstr)
              ##shipWt=float(line[35])
              #print(shipWt*shipFeePerLb)
              shipCost=(shipWt*shipFeePerLb)
              totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              ####print('total ship fee for sku= ',skuIn, totalShipCost)
              Spricestr=line[11]
              try:
                 float(Spricestr)
                 #print('float')
              except ValueError:
                 print (skuIn,Spricestr,"price Not a float.. skipping this row ...")
                 continue # loop
              Sprice=float(Spricestr)   ## sale price in vendor
              ##Sprice=float(line[11])   ## sale price in vendor
              ##print(Sprice)
              pctOfprice = (Sprice*discountPct) #price discount
              ourPrice = (Sprice-pctOfprice)+totalShipCost
              ###print('ourPrice',ourPrice)
              markupPrice = (ourPrice*markupPct)+ourPrice
              line[10] = round(markupPrice,2) # here we use the street price col to store our computed price 
              ##print('markuprice',line[10])
              ##print('OurPrice for sku= ',skuIn, line[10])
              # write out needed cols only
              #print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              ## output variables defined
              skuOut=line[0]
              itemName=line[2]
              desc1=line[6]
              desc2=line[7] # details formated
              condition=line[8]
              status=line[9] # in-stock or out-of-stock
              price=line[10]
              img1=line[14] #main image
              img2=line[15] # additional 1
              img3=line[16] # additional 2
              shipWtout=shipWt
              #custom cols needed for uploading to marketplaces
              pIdtype='GTIN'
              ##pId='PlaceHolder'   
              pId=line[9]   # this place holder for GTIN for upload, we store the inventory status here for monitoring!
              brandN='Generic'
              #lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              ##lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              # writeout relevant data for monitoring and translate status to qty available
              # if price less than low price value then add 3 to it 12-5-21
              if price < lowPrice:
                 #`line[10] = round(markupPrice,2) # here we use the street price col to store our computed price 
                 pricex=(price+addPrice)
                 price = round(pricex,2) #price incremet
#
              if status == INSTK:
                  qty=1
              else:
                  qty=0
              lines = [skuOut,price,qty]
              writer.writerow(lines)
              #writer.writelines(lines)
rf.close()
wf.close()
##############################
