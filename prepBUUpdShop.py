# BU shop updates 3/12/22
#
# single module to prep price and qty files used to upload to shopify
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
##
import csv
import io
i=0
notStkd="not stocked"
minQty=10  # 
defQty=1  # to turn on 
markupPct=0.38  # we cancalc our own markup wmt is slighly lower
prefix="BU-"
pack2Str="Pack of 2"
pack3Str="Pack of 3"
pack4Str="Pack of 4"
pack2Ctr=0 # multipack counter for all except 1
recCtr=0 # in sku list counter
pChngCtr=0 # items changing price in this run
qChngCtrOn=0 # items changing from qty=0 to qty=1 turning on
qChngCtrOff=0 # items changing from qty=1 to qty=0 turning off due to not founds
DefShipFee=11.99
com=","
sem=";"
#rStr="Restricted"
#
#M = open('LemQmon.csv', 'w')  # active items with qty to monitor
p = open('BUUpdPrcShop.csv', 'w')  # once items we want is located in our SKU LIST
L = open('ShopBUChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
header=["Handle","Title","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","SKU","HS Code","COO","Location","Oberlo"]
#
headerP=("Handle,"+"Title,"+"Variant Price\n") 
#
p.write(headerP)
#
N = open('BU_SHOP_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/BU_SHOP_SKU_MASTER.csv', 'r') as rf: # our shop inventory file
     reader = csv.reader(rf, delimiter=',')
     with open('BUUpdQtyShop.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w prefix,need to strip to compare with vendor file
              skuInx=skuIn[3:] #strip prefix
              #print("skuinx",skuInx)
              titleIn=line[1]  # take title as is from sku master (fixed with initial load)
              #titleInX=line[1]  # only 2 columns info needed , has other cols for shop updates 
              #titleIn=titleInX.replace(com,sem) # patch title and change comma to semicolon
              #
              qtyIn=line[11]
              # line[12] last colum where we can store price
              priceIn=line[12]  # initial file has "not stocked" and if it was reset again
              if priceIn == notStkd:
                  priceIn="0.0"
              try:
                  float(priceIn)
              except ValueError:
                  print(skuIn,"PriceIn data error reset to 99999.99 ",priceIn)
                  priceIn="99999.99"  # this will force recompute price later on
              priceinF=float(priceIn)
              #priceOut=str(priceinF)
              skuOut=skuIn.upper() # same as handle in upper
              qtyI=int(qtyIn) # listed qty integer
              qtyOutstr=qtyIn
              found=0
              # we may want to create exception sku list for restricted here so wlmtdel can process it
              #determine pksize based on title
              #print('sku= ',line[0])
              ##with open('mws/data/LeeMarPet.com_Inventory.csv', 'r') as f:   # vendor data for initial title cleanup
              with open('BUQtyPrc.csv', 'r') as f:   # custom vendor data for daily monitoring
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuBU=line[0] # sku without prefix
                    qtyBU=line[2] #1
                    qtyBUI=int(qtyBU)
                    priceBUstr=line[3] # vendor unit price with shipping cost
                    priceUPC=float(priceBUstr) # vendor unit price w shipping
                    #productSizeX=line[19] # to append to item title only if reading original vendor data
                    #productSize=productSizeX.replace(com,sem) # patch title and change comma to semicolon
                    ####################################################
                    if skuBU.lower() == skuInx.lower(): # itemnumber comparison 
                        #print("skuLem",skuLEM)
                        found=1  # our sku list item matches vendor feed
                        #######################  make it multipack based on price ###################
                        pkSizeI=1 # defaut
                        #titleIn=titleIn+" "+productSize
                        #price=priceUPC  # for pksize determination
                        #if pack2Str.lower() in titleIn.lower():
                        #    pkSizeI = 2
                        #elif pack3Str.lower() in titleIn.lower():
                        #    pkSizeI=3
                        #elif pack4Str.lower() in titleIn.lower():
                        #    pkSizeI=4
                        #if price <= 5.00:
                        #    pkSizeI = 4
                        #elif price <= 10:
                        #    pkSizeI=3
                        #elif price <= 20.00:
                        #    pkSizeI = 2
                        # change title to indicate pksize 
                        if pkSizeI > 1:
                            #titleIn="[Pack of "+str(pkSizeI)+"] - "+titleIn  # title already has correct pksize in it
                            pack2Ctr +=1  # multipack count
                        #else:
                        #    itemTx =  itemT
                        #############################################################################
                        #################### DETERMINE QTY on or OFF ######################
                        #qtyL=qtyLEMI/pkSizeI
                        #if qtyL <= 0:
                        #    qtyL=0
                        # track in qmon to check qty
                        #if qtyL >= minQty:
                        #    qtyMon=(minQty*pkSizeI)
                            #monStr=(skuIn+","+str(qtyMon)+"\n")
                            #M.write(monStr)
                            #
                        if qtyI == 0 and qtyBUI >= minQty:
                            qtyOut=defQty  # turn on 
                            qtyOutstr=str(qtyOut)
                            qChngCtrOn +=1 
                            lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                            #lines=[prefix+skuIn,qtyOut]
                            writer.writerow(lines)
                            qtyOutstr=str(qtyOut) # carry to new file
                        if qtyI > 0 and qtyBUI < minQty:
                            qtyOut=0  # turn off
                            qtyOutstr=str(qtyOut)
                            qChngCtrOff +=1 
                            lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                            #lines=[prefix+skuIn,qtyOut]
                            writer.writerow(lines)
                        #############################################################################
                        # Determine/calculate shipping for LM Shop
                        ############################################################################################
                        #shipFee=DefShipFee  # ship fee included in UPC
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
                        totalCost=ourCost
                        markUp=(totalCost*markupPct) # markup amount on cost of product + shipping
                        finalCost=(totalCost+markUp) #  add on markup value
                        priceV=round(finalCost,2)
                        priceOut=str(priceV) # we need this to build our new file
                        if priceinF != priceV: 
                            priceData=(skuIn+","+titleIn+","+priceOut+"\n")
                            p.write(priceData)
                            # to track the price changes
                            pChngCtr +=1 
                            chngLog=skuIn+" Listed Price= "+str(priceinF)+" newPrice= "+str(priceV)+" pkSize= "+str(pkSizeI)+" UnitP= "+priceOut+"\n"
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
                      lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                      #lines=[prefix+skuIn,qtyOut]
                      writer.writerow(lines)
#
              # Regardless of previous logic we just recreate our .new file
              #priceIn=line[2] # price listed
              #priceIn=line[2] # price listed
              #newStr=(skuIn,itemId,priceOut,qtyOut,gtinIn,pkSize)
              ##newStr=(skuIn+","+titleIn+","+priceOut+","+qtyOutstr+","+gtinIn+","+pkSize+"\n") # new file
              newStr=(skuIn+","+titleIn+","+"Title"+","+"Default Title"+","+","+","+","+","+skuOut+","+","+","+qtyOutstr+","+priceOut+"\n")
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
chngLog="Total Items with PkSize more than 1(multipack) in SKU LIST = "+str(pack2Ctr)+"\n"
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
