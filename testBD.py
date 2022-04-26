# parse homeroot.csv
# Author : Sankar Ramaiah
# 5/18/21 - convert Le daily catalog to text file with filling empty columns
import csv
import io
i=0
shipFeePerOrder=4.70
shipFeePerItem=0.30
shipFeePerLb=0.75
discountPct=0.20
markupPct=0.45
#
qlist =[]
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
with open('BD_WLMT_SKU_LIST.txt', 'r') as rf:
     reader = csv.reader(rf, delimiter='\t')
     with open('bbdQty.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              sku=line[0]
              qtyIn=0
              #print('sku= ',line[0])
              with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
                readerV = csv.reader(f, delimiter='\t')
                for line in readerV:
                    skuIn=line[0]
                    if sku == skuIn:
                        priceIn=line[1]
                        qtyIn=line[2]
                        print('matched',skuIn,priceIn,qtyIn)
              #   print(sku,' Not in vendor list - setting qty=0 ')
              lines=[sku,priceIn,qtyIn]
#
              #   continue
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[0]    # sku
              #line[4] = "***NULLIFIED-Not Used***"
              #if len(itemNColumn) == 0:
              #if not upcColumn.strip():
              #line[6] = "NA"
              #for i in range(0,35):
              #  if not line[i].strip():
              #       #print(line[i], 'has NO value - empty String?')
              #        line[i] = "NA"
              #  #else
              #skuIn=line[0]
              #line[0]='BD-'+skuIn
              #print(line[0])
              ##print(line[35])
              #shipWt=float(line[35])
              #print(shipWt*shipFeePerLb)
              #shipCost=(shipWt*shipFeePerLb)
              #totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              #print('total ship fee for sku= ',skuIn, totalShipCost)
              #Sprice=float(line[11])   ## sale price in vendor
              #print(Sprice)
              #pctOfprice = (Sprice*discountPct) #price discount
              #ourPrice = (Sprice-pctOfprice)+totalShipCost
              #print('ourPrice',ourPrice)
              #markupPrice = (ourPrice*markupPct)+ourPrice
              #line[10] = round(markupPrice,2) # here we use the street price col to store our computed price 
              #print('markuprice',line[10])
              #print('OurPrice for sku= ',skuIn, line[10])
              ## write out needed cols only
              ##print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              #### output variables defined
              #skuOut=line[0]
              #itemName=line[2]
              #desc1=line[6]
              #desc2=line[7] # details formated
              #condition=line[8]
              #status=line[9] # in-stock or out-of-stock
              #price=line[10]
              #img1=line[14] #main image
              #img2=line[15] # additional 1
              #img3=line[16] # additional 2
              #shipWtout=shipWt
              ##custom cols needed for uploading to marketplaces
              #pIdtype='GTIN'
              ###pId='PlaceHolder'   
              #pId=line[9]   # this place holder for GTIN for upload, we store the inventory status here for monitoring!
              #brandN='Generic'
              ##lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              ##lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              writer.writerow(lines)
              #writer.writelines(lines)
rf.close()
wf.close()
