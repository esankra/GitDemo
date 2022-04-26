# parse Lemar csv and produces FB format DS for replace updates 12-04-21
# 12-4-21 modified from PrepFBUpdBD (blancho)
# Author : Sankar Ramaiah
##
import csv
import io
#
markupPct=0.42
DefShipFee=11.99
DefQty=1
minCount=5
pkSize=0
pk2Count=0
totalCount=0
skipCount=0
prefix="LM-"
# FB upload of LeeM
#header
header=['id','title','description','link','image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
FB_CAT=106  ## pet supplies
GOOG_CAT=2   # 2    Animals & Pet Supplies  Pet Supplies
INSTK='in stock'
OSTK='out of stock'
myLink='https://salesshoppers.com/collections/pet'  # main collection page
#
with open('mws/data/LeeMarPet.com_Inventory.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('lem-fb-datasource.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              #if len(line) == 0:
              #   print('length of line is 0?')
              #   continue
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[0]    # sku
              #line[4] = "***NULLIFIED-Not Used***"
              #if len(itemNColumn) == 0:
              #if not upcColumn.strip():
              #line[6] = "NA"
              #for i in range(0,35):
              #  if not line[i].strip():
              #       #print(line[i], 'has NO value - empty String?')
              #        line[i] = "NA"
              #  #else
              skuOut=prefix+line[0]
              qtyStr=line[1] 
              try:
                 int(qtyStr)  # is qty valid integer
                 #print('Integer')
              except ValueError:
                 print (skuOut,qtyStr,"Qty in Not integer..skipping this row ...")
                 skipCount +=1
                 continue # skip row and continue loop
              qtyIn=int(qtyStr)
              if qtyIn <= minCount:  # skip and go to next as we need mimimum 5 or more to list
                  skipCount +=1
                  continue
              #line[0]='LM-'+skuIn
              #print(line[0])
              # skip brands not allowed
              brandN=line[17]
              if 'Aquatop' in brandN or 'KONG' in brandN or 'Outward Hound' in brandN or 'Penn Plax' in brandN:
                  print(skuOut,brandN,"brand not allowed, skipping ....")
                  skipCount +=1
                  continue
              itemName=line[18]   # use product N and decide pack size now
              itemSize=line[19]
              print(itemSize)
              # determine packsize 
              pkSize=1 # default
              itemT=itemName+" "+itemSize # for 1 pack unless altered below
              if qtyIn >= 20:
                  itemT='[Pack of 2] '+itemT  # enough to sell pack of 2
                  pkSize=2
                  pk2Count +=1
              print('itemfullname ',itemT)
              # compute price
              priceIn=line[2]
              try:
                 float(priceIn)
                 #print('float')
              except ValueError:
                 print (skuOut,priceIn,"priceIn  Not a float..skipping this row ...")
                 skipCount +=1
                 continue # skip row and continue loop
              #
              Sprice=float(priceIn)   ## sale price in vendor
              itemCost = (Sprice*pkSize) # for correct packsize
              ourPrice = (itemCost+DefShipFee) 
              #print('ourPrice',ourPrice)
              markupPrice = (ourPrice*markupPct)+ourPrice
              priceOut = round(markupPrice,2) # final price to list
              print('OurPrice for sku= ',skuOut, priceOut,'for Pack of ',pkSize)
              # write out needed cols only
              #print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              ## output variables defined
              desc=line[20]
              #desc2=line[7] # details formated
              #condition=line[8]
              condition='new'  # bbd use New
              status=line[14] # Active , Discontinued
              img=line[23] #main image and only one image
              #img2=line[15] # additional 1
              #img3=line[16] # additional 2
              #shipWtout=shipWt
              #custom cols needed for uploading to marketplaces
              #pIdtype='GTIN'
              ##pId='PlaceHolder'   
              #pId=line[9]   # this place holder for GTIN for upload, we store the inventory status here for monitoring!
              #brandN='Generic'
              # drop blancho bedding in title
              #if itemStr in itemName:
              #    itemName=itemName.replace(itemStr, '')
              #    print(skuOut,itemName,"item name replaced ....")
              #    pass
              qty=DefQty  # if we are in loop here then item is avaiable we set qty 1 
              availability=INSTK
              #Addimgs=img2,img3
              # stk status for fb in stock or out of stock (no -) and we write out only in stock
              #if status == 'in-stock':
              #    availability=INSTK
              #    qty=1
              #    lines = [skuOut,itemT,desc,myLink,img1,Addimgs,brandN,qty,availability,price,condition,FB_CAT,GOOG_CAT]
              #    writer.writerow(lines)
              #
              #lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              #lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              ## fb datasource format here
              #lines = [skuOut,itemName,desc1,myLink,img1,brandN,qty,availability,price,condition,FB_CAT,GOOG_CAT]
              totalCount +=1
              lines = [skuOut,itemT,desc,myLink,img,brandN,qty,availability,priceOut,condition,FB_CAT,GOOG_CAT]
              writer.writerow(lines)
              #writer.writelines(lines)
print('Total Records processed = ',totalCount)
print('Total Records skipped = ',skipCount)
print('Total Records pkSize 2 = ',pk2Count)
rf.close()
wf.close()
#
#######################################END SCRIPT ##########################################################
