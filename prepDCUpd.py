## 12-29-21 - Modified to determine whic col to match sku while finding records in vendor data
# single module to prep price and qty files used to upload to wlmt and amzn
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
# 12-10-21 - prep raw update files - later formated to xmls to upload to mkt channels
#Revisions
# 12-11-21 - added logic to compute markup here as rounding 2x causes a penny difference
# added pirceChange log to track price changes and count of items needing qty changes
import csv
import io
i=0
markupPct=0.42  # we cancalc our own markup here if needed or use precalculated from DCQtyPrc
prefix="DC-"
pack2Str="Pack of 2"
pack2Ctr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds

#
p = open('DCPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
L = open('DCChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/DC_AMZN_SKU_LIST.txt', 'r') as rf: # previosuly prepared with unitcost and unit price
     reader = csv.reader(rf, delimiter='\t')
     with open('DCQty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in amzn sku list w/prefix
              #################################################################################
              # analyze the sku in to see which column on vendor input it should be matched with 
              a=skuIn[3:] # strip prefix to get the number parts if they are indded number
              useCol=3 # default to col3 match - majority of our skus are col3 
              try:
                  int(a)    # if exception raised we assign col3 and move fwd
                  i=int(a)  # if it is int then proceed this way
                  if i <= 5000:
                      useCol=1  # skuDC1 match with skuIn
              except ValueError:
                  useCol=3  #skuDC2 match with skuIn
              #print("Match column to use found to be =",useCol,skuIn)
              #################################################################################
              titleIn=line[2] # title needed for determining packsize
              priceIn=line[3] # price listed
              qtyIn=line[4] # qty listed
              priceinF=float(priceIn)
              pkSize=1
              qtyI=int(qtyIn) # listed qty integer
              #determine pksize based on title
              if pack2Str in titleIn:
                  pack2Ctr +=1
                  pkSize=2
              found=0
              #print('sku= ',line[0])
              with open('DCQtyPrc.csv', 'r') as f:   # custom vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuDC1=prefix+line[0] # pid
                    skuDC2=prefix+line[1] # cold 2 in our dcqtyprc custom made file
                    unitCoststr=line[2] # already marked up price at 42%
                    priceUCF=float(unitCoststr) 
                    qtyDC=line[3] #1
                    priceDCstr=line[4] # vendor unit price
                    priceUPC=float(priceDCstr) # vendor unit price w/out any shipping
                    ######################################################################
                    # assign correct skuDC to match for the current record based on useCol
                    skuDC=skuDC2  # use col 3 vendor sku as default
                    if useCol == 1:
                        skuDC=skuDC1  # chang to use DC1
                    #######################################################################
                    if skuDC == skuIn:
                        found=1  # our sku list item matches vendor feed
                        if qtyI == 0:
                            qtyOut=1  # turn on 
                            qChngCtrOn +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                        #priceV = (priceUCF*pkSize) # use this or calc from UPC unit price
                        # recalc price here at different markup if needed
                        ourCost=(priceUPC*pkSize) # price of unit for pkSize Units
                        markUp=(ourCost*markupPct)
                        totalCost=(ourCost+markUp) #  add on markup value
                        priceV=round(totalCost,2)
                        if priceinF != priceV: 
                            priceData=skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            priceLog=skuIn+" Price Listed= "+str(priceinF)+" newPrice= "+str(priceV)+"\n"
                            L.write(priceLog)  # for auditing and reference only
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  if qtyI == 1:
                      qtyOut=0  # turn OFF
                      qChngCtrOff +=1 
                      lines=[skuIn,qtyOut]
                      writer.writerow(lines)
#dump to change log instead of print

priceLog="Total Items Price Changed = "+str(pChngCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items Activated  = "+str(qChngCtrOn)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items DeActivated = "+str(qChngCtrOff)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items in SKU LIST = "+str(recCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total 2 pack Items in SKU LIST = "+str(pack2Ctr)+"\n"
L.write(priceLog)  # for auditing and reference only
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
p.close()
L.close()
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

