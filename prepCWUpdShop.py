# copied from HR to update qty and price on Shopify for Coswtway 12-18-21
# single module to prep price and qty files used to upload to wlmt and amzn
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
# 12-13-21 - prep raw update files - later formated to xmls to upload to mkt channels
#Revisions
import csv
import io
i=0
maxLeadT=5
minQty=25  # 
defQty=1  # to turn on 
pkSizeI=1  # 
markupPct=0.38  # we calc our own markup wmt is slighly lower
prefix="CW-"
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
p = open('CWUpdPrcShop.csv', 'w', encoding="utf-8")  # price file HR shopify items
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
#N = open('hr_BNZ_SKU_MASTER.new', 'w')  # bnz not keeping local copyies 
L = open('ShopCWChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
header=["Handle","Title","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","SKU","HS Code","COO","Location","Oberlo"]
#
headerP=("Handle,"+"Title,"+"Variant Price\n") 
#
p.write(headerP)
#
with open('mws/data/CW_SHOP_SKU_MASTER.csv', 'r') as rf: # our inventory list on shopify csv, using CW prefix
     reader = csv.reader(rf, delimiter=',')
     with open('CWUpdQtyShop.csv', 'w') as wf:  # just qty file
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # Handle, sku in sku list w/o prefix,stored in lower case 
              #skuInx=skuIn[3:] #strip HR-
              #skuOut=prefix+skuInx # no prefix in input or output to upload
              titleIn=line[1]  # only 2 columns info needed , has other cols for shop updates 
              skuOut=line[8] # SKU col in shopify inventory file (item number in costway)
              found=0
              with open('CWQtyPrc.csv', 'r') as f:   # custom vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuCW=line[0] # HW etc
                    qtyCW=line[1] #1
                    qtyCWI=int(qtyCW)
                    priceCWstr=line[2] # vendor unit price
                    priceUPC=float(priceCWstr) # vendor unit price w/out any shipping
                    qtyOut=1 # def to 1 
                    ####################################################
                    if skuCW == skuIn:  # compare skuin 
                        found=1  # our sku list item matches vendor feed
                        #####################################################################
                        # calc price first as we need it when writing qty output (keep price and qty in one row
                        #############################################################################
                        # Determine/calculate shipping regardless of qty setting
                        ############################################################################################
                        shipFee=DefShipFee  # assume default
                        ourCost=(priceUPC*pkSizeI) # base cost
                        #################################################################################################
                        # Compute Final cost with shipping and markup
                        #################################################################################################
                        totalCost=ourCost+shipFee # with shipping
                        markUp=(totalCost*markupPct) # markup amount on cost of product + shipping
                        finalCost=(totalCost+markUp) #  add on markup value
                        priceV=round(finalCost,2)
                        priceOut=str(priceV) # we need this to build our new file
                        pChngCtr +=1 
                        #################### DETERMINE QTY on or OFF ######################
                        if qtyCWI >= minQty:
                            qtyOut=defQty  # turn on 
                            qChngCtrOn +=1 
                            # this is the only time we should update price to make sure it is right,when turning ON
                            priceData=(skuIn+","+titleIn+","+priceOut+"\n")
                            p.write(priceData)
                        else:
                            qtyOut=0  # turn off
                            qChngCtrOff +=1 
                        #write one record with qty 
                        qtyOutstr=str(qtyOut) # 
                        lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                        #lines=[skuIn,titleIn,"Title","Default Title",,,,,skuOut,,,qtyOutstr,"not stocked"]
                        #lines=[skuIn,str(qtyOut),str(priceV),"TRUE"]
                        writer.writerow(lines)
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  #priceOut=999.99  # since item not found price should be place holder for future 
                  qtyOut=0  # turn OFF
                  qtyOutstr=str(qtyOut) 
                  qChngCtrOff +=1 
                  lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                  #lines=[skuIn,titleIn,"Title","Default Title",,,,,skuOut,,,qtyOutstr,"not stocked"]
                  #lines=[skuIn,str(qtyOut),str(priceOut),"TRUE"]
                  writer.writerow(lines)
#
              # Regardless of previous logic we just recreate our .new file
              #priceIn=line[2] # price listed
              #priceIn=line[2] # price listed
              #newStr=(skuIn,itemId,priceOut,qtyOut,gtinIn,pkSize)
              #newStr=(skuIn+","+itemId+","+priceOut+","+qtyOutstr+","+gtinIn+","+pkSize+"\n") # new file
              #N.write(newStr)

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
#M.close()
#N.close()
#R.close()
#################################-----------------END----------------------###################
