# BBD processing - use single AMZN SKU LIST to find changes to price and qty 12-14-21
# Author : Sankar Ramaiah
# 12-14-21 - modify to add chng log so we can see what changed each week when vendor sheet comes
import csv
import io
i=0
prefix="BD-"
pack2Ctr=0 # 
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
#
p = open('bbdPrc.csv', 'w')  # once items we want is located in our SKU LIST
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
L = open('BDChng.log', 'w')  # track items with price changes & qty showing old new pirce
#
with open('mws/data/BD_AMZN_SKU_LIST.txt', 'r') as rf: # generated from AllListing report
     reader = csv.reader(rf, delimiter='\t')
     with open('bbdQty.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              #sku=line[0]
              skuIn=line[0] # sku in amzn sku list w/prefix
              titleIn=line[2] # title needed for determining packsize
              priceIn=line[3] # price listed
              qtyIn=line[4] # qty listed
              priceinF=float(priceIn)
              pkSize=1 # not present in AMZN sku list
              qtyI=int(qtyIn) # listed qty integer
              found=0
              #print('sku= ',line[0])
              with open('bbdQtyPrc.csv', 'r') as f:   # sku,price and qty (0/1)
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    skuBD=line[0]
                    if skuBD == skuIn: # with prefix fom custom vendor qtyprc file 
                        found=1
                        ############### qty changed ?? ################
                        priceBDstr=line[1]
                        priceV=float(priceBDstr) # compare this with listed price
                        qtyBDstr=line[2]
                        qtyBDI=int(qtyBDstr)
                        if qtyI == 0 and qtyBDI > 0:
                            qtyOut=1 #turn ON
                            qChngCtrOn +=1
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                        if qtyI == 1 and qtyBDI == 0:
                            qtyOut=0 #turn off
                            qChngCtrOff +=1
                            lines=[skuIn,qtyOut]
                            writer.writerow(lines)
                        ################## PRICE changed ?? ###################
                        if priceinF != priceV: 
                            priceData=skuIn+","+str(priceV)+"\n"
                            p.write(priceData)  # for bash processing to push to mkt channels
                            # to track the price changes
                            pChngCtr +=1 
                            priceLog=skuIn+" Price Listed= "+str(priceinF)+" newPrice= "+str(priceV)+"\n"
                            L.write(priceLog)  # for auditing and reference only
                        break
#
              recCtr +=1
              if found == 0:
                  if qtyI == 1:
                      qtyOut=0
                      qChngCtrOff +=1
                      lines=[skuIn,qtyOut]
                      writer.writerow(lines)

#
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
# close all files
rf.close()
wf.close()
p.close()
L.close()
