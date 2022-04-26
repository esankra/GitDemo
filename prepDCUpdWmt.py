## 12-30-21 modified to analyze skuIn to determine which col in vendor file it should be matched
# copied amzn module and customized for wmt 12-11-21
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
markupPct=0.40  # we cancalc our own markup wmt is slighly lower
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
N = open('DC_WLMT_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
L = open('DCChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/DC_WLMT_SKU_MASTER.csv', 'r') as rf: # our wlmt csv file built from API we rereate new to keep functionlaity
     reader = csv.reader(rf, delimiter=',')
     with open('DCQty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w/o prefix, our sku master does not have prefix either
              #################################################################################
              # analyze the sku in to see which column on vendor input it should be matched with 
              #a=skuIn[3:] # strip prefix to get the number parts if they are indded number
              a=skuIn # for wlmt no need to strip prefix input has no prefix
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
              itemId=line[1] # we read all 6 col so we can recreate the new file for next run
              priceIn=line[2] # price listed
              qtyIn=line[3] # qty listed
              priceinF=float(priceIn)
              gtinIn=line[4]  # our GTI assigned to wlmt during initial load
              pkSize=line[5] # we keep pksize from sku list when rebuilding the csv from API
              pkSizeI=int(pkSize) # listed pksize  integer
              qtyI=int(qtyIn) # listed qty integer
              qtyOutstr=qtyIn
              #determine pksize based on title
              if pkSizeI == 2:
                  pack2Ctr +=1
              found=0
              #print('sku= ',line[0])
              with open('DCQtyPrc.csv', 'r') as f:   # custom vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuDC1=line[0] # pid
                    skuDC2=line[1] # cold 2 in our dcqtyprc custom made file
                    unitCoststr=line[2] # already marked up price at 42%
                    priceUCF=float(unitCoststr) 
                    qtyDC=line[3] #1
                    priceDCstr=line[4] # vendor unit price
                    priceUPC=float(priceDCstr) # vendor unit price w/out any shipping
                    ####################################################
                    ######################################################################
                    # assign correct skuDC to match for the current record based on useCol
                    skuDC=skuDC2  # use col 3 vendor sku as default
                    if useCol == 1:
                        skuDC=skuDC1  # chang to use DC1
                    #######################################################################
                    if skuDC == skuIn:
                    #if skuDC1 == skuIn or skuDC2 == skuIn:
                        found=1  # our sku list item matches vendor feed
                        if qtyI == 0:
                            qtyOut=1  # turn on 
                            qtyOutstr=str(qtyOut) 
                            qChngCtrOn +=1 
                            lines=[prefix+skuIn,qtyOut]
                            writer.writerow(lines)
                        #priceV = (priceUCF*pkSize) # use this or calc from UPC unit price
                        # recalc price here at different markup if needed
                        ourCost=(priceUPC*pkSizeI) # price of unit for pkSize Units
                        markUp=(ourCost*markupPct)
                        totalCost=(ourCost+markUp) #  add on markup value
                        priceV=round(totalCost,2)
                        priceOut=str(priceV) # we need this to build our new file
                        if priceinF != priceV: 
                            priceData=prefix+skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            priceLog=prefix+skuIn+" Price Listed= "+str(priceinF)+" newPrice= "+str(priceV)+"\n"
                            L.write(priceLog)  # for auditing and reference only
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
N.close()
