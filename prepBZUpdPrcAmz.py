# 1-21-22 - BEnzara AMZN Price updates 3/26/22 
# Author : Sankar Ramaiah
# reads auto created BZ list and finds each item in manually provided price list and prepares price update file
#
### IMPORTANT NOTE: this module is invoked on demand using the price file manually maintained. after running this module 
#### run this command ./prepAmznPrcUpd.sh BZPrc.csv to prepare the xml for amazon price update and run exec upd script final step
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
prcCtr=0 # in sku list counter
notFoundCtr=0 # items not found in price file
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
L = open('BZChngPrc.txt', 'w')  # track items with price changes & qty showing old new pirce
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/BZ_SKU_MASTER.txt', 'r') as rf: # created from All listing matching BZ-
     reader = csv.reader(rf, delimiter='\t')
     with open('BZPrc.csv', 'w') as wf:   # file for preparing xml to upload to amzn mws
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
              with open('BZ-PRICEUPDATE-3-24-22.csv', 'r') as f:   # manually prepared price file in shopify upload format
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuBZ=line[0] # vendor sku
                    prcBZ=line[2] #
                    ####################################################
                    if skuBZ == skuIn:
                        found=1  # our sku list item matches vendor feed
                        ## validate qty 
                        try:
                            float(prcBZ)
                        except ValueError:
                            print(skuBZ,"invalid price data..skiping..",prcBZ)
                            break
                        prcBZF=float(prcBZ)
                        # smiply write out a price update file 
                        if priceInF != prcBZF:
                            #
                            print(skuBZ,"Price needs updating...Current Price= ",priceIn,"New Price= ",prcBZ)
                            prcCtr +=1  # number of items price updated
                            lines=[skuIn,prcBZF]
                            writer.writerow(lines)
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  notFoundCtr +=1
                  print(skuIn,"SKU not found in price file.")
              ## loop continues here at break <<<<<-----<<<<<
#dump to change log instead of print

#priceLog="Total Items Price Changed = "+str(pChngCtr)+"\n"
#L.write(priceLog)  # for auditing and reference only
priceLog="Total Items in AMZN SKU LIST = "+str(recCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items price updated  = "+str(prcCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
priceLog="Total Items Not found in Price File = "+str(notFoundCtr)+"\n"
L.write(priceLog)  # for auditing and reference only
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
print("*********************************************************************************************")
print("*** Execute command to complete updates *** ./prepAmznPrcUpd.sh BZPrc.csv to prepare the xml")
print("*********************************************************************************************")
rf.close()
wf.close()
#p.close()
L.close()
