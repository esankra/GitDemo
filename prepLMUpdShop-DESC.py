# LEemar SHOPIFY updates 1-11-22
# Just prepare update file with full description for all SKUS in master
# Author : Sankar Ramaiah
##
import csv
import io
i=0
notStkd="not stocked"
minQty=10  # 
defQty=2  # to turn on 
markupPct=0.40  # we cancalc our own markup wmt is slighly lower
prefix="LM-"
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
p = open('LMUpdDESCShop.csv', 'w')  # once items we want is located in our SKU LIST
#L = open('ShopLMChng.log', 'w')  # track items with price changes & qty showing old new pirce
## log file
header=["Handle","Title","Option1 Name","Option1 Value","Option2 Name","Option2 Value","Option3 Name","Option3 Value","SKU","HS Code","COO","Location","Oberlo"]
#
headerP=("Handle,"+"Title,"+"Body (HTML)\n")   # just title and desc fix
#
p.write(headerP)
#
#N = open('LM_SHOP_SKU_MASTER.new', 'w')  # we writeout locally and copy it back to data once successful 
## log file
#with open('DCQtyPrc.csv', 'r') as rf: # previosuly prepared with unitcost and unit price
with open('mws/data/LM_SHOP_SKU_MASTER.csv', 'r') as rf: # our shop inventory file
     reader = csv.reader(rf, delimiter=',')
     with open('LMUpdQtyShop.csv', 'w') as wf:
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
              priceinF=float(priceIn)
              #priceOut=str(priceinF)
              skuOut=skuIn.upper() # same as handle in upper
              qtyI=int(qtyIn) # listed qty integer
              qtyOutstr=qtyIn
              found=0
              # we may want to create exception sku list for restricted here so wlmtdel can process it
              #determine pksize based on title
              #print('sku= ',line[0])
              with open('mws/data/LeeMarPet.com_Inventory.csv', 'r') as f:   # vendor data for initial title cleanup
              #with open('LEMQtyPrc.csv', 'r') as f:   # custom vendor data for daily monitoring
                readerV = csv.reader(f, delimiter=',')
                for line in readerV:
                    ###################################################
                    skuLEM=line[0] # item Number in lemar
                    qtyLEM=line[1] #1
                    qtyLEMI=int(qtyLEM)
                    priceLEMstr=line[2] # vendor unit price
                    priceUPC=float(priceLEMstr) # vendor unit price w/out any shipping
                    #productSizeX=line[19] # to append to item title only if reading original vendor data
                    #productSize=productSizeX.replace(com,sem) # patch title and change comma to semicolon
                    ####################################################
                    if skuLEM.lower() == skuInx.lower(): # itemnumber comparison 
                        #print("skuLem",skuLEM)
                        productDesc=line[20] # html desc
                        found=1  # our sku list item matches vendor feed
                        #######################  make it multipack based on price ###################
                        #priceData=(skuIn+","+titleIn+","+productDesc+"\n")
                        priceData=(skuIn+"\t"+titleIn+"\t"+productDesc+"\n")
                        p.write(priceData)
                        break
                        # may need break here to exit inner loop
                        #print('matched',skuIn,priceIn,qtyIn)
              recCtr +=1 # how many we have in our SKU list from all listing reprts
              if found == 0:  # item NOT found in vendor data but we have in our SKU list
                  ##
                  # since item not found we keep title data as desc
                  priceData=(skuIn+"\t"+titleIn+"\t"+titleIn+"\n")
                  p.write(priceData)
#
              # Regardless of previous logic we just recreate our .new file
              #priceIn=line[2] # price listed
              #priceIn=line[2] # price listed
              #newStr=(skuIn,itemId,priceOut,qtyOut,gtinIn,pkSize)
              ##newStr=(skuIn+","+titleIn+","+priceOut+","+qtyOutstr+","+gtinIn+","+pkSize+"\n") # new file

#dump to change log instead of print
#print("Total items in SKU List file = ",recCtr) 
#print("Total 2 pack items in SKU List file = ",pack2Ctr)
rf.close()
wf.close()
p.close()
#L.close()
#M.close()
#N.close()
#R.close()
#################################-----------------END----------------------###################
