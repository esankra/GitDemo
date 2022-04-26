#  Update EBAY daily job
#Revisions
import csv
import io
i=0
defQty=1  # to turn on 
pkSizeI=1  # 
markupPct=0.38  # we calc our own markup 
prefix="dc-"  # shop handle
prefix2="DC-"  # real diecast sku (col 3 in diecast)
pk2Str="Pack of 2"
notFoundStr="NOT FOUND" # title issue
pack2Ctr=0
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
DefShipFee=0.00
com=","
sem=";"
#
#
p = open('DCUpdPrcEbay.csv', 'w')  # price file
#
#N = open('hr_BNZ_SKU_MASTER.new', 'w')  # bnz not keeping local copyies 
L = open('EbayDCChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
N = open('DC_EBAY_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful
#SKU,Channel ID,List Price,Total Ship to Home Quantity
header=["SKU","Channel ID","List Price","Total Ship to Home Quantity"]
#
headerP=("SKU,"+"Channel ID,"+"List Price,"+"Total Ship to Home Quantity\n") 
#
p.write(headerP)
#
with open('mws/data/DC_EBAY_SKU_MASTER.csv', 'r') as rf: # manual list (can recreate from MIP report)
     reader = csv.reader(rf, delimiter=',')
     with open('DCUpdQtyEbay.csv', 'w') as wf:  # just qty file
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header) # ebay MIP header
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w prefix,need to strip to compare with vendor file
              skuInx=skuIn[3:] #strip prefix
              titleIn=line[1]  # only 2 columns info needed , has other cols for shop updates 
              qtyIn=line[2]
              try:
                  qtyInI=int(qtyIn)
              except ValueError:
                  print(qtyIn,"Invalid qty.. skip row..")
                  continue
              qtyI=int(qtyIn)
              qtyOutstr=qtyIn
              priceIn=line[3]
              priceinF=float(priceIn)
              #titleIn=titleInX.replace(com,sem) # may not need for ebay - patch title and change comma to semicolon
              found=0
              ###############  determine pack size from title ############
              pkSizeI=1
              if pk2Str.lower() in titleIn.lower():
                  pack2Ctr+=1
                  pkSizeI=2
              # 
              with open('DCQtyPrcEbay.csv', 'r') as f:   # custom vendor data prepared by python common module
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuDC1=prefix+line[0] # pid
                    skuDC2=prefix2+line[1] # col 2 in our dcqtyprc custom made file
                    unitCoststr=line[2] # already marked up price 
                    priceUCF=float(unitCoststr) 
                    qtyDC=line[3] #1
                    priceDCstr=line[4] # vendor unit price
                    priceUPC=float(priceDCstr) # vendor unit price w/out any shipping
                    ######################################################################
                    # assign correct skuDC to match for the current record based on useCol
                    skuDC=skuDC2  # use col 3 vendor sku as default
                    #######################################################################
                    if skuDC == skuIn:
                        found=1  # our sku list item matches vendor feed
                        if qtyI == 0:
                            qtyOut=1  # turn on 
                            qtyOutstr=str(qtyOut) 
                            qChngCtrOn +=1 
                            lines=[skuIn,"EBAY_US","",qtyOut]
                            writer.writerow(lines)
                        #priceV = (priceUCF*pkSize) # use this or calc from UPC unit price
                        # recalc price here at different markup if needed
                        ourCost=(priceUPC*pkSizeI) # price of unit for pkSize Units
                        markUp=(ourCost*markupPct)
                        totalCost=(ourCost+markUp) #  add on markup value
                        priceV=round(totalCost,2)
                        priceOut=str(priceV) # we need this to build our new file
                        if priceinF != priceV: 
                            priceData=skuIn+","+"EBAY_US"+","+str(priceV)+","+qtyOutstr+"\n"
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
                  priceOut=priceIn  # since item not found price should be carried over from input sku master
                  if qtyI == 1:
                      qtyOut=0  # turn OFF
                      qtyOutstr=str(qtyOut) 
                      qChngCtrOff +=1 
                      #lines=[skuIn,"EBAY_US",,qtyOut]
                      lines=[skuIn,"EBAY_US","",qtyOut]
                      writer.writerow(lines)
#
              # Regardless of previous logic we just recreate our .new file
              #priceIn=line[2] # price listed
              #priceIn=line[2] # price listed
              #newStr=(skuIn,itemId,priceOut,qtyOut,gtinIn,pkSize)
              newStr=(skuIn+","+titleIn+","+qtyOutstr+","+priceOut+"\n") # new file
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
