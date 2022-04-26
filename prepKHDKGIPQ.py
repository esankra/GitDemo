# parse KGIP and KGIQ
# Author : Sankar Ramaiah
# 12-7-21 - comines price and qty files from vendor download and gathers relevant data for next steps
# 12-8-21 - added aditional logic to compute unitcost(price+shipping)
# 12-8-21 - carry forward unit price in addition to Unit cost computed for pricing pack 2s later
import csv
import io
i=0
minQty=5
skipCount=0
shipPct=0.25
DefShipFee=10.95  # use this unless 25% of product cost is higher
markupPct=0.40
header=['Sku','Title','Quantity','Unit Cost','VendorUPC','Brand','Description','Item Weight','Item Price']
#
#p = open('bbdPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
with open('KGIQ.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('KGIPQ.csv', 'w') as wf:  # combine price and qty in one file output
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:  # qty file top loop
              sku=line[0]
              itemT=line[1]
              qtyIn=line[2]  # vendor qty
              itemL=line[5]
              itemW=line[6]
              itemH=line[7]
              itemWt=line[8]  # in case we redo walmart and need this data collect it now
              itemUpc=line[13]
              brandN=line[14]
              itemM=line[17] # material
              itemDesc=line[22]
              #validate qty
              try:
                  int(qtyIn)
              except ValueError:
                  skipCount +=1
                  print(sku,"invalid qty data..skiping..",qtyIn)
                  continue  # skip invalid data
              # skip qty 0 rows
              #qty=int(qtyIn)
              #if qty <= minQty:
              #    print(sku,"qty low .. skipping",qty)
#
              found=0
              #print('sku= ',line[0])
              with open('KGIP.csv', 'r', encoding="ISO-8859-1") as f:   # qty file from vendor
                readerP = csv.reader(f, delimiter=',')
                for line in readerP:
                    skuIn=line[0]
                    if sku == skuIn:
                        priceIn=line[2]  # vendor wholesale price
                        #qtyIn=line[2]
                        #print('matched',skuIn,priceIn,qtyIn)
                        found=1
              #print(sku,'foundflag = ',found)
              if found == 1:
                  #validate price
                  try:
                     float(priceIn)
                  except ValueError:
                     skipCount +=1
                     print(sku,"invalid price data..skiping..",priceIn)
                     continue  # skip invalid data
                  #
                  # compute unit cost (vendor price + shipping cost to us) no markup 
                  price=float(priceIn) #vendor price
                  shipFee=DefShipFee # unless next calc exceeds 
                  shipFeeP=(price*shipPct) # ship fee pct 25%
                  if shipFeeP > shipFee:
                      shipFee=shipFeeP
                  priceX=(price+shipFee)
                  unitCost = round(priceX,2) # single unit cost with pricing included
                  unitPrice = round(price,2) # single unit price without any ship fee added
                  addDesc=" Item Dimenions LxWxH in inches = "+itemL+"X"+itemW+"X"+itemH+" Material: "+itemM
                  ##print(sku, addDesc)
                  lines=[sku,itemT,qtyIn,unitCost,itemUpc,brandN,itemDesc+addDesc,itemWt,unitPrice]  # customized output cols
                  writer.writerow(lines)
                  #priceData=sku+","+priceIn+"\n"
                  #p.write(priceData)
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
              #writer.writelines(lines)
rf.close()
wf.close()
#p.close()
