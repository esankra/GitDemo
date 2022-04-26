# parse homeroot.csv
# prepare all active cars from DC with 43% markup for FB data source on commerce manager 11-28-21
# Author : Sankar Ramaiah
##
import csv
import io
i=0
shipFeePerOrder=4.70
shipFeePerItem=0.30
shipFeePerLb=0.75
discountPct=0.20
markupPct=0.45
INSTK='in-stock'
#
with open('products.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('cars-fb-load-4000+.csv', 'w') as wf:
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
              skuIn=line[2]  # dc code sku col
              line[0]='DC-'+skuIn
              ##print(line[0])
              #print(line[35])
              shipWt=float(line[35])
              #print(shipWt*shipFeePerLb)
              shipCost=(shipWt*shipFeePerLb)
              totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              ####print('total ship fee for sku= ',skuIn, totalShipCost)
              Sprice=float(line[11])   ## sale price in vendor
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
              itemName=line[3]
              desc1=line[5]
              #desc2=line[7] # details formated
              condition='new'
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
              if status == INSTK:
                  qty=1
              else:
                  qty=0
              lines = [skuOut,price,qty]
              writer.writerow(lines)
              #writer.writelines(lines)
rf.close()
wf.close()
