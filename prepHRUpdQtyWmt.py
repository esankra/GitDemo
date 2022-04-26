# copied from LM WLMT python modules
# single module to prep price and qty files used to upload to wlmt and amzn
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
# 12-13-21 - prep raw update files - later formated to xmls to upload to mkt channels
#Revisions
##  JUST prepare QTY updates for HR to upload to wlmt using price and inventory file instead of full sheet
import csv
import io
i=0
maxLeadT=5
minQty=25  # 
defQty=1  # to turn on 
markupPct=0.38  # we calc our own markup wmt is slighly lower
prefix="hr-"
pack2Str="Pack of 2"
pack2Ctr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
DefShipFee=0.00
#
#M = open('HrQmon.csv', 'w')  # active items with qty to monitor
#R = open('LemRest.csv', 'w')  # to delete later items restricted in wlmt
#
#p = open('HRPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
#N = open('hr_WLMT_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
#L = open('HRChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/hr_WLMT_SKU_MASTER.csv', 'r') as rf: # our wlmt csv file built from API we rereate new to keep functionlaity
     reader = csv.reader(rf, delimiter=',')
     with open('hrQty.csv', 'w') as wf:  # only qty updates done by this module
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w prefix,need to strip to compare with vendor file
              skuInx=skuIn[3:] #strip hr-
              itemId=line[1] # we read all 6 col so we can recreate the new file for next run
              priceIn=line[2] # price listed
              qtyIn=line[3] # qty listed
              priceinF=float(priceIn)
              gtinIn=line[4]  # our GTI assigned to wlmt during initial load
              pkSize=line[5] # we keep pksize from sku list when rebuilding the csv from API
              pkSizeI=int(pkSize) # listed pksize  integer for hr we only have 1 at this time
              qtyI=int(qtyIn) # listed qty integer
              qtyOutstr=qtyIn
              found=0
              # we may want to create exception sku list for restricted here so wlmtdel can process it
              #determine pksize based on title
              if pkSizeI > 2:  # count items with pksize more than 2 
                  pack2Ctr +=1
              #print('sku= ',line[0])
              with open('hrqtyFeed.txt', 'r') as f:   # price inventory feed from vendor
                readerV = csv.reader(f, delimiter='\t')
                for line in readerV:
                    ###################################################
                    skuHR=line[0] # item Number in lemar
                    qtyHR=line[1] #1
                    qtyHRI=int(qtyHR)
                    #priceHRstr=line[2] # vendor unit price
                    #priceUPC=float(priceHRstr) # vendor unit price w/out any shipping
                    #leadTIn=line[3] # leattime in vendor
                    #leadTI=int(leadTIn)
                    ####################################################
                    if skuHR == skuInx:  # compare skuin stripped without prefix
                        found=1  # our sku list item matches vendor feed
                        #################### DETERMINE QTY on or OFF ######################
                        if qtyI == 0 and qtyHRI >= minQty:
                            qtyOut=defQty  # turn on 
                            qChngCtrOn +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                            qtyOutstr=str(qtyOut) # carry to new file
                        if qtyI > 0 and qtyHRI < minQty:
                            qtyOut=0  # turn off
                            qChngCtrOff +=1 
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                            qtyOutstr=str(qtyOut) # carry to new file
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  if qtyI == 1:
                      qtyOut=0  # turn OFF
                      qtyOutstr=str(qtyOut) 
                      qChngCtrOff +=1 
                      lines=[skuIn,qtyOut]
                      writer.writerow(lines)
#
              # Regardless of previous logic we just recreate our .new file
              #priceIn=line[2] # price listed
              #priceIn=line[2] # price listed
              #newStr=(skuIn,itemId,priceOut,qtyOut,gtinIn,pkSize)

#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
#p.close()
#L.close()
#M.close()
#N.close()
#R.close()
#################################-----------------END----------------------###################
