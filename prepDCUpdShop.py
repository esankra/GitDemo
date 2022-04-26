#  Update Shopify for cars - full updates of price and qty applied via uploads 1-8-21
#Revisions
import csv
import io
i=0
defQty=1  # to turn on 
pkSizeI=1  # 
markupPct=0.40  # we calc our own markup wmt is slighly lower
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
#M = open('HrQmon.csv', 'w')  # active items with qty to monitor
#R = open('LemRest.csv', 'w')  # to delete later items restricted in wlmt
#
p = open('DCUpdPrcShop.csv', 'w')  # price file HR shopify items
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
#N = open('hr_BNZ_SKU_MASTER.new', 'w')  # bnz not keeping local copyies 
L = open('ShopDCChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
header=["Handle","Title","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","SKU","HS Code","COO","Location","Oberlo"]
#
headerP=("Handle,"+"Title,"+"Variant Price\n") 
#
p.write(headerP)
#
with open('mws/data/DC_SHOP_SKU_MASTER.csv', 'r') as rf: # our list on shopify csv
     reader = csv.reader(rf, delimiter=',')
     with open('DCUpdQtyShop.csv', 'w') as wf:  # just qty file
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w prefix,need to strip to compare with vendor file
              skuInx=skuIn[3:] #strip prefix
              titleInX=line[1]  # only 2 columns info needed , has other cols for shop updates 
              titleIn=titleInX.replace(com,sem) # patch title and change comma to semicolon
              found=0
              ###############  determine pack size from title ############
              pkSize=1
              if pk2Str.lower() in titleIn.lower():
                  pack2Ctr+=1
                  pkSize=2
              #                                                                                    lineOut[5]=pkSize
              with open('DCQtyPrc.csv', 'r') as f:   # custom vendor data prepared by python common module
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuDC1=prefix+line[0] # pid
                    skuDC2=prefix2+line[1] # col 2 in our dcqtyprc custom made file
                    unitCoststr=line[2] # already marked up price at 42%
                    priceUCF=float(unitCoststr) 
                    qtyDC=line[3] #1
                    priceDCstr=line[4] # vendor unit price
                    priceUPC=float(priceDCstr) # vendor unit price w/out any shipping
                    ######################################################################
                    # assign correct skuDC to match for the current record based on useCol
                    skuDC=skuDC1  # use col 3 vendor sku as default
                    #######################################################################
                    if skuDC == skuIn:
                        found=1  # our sku list item matches vendor feed
                        # patch up any not founds 
                        #if notFoundStr.lower() in titleIn.lower():
                        #    titleIn=
                        qtyOut=1  # turn on 
                        qtyOutstr=str(qtyOut)
                        qChngCtrOn +=1 
                        lines=[skuIn,titleIn,"Title","Default Title","","","","",skuDC2,"","",qtyOutstr,"not stocked"]
                        writer.writerow(lines)
                        #priceV = (priceUCF*pkSize) # use this or calc from UPC unit price
                        # recalc price here at different markup if needed
                        ourCost=(priceUPC*pkSize) # price of unit for pkSize Units
                        markUp=(ourCost*markupPct)
                        totalCost=(ourCost+markUp) #  add on markup value
                        priceV=round(totalCost,2)
                        #if priceinF != priceV:  # we dont have previous price to compare prepare all
                        priceOut=str(priceV)
                        pChngCtr +=1 
                        priceData=(skuIn+","+titleIn+","+priceOut+"\n")
                        p.write(priceData)
                        #priceLog=skuIn+" Price Listed= "+str(priceinF)+" newPrice= "+str(priceV)+"\n"
                        #L.write(priceLog)  # for auditing and reference only
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  #if qtyI == 1:
                  qtyOut=0  # turn OFF
                  qtyOutstr=str(qtyOut)
                  qChngCtrOff +=1 
                  lines=[skuIn,titleIn,"Title","Default Title","","","","",skuIn,"","",qtyOutstr,"not stocked"]
                  writer.writerow(lines)

#dump to change log instead of print
#chngLog="Total Items Price Changed = "+str(pChngCtr)+"\n"
#L.write(chngLog)  # for auditing and reference only
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
#################################-----------------END----------------------###################
