# copied wlmt upd module and modified for amzn 1-5-22
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
# prep raw update files - later formated to xmls to upload to mkt channels
#Revisions
##
import csv
import io
i=0
minQty=10  # 
defQty=2  # to turn on 
markupPct=0.40  # we cancalc our own markup wmt is slighly lower
prefix="LM-"
pack2Str="Pack of 2"
pack2Ctr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
DefShipFee=11.99
rStr="Restricted"
#
M = open('LemQmon.csv', 'w')  # active items with qty to monitor
R = open('LemRest.csv', 'w')  # to delete later items restricted in wlmt
#
p = open('LEMPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
N = open('LM_WLMT_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
L = open('LMChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/LM_WLMT_SKU_MASTER.csv', 'r') as rf: # our wlmt csv file built from API we rereate new to keep functionlaity
     reader = csv.reader(rf, delimiter=',')
     with open('LEMQty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w/o prefix, our sku master does not have prefix either
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
              if pkSizeI > 2:  # count items with pksize more than 2 
                  pack2Ctr +=1
              #print('sku= ',line[0])
              with open('LEMQtyPrc.csv', 'r') as f:   # custom vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuLEM=line[0] # item Number in lemar
                    qtyLEM=line[1] #1
                    qtyLEMI=int(qtyLEM)
                    priceLEMstr=line[2] # vendor unit price
                    priceUPC=float(priceLEMstr) # vendor unit price w/out any shipping
                    wlmtRest=line[4] # wlmt Restricted?
                    ####################################################
                    if skuLEM == skuIn:
                        found=1  # our sku list item matches vendor feed
                        if wlmtRest == rStr:
                            resStr=(prefix+skuIn+"\n")
                            R.write(resStr)
                        #################### DETERMINE QTY on or OFF ######################
                        qtyL=qtyLEMI/pkSizeI
                        if qtyL <= 0:
                            qtyL=0
                        # track in qmon to check qty
                        if qtyL >= minQty:
                            qtyMon=(minQty*pkSizeI)
                            monStr=(skuIn+","+str(qtyMon)+"\n")
                            M.write(monStr)
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
                        # Determine/calculate shipping for KHD 
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
                            priceData=prefix+skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            chngLog=prefix+skuIn+" Listed Price= "+str(priceinF)+" newPrice= "+str(priceV)+" pkSize= "+str(pkSize)+" UnitP= "+priceLEMstr+"\n"
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
              newStr=(skuIn+","+itemId+","+priceOut+","+qtyOutstr+","+gtinIn+","+pkSize+"\n") # new file
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
M.close()
N.close()
R.close()
#################################-----------------END----------------------###################
