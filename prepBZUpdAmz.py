# 1-21-22 - BEnzara AMZN qty update 
# Author : Sankar Ramaiah
# 
#Revisions
import csv
import io
i=0
markupPct=0.40  # we cancalc our own markup here if needed or use precalculated from DCQtyPrc
prefix="BZ-"
pack2Str="Pack of 2"
pack2Ctr=0
highPCtr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
minQty=150  # using high count 2/24/22
#lowPrice=20.00 # we force defshipping for all items below 20 regardless of pksize (pksize is either 1 or 2)
lowPrice=15.00 # we force defshipping for all items below 15 effective 1/4/22
highPrice=800.00 # we are turning on only items below this price for initial selling
DefShipFee=10.95
##shipFeePct=0.25
shipFeePct=0.35 # effective 1/4/22
#
#p = open('KHDPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
L = open('BZChng.txt', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/BZ_SKU_MASTER.txt', 'r') as rf: # created from All listing matching BZ-
     reader = csv.reader(rf, delimiter='\t')
     with open('BZQty.csv', 'w') as wf:   # file for preparing xml to upload to amzn mws
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in amzn sku list w/prefix
              titleIn=line[2] # title needed for determining packsize
              priceIn=line[3] # price listed
              qtyIn=line[4] # qty listed
              priceInF=float(priceIn)
              pkSize=1
              qtyI=int(qtyIn) # listed qty integer
              #determine pksize based on title
              pkSize=1
              #if pack2Str in titleIn:
              #    pack2Ctr +=1
              #    pkSize=2
              found=0
              #print('sku= ',line[0])
              with open('BZDailyCat.csv', 'r') as f:   # vendor data from filezilla or ftp 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuBZ=prefix+line[0] # vendor sku
                    qtyBZ=line[1] #
                    ####################################################
                    if skuBZ == skuIn:
                        found=1  # our sku list item matches vendor feed
                        ## validate qty 
                        try:
                            int(qtyBZ)
                        except ValueError:
                            print(skuBZ,"invalid qty data..skiping..",qtyBZ)
                            break
                        qtyBZI=int(qtyBZ)
                        ############ DETERMINE price is within allowed price ###########
                        if priceInF > highPrice:
                            #print("price is high... skipping",priceIn)
                            highPCtr +=1 
                            found=0 # make it appear as not found so will set to 0 in case it is on
                            break  # skip to next record
                        #################### DETERMINE QTY on or OFF ######################
                        if qtyI == 0 and qtyBZI > minQty:
                            qtyOut=1  # turn on 
                            qChngCtrOn +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                            # provide report of items being turned on only for review
                            priceLog=skuBZ+"\t"+titleIn+"\t"+str(priceInF)+"\n"
                            L.write(priceLog)  # for auditing and reference only

                        if qtyI > 0 and qtyBZI <= minQty:
                            qtyOut=0  # turn off
                            qChngCtrOff +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                        ###########################################################################################
                        # Price maintained manually - Only qty updates 
                        ############################################################################################
                        #shipFee=DefShipFee  # assume default
                        # recalc shipfee if it will be different than default fee
                        #ourCost=(priceUPC*pkSize) # price of unit for pkSize Units
                        #ourCost2Ship=(ourCost*shipFeePct) # shipping cost
                        #if ourCost2Ship > DefShipFee:
                        #    shipFee=ourCost2Ship
                        ##take the higher shipping cost unless item unit price is < lowPrice ($20)
                        #if priceUPC <= lowPrice:
                        #    shipFee=DefShipFee  # force default ship fee for low price items regardless of pksize
                        #################################################################################################
                        # Compute Final cost with shipping and markup
                        #################################################################################################
                        #totalCost=ourCost+shipFee # with shipping
                        #markUp=(totalCost*markupPct) # markup amount on cost of product + shipping
                        #finalCost=(totalCost+markUp) #  add on markup value
                        #priceV=round(finalCost,2)
                        #if priceinF != priceV: 
                        #    priceData=skuIn+","+str(priceV)+"\n"
                        #    p.write(priceData)  # for bash processing to push to mkt channels
                        #    # to track the price changes
                        #    pChngCtr +=1 
                        #    priceLog=skuIn+" Listed Price= "+str(priceinF)+" newPrice= "+str(priceV)+" pkSize= "+str(pkSize)+" UnitP= "+unitCoststr+"\n"
                        #    L.write(priceLog)  # for auditing and reference only
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
              ## loop continues here at break <<<<<-----<<<<<
#dump to change log instead of print

#priceLog="Total Items Price Changed = "+str(pChngCtr)+"\n"
#L.write(priceLog)  # for auditing and reference only
priceLog="Total Items Activated  = "+str(qChngCtrOn)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items DeActivated = "+str(qChngCtrOff)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items in AMZN SKU LIST = "+str(recCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items skipped for High Price = "+str(highPCtr)+" Price "+str(highPrice)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Quantity minimum  = "+str(minQty)+"\n"
L.write(priceLog)  # for auditing and reference only
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
#p.close()
L.close()
