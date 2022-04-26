# BB2 daily qty price monitoring - 4/5/22
# Author : Sankar Ramaiah
#Revisions
import csv
import io
i=0
minQty=10  # 
defQty=1  # to turn on 
markupPct=0.40  # we cancalc our own markup wmt is slighly lower
prefix="BB2-"
pack2Str="Pack of 2"
pack2Ctr=0
recCtr=0 # in sku list counter
FoundCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
DefShipFee=19.95
#
#
p = open('BB2Prc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
N = open('BB2_WLMT_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
L = open('BB2Chng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/BB2_WLMT_SKU_MASTER.csv', 'r') as rf: # our wlmt csv file built from API we rereate new to keep functionlaity
     reader = csv.reader(rf, delimiter=',')
     with open('BB2Qty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuInX=line[0] # sku in sku list w prefix, our sku master have prefix 
              skuIn=skuInX[4:]  # strip BB2-
              #print(skuIn,skuInX)
              itemId=line[1] # we read all 6 col so we can recreate the new file for next run
              priceIn=line[2] # price listed
              qtyIn=line[3] # qty listed
              priceinF=float(priceIn)
              gtinIn=line[4]  # our GTI assigned to wlmt during initial load
              pkSize=line[5] # we keep pksize from sku list when rebuilding the csv from API
              pkSizeI=int(pkSize) # listed pksize  integer for LM it can be 3,4 10 11 etc
              qtyI=int(qtyIn) # listed qty integer
              qtyOutstr=qtyIn
              found=0
              # we may want to create exception sku list for restricted here so wlmtdel can process it
              #determine pksize based on title
              if pkSizeI > 1:  # count items with pksize more than 1 
                  pack2Ctr +=1
              #print('sku= ',line[0])
              with open('BrybellyCatalog.csv', 'r') as f:   # Original vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuBB=line[0] # sku in vendor feed no prefix here
                    #print(skuBB)
                    qtyBB=line[2] #1
                    pricestr=line[4] # vendor unit price
                    # validate price and qty on error set qtyBB =0
                    try:
                        int(qtyBB)
                    except ValueError:
                        qtyBB=0 # this will force qty to be set 0 if sku match found
                    try:
                        float(pricestr)
                    except ValueError:
                        pricestr="9999.99"
                        qtyBB=0 # this will force qty to be set 0 if sku match found
                        #continue # will force qty to be set to 0 for this row
                    qtyBBI=int(qtyBB)
                    priceUPC=float(pricestr) # vendor unit price w/out any shipping
                    ####################################################
                    if skuBB == skuIn:
                        found=1  # our sku list item matches vendor feed
                        FoundCtr +=1 
                        #################### DETERMINE QTY on or OFF ######################
                        qtyL=qtyBBI/pkSizeI
                        if qtyL <= 0:
                            qtyL=0
                        # track in qmon to check qty
                        #if qtyL >= minQty:
                        #    qtyMon=(minQty*pkSizeI)
                        #    monStr=(skuIn+","+str(qtyMon)+"\n")
                        #    M.write(monStr)
                            #
                        if qtyI == 0 and qtyL >= minQty:
                            qtyOut=defQty  # turn on 
                            qChngCtrOn +=1 
                            lines=[prefix+skuIn,qtyOut]
                            writer.writerow(lines)
                            qtyOutstr=str(qtyOut) # carry to new file
                        if qtyI > 0 and qtyL <= minQty:
                            qtyOut=0  # turn off
                            qChngCtrOff +=1 
                            lines=[prefix+skuIn,qtyOut]
                            writer.writerow(lines)
                            qtyOutstr=str(qtyOut) # carry to new file
                        #############################################################################
                        # Determine/calculate price
                        ############################################################################################
                        shipFee=DefShipFee  # assume default
                        # recalc shipfee if it will be different than default fee
                        ourCost=(priceUPC*pkSizeI) # base cost
                        #ourCost2Ship=(ourCost*shipFeePct) # shipping cost
                        #if ourCost2Ship > DefShipFee:
                        #    shipFee=ourCost2Ship
                        #take the higher shipping cost unless item unit price is < lowPrice ($20)
                        #if priceUPC <= lowPrice:
                        #    shipFee=DefShipFee  # force default ship fee for low price items regardless of pksize
                        #################################################################################################
                        # Compute Final cost with shipping and markup
                        #################################################################################################
                        totalCost=ourCost+shipFee # with shipping
                        markUp=(totalCost*markupPct) # markup amount on cost of product + shipping
                        finalCost=(totalCost+markUp) #  add on markup value
                        # add padding to adjust price - custom pricing 
                        if finalCost <=40:
                            finalCost=finalCost+4
                        else:
                            if finalCost <=50:
                                finalCost=finalCost+3
                            else:
                                finalCost=finalCost+2
                        #########
                        priceV=round(finalCost,2)
                        priceOut=str(priceV) # we need this to build our new file
                        if priceV > priceinF:   # price computed is greater than current listed price then upate it
                            priceData=prefix+skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            chngLog=prefix+skuIn+" Listed Price= "+str(priceinF)+" newPrice= "+str(priceV)+" pkSize= "+str(pkSize)+" UnitP= "+pricestr+"\n"
                            L.write(chngLog)  # for auditing and reference only
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  priceOut=priceIn  # since item not found price should be carried over from input sku master
                  if qtyI == 1:
                      qtyOut=0  # turn OFF
                      qtyOutstr=str(qtyOut) 
                      qChngCtrOff +=1 
                      lines=[prefix+skuIn,qtyOut]
                      writer.writerow(lines)
#
              # Regardless of previous logic we just recreate our .new file
              #priceIn=line[2] # price listed
              #priceIn=line[2] # price listed
              #newStr=(skuIn,itemId,priceOut,qtyOut,gtinIn,pkSize)
              newStr=(prefix+skuIn+","+itemId+","+priceOut+","+qtyOutstr+","+gtinIn+","+pkSize+"\n") # new file
              N.write(newStr)

#dump to change log instead of print

chngLog="Total Items Price Changed = "+str(pChngCtr)+"\n"
L.write(chngLog)  # for auditing and reference only
chngLog="Total Items Activated  = "+str(qChngCtrOn)+"\n"
L.write(chngLog)  # for auditing and reference only
chngLog="Total Items DeActivated = "+str(qChngCtrOff)+"\n"
L.write(chngLog)  # for auditing and reference only
chngLog="Total Items in SKU LIST = "+str(recCtr)+"\n"
L.write(chngLog)  # for auditing and reference only
chngLog="Total Items with PkSize more than 2 in SKU LIST = "+str(pack2Ctr)+"\n"
L.write(chngLog)  # for auditing and reference only
chngLog="Total Items found in vendor feed= "+str(FoundCtr)+"\n"
L.write(chngLog)  # for auditing and reference only
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
p.close()
L.close()
N.close()
#################################-----------------END----------------------###################
