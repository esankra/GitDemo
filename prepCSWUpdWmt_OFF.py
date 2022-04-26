# set all to 0 - turn everything for cswy to 0 off - used to emporarily halt selling csw items 3-20-22
# WLMT CSWY update price qty
# uses preprocessor python which prepares CWQtyPrc.csv used by shopify modules
# Author : Sankar Ramaiah
# 2-5-22 - initial creation 
# Notes: run in VM1 , uses same 6 col csv catalog built by wlmt api, last col is Not pack size for this moduel, it is flag
# set to 1 means process 0 in this column we skip that item from turning on.
#Revisions
import csv
import io
i=0
minQty=50  # 3/8/22 - nancy said 50 sometime means 0 !!!
defQty=1  # to turn on 
markupPct=0.40  # we cancalc our own markup wmt is slighly lower
prefix="CSW-"
pack2Str="Pack of 2"
pack2Ctr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
DefShipFee=0.00
rStr="Restricted"
listOff=0
listOn=1
#
#M = open('LemQmon.csv', 'w')  # active items with qty to monitor
#R = open('LemRest.csv', 'w')  # to delete later items restricted in wlmt
#
p = open('CSWPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
N = open('CSW_WLMT_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
L = open('CSWChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/CSW_WLMT_SKU_MASTER.csv', 'r') as rf: # our wlmt csv file built from API we rereate new to keep functionlaity
     reader = csv.reader(rf, delimiter=',')
     with open('CSWQty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku w prefix
              itemId=line[1] # we read all 6 col so we can recreate the new file for next run
              priceIn=line[2] # price listed
              qtyIn=line[3] # qty listed
              priceinF=float(priceIn)
              gtinIn=line[4]  # our GTI assigned to wlmt during initial load
              ##pkSize=line[5] # we keep pksize from sku list when rebuilding the csv from API
              listFl=line[5] # if set to 0 we set qty =0 for this listing if it is not already 0
              listFlI=int(listFl) # 
              qtyI=int(qtyIn) # listed qty integer
              qtyOutstr=qtyIn
              found=0
              pkSizeI=1 # all csw items are single pack without any exceptions!!
              # we may want to create exception sku list for restricted here so wlmtdel can process it
              #determine pksize based on title
              #if pkSizeI > 2:  # count items with pksize more than 2 
              #    pack2Ctr +=1
              #print('sku= ',line[0])
              with open('CWQtyPrc.csv', 'r') as f:   # custom vendor data prepared and shared by shop and wlmt common
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuCSW=prefix+line[0].upper() # sku stored in lower case due to shop handle and add prefix
                    qtyCSW=line[1] # vendor qty
                    qtyCSWI=int(qtyCSW)
                    priceCSWstr=line[2] # vendor unit price
                    priceUPC=float(priceCSWstr) # vendor unit price w/out any shipping
                    #wlmtRest=line[4] # wlmt Restricted?
                    ####################################################
                    if skuCSW == skuIn:
                        found=1  # our sku list item matches vendor feed
                        #if listFlI == listOff:  # listing is off 
                            # listing should not be activated so we set qty to 0
                        qtyCSWI=0  # force ty to 0 unconditionally for all items we have listed 3/20/22 - price changes kept
                        qtyOut=0  # turn off
                        qChngCtrOff +=1 
                        lines=[skuIn,qtyOut]
                        writer.writerow(lines)
                        qtyOutstr=str(qtyOut) # carry to new file
                            #resStr=(prefix+skuIn+"\n")
                            #R.write(resStr)
                        #################### DETERMINE QTY on or OFF ######################
                        #qtyL=qtyLEMI/pkSizeI
                        #if qtyL <= 0:
                        #    qtyL=0
                        # track in qmon to check qty
                        #if qtyL >= minQty:
                        #    qtyMon=(minQty*pkSizeI)
                        #    monStr=(skuIn+","+str(qtyMon)+"\n")
                        #    M.write(monStr)
                            #
                        #if qtyI == 0 and qtyCSWI > minQty:
                        #    qtyOut=defQty  # turn on 
                        #    qChngCtrOn +=1 
                        #    lines=[skuIn,qtyOut]
                        #    writer.writerow(lines)
                        #    qtyOutstr=str(qtyOut) # carry to new file
                        #if qtyI > 0 and qtyCSWI <= minQty:
                        #    qtyOut=0  # turn off
                        #    qChngCtrOff +=1 
                        #    lines=[skuIn,qtyOut]
                        #    writer.writerow(lines)
                        #    qtyOutstr=str(qtyOut) # carry to new file
                        #############################################################################
                        # Determine/calculate shipping 
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
                        priceV=round(finalCost,2)
                        priceOut=str(priceV) # we need this to build our new file
                        if priceinF != priceV: 
                            priceData=skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            chngLog=skuIn+" Listed Price= "+str(priceinF)+" newPrice= "+str(priceV)+" pkSize= "+str(pkSizeI)+" UnitP= "+priceCSWstr+"\n"
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
              newStr=(skuIn+","+itemId+","+priceOut+","+qtyOutstr+","+gtinIn+","+str(listFlI)+"\n") # new file
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
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
p.close()
L.close()
#M.close()
N.close()
#R.close()
#################################-----------------END----------------------###################
