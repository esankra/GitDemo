## Benzara SHOPIFY qty updates - uses the daily BZ cat csv file downloaded via filezilla or ftp 
# 2/25/22
# Author : Sankar Ramaiah
#Revisions
#
import csv
import io
i=0
maxLeadT=5
minQty=10  # low qty for shop 
defQty=1  # to turn on 
pkSizeI=1  # 
markupPct=0.38  # we calc our own markup wmt is slighly lower
prefix="BZ-"
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
#p = open('CWUpdPrcShop.csv', 'w', encoding="utf-8")  # price file HR shopify items
#with open('bbdQtyPrc.txt', 'r') as f:   # sku,price and qty (0/1)
#     readerV = csv.reader(f, delimiter='\t')
     #BDVendorList = f.read()
     #for qlist in BDVendorList:
         #print(qlist[0],qlist[1],qlist[2])
         #print(BDVendorList[0][1])
     #print(BDVendorList)
#
N = open('BZ_SHOP_SKU_MASTER.new', 'w')  # we maitain local copy for shop - reexport BZ-Bulk tag to reset
writerN = csv.writer(N)
#
L = open('ShopBZChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
# header for qty updates to shop
header=["Handle","Title","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","SKU","HS Code","COO","Location","Oberlo"]
#
#headerP=("Handle,"+"Title,"+"Variant Price\n") 
#
#N.write(header)
#
with open('mws/data/BZ_SHOP_SKU_MASTER.csv', 'r') as rf: # our inventory list on shopify csv, using CW prefix
     reader = csv.reader(rf, delimiter=',')
     with open('BZUpdQtyShop.csv', 'w') as wf:  # just qty file
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:
              skuIn=line[0] # Handle, sku in sku list w/o prefix,stored in lower case 
              skuInX=skuIn[3:] #strip prefix
              #skuInX=prefix+skuIn # no prefix in input 
              titleIn=line[1]  # only 2 columns info needed , has other cols for shop updates 
              skuOut=line[8] # SKU col in shopify inventory file (item number in costway)
              listedQtystr=line[11]
              found=0
              with open('BZDailyCat.csv', 'r') as f:   # downlaoded vendor data 
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuBZ=line[0] # vendor sku from inv feed
                    qtyBZ=line[1] #1
                    #priceBZstr=line[2] # vendor unit price
                    #priceUPC=float(priceCWstr) # vendor unit price w/out any shipping
                    qtyOut=1 # def to 1 
                    ####################################################
                    if skuBZ.upper()  == skuInX.upper():  # compare skuin 
                        found=1  # our sku list item matches vendor feed
                        ## validate qty 
                        try:
                            int(qtyBZ)
                        except ValueError:
                            print(skuBZ,"invalid qty data..skiping..",qtyBZ)
                            break
                        qtyBZI=int(qtyBZ)
                        #################### DETERMINE QTY on or OFF ######################
                        if qtyBZI >= minQty:
                            qtyOut=defQty  # turn on 
                            qChngCtrOn +=1 
                            # no price checks for bz
                            #priceData=(skuIn+","+titleIn+","+priceOut+"\n")
                            #p.write(priceData)
                        else:
                            qtyOut=0  # turn off
                            qChngCtrOff +=1 
                        #write one record with qty only if there is a change from listed qty
                        qtyOutstr=str(qtyOut) # a
                        if qtyOutstr != listedQtystr:
                            #
                            lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                            writer.writerow(lines)
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  qtyOut=0  # turn OFF
                  qtyOutstr=str(qtyOut) 
                  qChngCtrOff +=1 
                  if qtyOutstr != listedQtystr:
                      #
                      lines=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
                  #lines=[skuIn,titleIn,"Title","Default Title",,,,,skuOut,,,qtyOutstr,"not stocked"]
                  #lines=[skuIn,str(qtyOut),str(priceOut),"TRUE"]
                      writer.writerow(lines)
#
              # Regardless of previous logic we just recreate our .new file
              # writing as csv file
              lineout=[skuIn,titleIn,"Title","Default Title","","","","",skuOut,"","",qtyOutstr,"not stocked"]
              writerN.writerow(lineout)
              #newStr=(skuIn+","+titleIn+","+"Title"+","+"Default Title"+","+""+","+""+","+""+","+""+","+skuOut+","+""+","+""+","+qtyOutstr+","+"not stocked"+"\n")
              ##newStr=(skuIn+","+titleIn+","+"Title"+","+"Default Title"+","+","+","+","+skuOut+","+qtyOutstr+","+"not stocked""\n") # new file
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
#chngLog="Total Items with PkSize more than 2 in SKU LIST = "+str(pack2Ctr)+"\n"
#L.write(chngLog)  # for auditing and reference only
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
#p.close()
L.close()
#M.close()
N.close()
#R.close()
#################################-----------------END----------------------###################
