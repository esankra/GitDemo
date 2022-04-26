# copied from BNZ HR to update qty and price on Shopify
# single module to prep price and qty files used to upload to wlmt and amzn
# files contain, sku, qty and sku, price respectively 
# Author : Sankar Ramaiah
# 12-13-21 - prep raw update files - later formated to xmls to upload to mkt channels
#Revisions
#12-21-21 patched title replace comma with semi
#Revisions
import csv
import io
i=0
maxLeadT=5
minQty=25  # 
defQty=1  # to turn on 
pkSizeI=1  # 
markupPct=0.38  # we calc our own markup wmt is slighly lower
prefix="HR-"
pack2Str="Pack of 2"
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
p = open('HRUpdPrcShop.csv', 'w')  # price file HR shopify items
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
#N = open('hr_BNZ_SKU_MASTER.new', 'w')  # bnz not keeping local copyies 
L = open('ShopHRChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
header=["Handle","Title","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","SKU","HS Code","COO","Location","Oberlo"]
#
headerP=("Handle,"+"Title,"+"Variant Price\n") 
#
p.write(headerP)
#
with open('mws/data/HR_SHOP_SKU_MASTER.csv', 'r') as rf: # our list on shopify csv
     reader = csv.reader(rf, delimiter=',')
     with open('HRUpdQtyShop.csv', 'w') as wf:  # just qty file
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # sku in sku list w prefix,need to strip to compare with vendor file
              skuInx=skuIn[3:] #strip HR-
              skuOut=prefix+skuInx
              titleInX=line[1]  # only 2 columns info needed , has other cols for shop updates 
              titleIn=titleInX.replace(com,sem) # patch title and change comma to semicolon
              found=0
              with open('HRQtyPrc.csv', 'r') as f:   # custom vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuHR=line[0] # item Number in lemar
                    qtyHR=line[1] #1
                    qtyHRI=int(qtyHR)
                    priceHRstr=line[2] # vendor unit price
                    priceUPC=float(priceHRstr) # vendor unit price w/out any shipping
                    leadTIn=line[3] # leattime in vendor
                    leadTI=int(leadTIn)
                    qtyOut=1 # def to 1 
                    ####################################################
                    if skuHR == skuInx:  # compare skuin stripped without prefix
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
                        if leadTI > maxLeadT:  # we force inactive , do not turn on
                            qtyOut=0  # turn off
                            qtyOutstr=str(qtyOut) # carry to new file
                            qChngCtrOff +=1 
                            lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                            writer.writerow(lines)
                            break # skip to next record
                        if qtyHRI >= minQty:
                            qtyOut=defQty  # turn on 
                            qChngCtrOn +=1 
                            # this is the only time we should update price to make sure it is right
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
                  priceOut=999.99  # since item not found price should be place holder for future 
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
