# single module to prep price and qty files used to upload to Amzn KHD-
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
# 12-12-21 - prep raw update files - later formated to xmls to upload to mkt channels
#Revisions
# 12-11-21 - added logic to compute markup here as rounding 2x causes a penny difference
# added pirceChange log to track price changes and count of items needing qty changes
import csv
import io
i=0
markupPct=0.40  # we cancalc our own markup here if needed or use precalculated from DCQtyPrc
prefix="KHD-"
pack2Str="Pack of 2"
pack2Ctr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
minQty=20
#lowPrice=20.00 # we force defshipping for all items below 20 regardless of pksize (pksize is either 1 or 2)
lowPrice=15.00 # we force defshipping for all items below 15 effective 1/4/22
DefShipFee=10.95
##shipFeePct=0.25
shipFeePct=0.35 # effective 1/4/22
#
p = open('KHDPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
L = open('KHDChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/KHD_AMZN_SKU_LIST.txt', 'r') as rf: # previosuly prepared with unitcost and unit price
     reader = csv.reader(rf, delimiter='\t')
     with open('KHDQty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in amzn sku list w/prefix
              titleIn=line[2] # title needed for determining packsize
              priceIn=line[3] # price listed
              qtyIn=line[4] # qty listed
              priceinF=float(priceIn)
              pkSize=1
              qtyI=int(qtyIn) # listed qty integer
              #determine pksize based on title
              pkSize=1
              if pack2Str in titleIn:
                  pack2Ctr +=1
                  pkSize=2
              found=0
              #print('sku= ',line[0])
              with open('KGIPQ.csv', 'r') as f:   # custom vendor data prepared previously combining price and qty files from vendor
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuKHD=prefix+line[0] # vendor sku
                    qtyKHD=line[2] #
                    unitCoststr=line[3] # already marked up price at 42%
                    priceKHDstr=line[8] # vendor unit price
                    priceUCF=float(unitCoststr) 
                    priceUPC=float(priceKHDstr) # vendor unit price w/out any shipping
                    qtyKHDI=int(qtyKHD)
                    ####################################################
                    if skuKHD == skuIn:
                        found=1  # our sku list item matches vendor feed
                        #################### DETERMINE QTY on or OFF ######################
                        if qtyI == 0 and qtyKHDI > minQty:
                            qtyOut=1  # turn on 
                            qChngCtrOn +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                        if qtyI > 0 and qtyKHDI <= minQty:
                            qtyOut=0  # turn off
                            qChngCtrOff +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                        ###########################################################################################
                        # Determine/calculate shipping for KHD 
                        ############################################################################################
                        shipFee=DefShipFee  # assume default
                        # recalc shipfee if it will be different than default fee
                        ourCost=(priceUPC*pkSize) # price of unit for pkSize Units
                        ourCost2Ship=(ourCost*shipFeePct) # shipping cost
                        if ourCost2Ship > DefShipFee:
                            shipFee=ourCost2Ship
                        #take the higher shipping cost unless item unit price is < lowPrice ($20)
                        if priceUPC <= lowPrice:
                            shipFee=DefShipFee  # force default ship fee for low price items regardless of pksize
                        #################################################################################################
                        # Compute Final cost with shipping and markup
                        #################################################################################################
                        totalCost=ourCost+shipFee # with shipping
                        markUp=(totalCost*markupPct) # markup amount on cost of product + shipping
                        finalCost=(totalCost+markUp) #  add on markup value
                        priceV=round(finalCost,2)
                        if priceinF != priceV: 
                            priceData=skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            priceLog=skuIn+" Listed Price= "+str(priceinF)+" newPrice= "+str(priceV)+" pkSize= "+str(pkSize)+" UnitP= "+unitCoststr+"\n"
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
priceLog="Total Items in AMZN SKU LIST = "+str(recCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total 2 pack Items in AMZN SKU LIST = "+str(pack2Ctr)+"\n"
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

