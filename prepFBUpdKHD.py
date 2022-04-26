# read KGIPQ.csv prepared by previous module and preps the FB DS file for FB
# Author : Sankar Ramaiah
# 12-7-21 - prereq must be met and files must be combined 
import csv
import io
i=0
#shipPct=0.20
#DefShipFee=10.95
markupPct=0.40
priceLimit=20.00
prefix="KHD-"
minQty=20 # for both packsize 1 or 2 
DefQty=1 # 
DefShipFee=10.95  # add this to 2 pk
prefix="KH-"
#
header=['id','title','description','link','image_link','additional_image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
# header BNZ - we prepare both files at one time  - 
#headerB=['id','title','quantity','price','force_update']  # just an update for Bnz 
headerB="id,title,quantity,price,force_update\n"  # just an update for Bnz 
FB_CAT=375  # home > home goods > home decor
GOOG_CAT=536  # google category (home & Garden)
INSTK='in stock'
OSTK='out of stock'
sampleStr="(Sample)"  # we skip samples
myLink='https://salesshoppers.com/collections/home-garden'  # main collection page
#
condition="new"
# here we open BNZ KH out file and write out header
B=open('KH_BNZ_Datasource.csv', 'w') # for bonanza upload
B.write(headerB)
          #writerB = csv.writer(wfB, delimiter=',')
          #writerB.writerow(headerB)
#
with open('KGIPQ.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('KH_FB_Datasource.csv', 'w') as wf:  # for FB Datasource
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:  # qty file top loop
              sku=line[0]
              itemT=line[1]
              qtyIn=line[2]  # vendor qty already validated in previous module
              priceIn=line[3] # unit cost per item including shipping cost
              itemUpc=line[4]
              brandN=line[5]
              itemDesc=line[6] # with dimensions etc
              itemWt=line[7]
              itemPrice=line[8] # validated for float previsous module
              found=0
              #print('sku= ',line[0])
              with open('KHD_Image_Links.csv', 'r') as f:   # images file from KHD
              #with open('KHD_Image_Links.csv', 'r', encoding="ISO-8859-1") as f:   # 
                readerI = csv.reader(f, delimiter=',')
                for line in readerI:
                    skuIn=line[0]
                    if sku == skuIn:
                        # get image links as needed
                        img=line[4] # main image
                        img2=line[1] # may be empty
                        #print('matched',skuIn,priceIn,qtyIn)
                        found=1
              #print(sku,'foundflag = ',found)
              if found == 1:
                  # found and img string is NOT empty process the record other skip
                  if not img: 
                      continue  #skip record in loop`
                  # prepare final output here
                  availability=OSTK # default it
                  qty=int(qtyIn)
                  if qty >= minQty: 
                      availability=INSTK
                  #
                  price=float(priceIn) # here price is UNIT cost already computed earlier includes shipping
                  priceU=float(itemPrice) # vendor price of single unit without any shippping
                  itemTOut=itemT # def
                  pkSize=1
                  # Add markup next
                  priceX=(price*pkSize) # consider pksize as it doubles shipping for higher price
                  markupAmount=(priceX*markupPct)
                  priceOutX=(priceX+markupAmount)
                  priceOut=round(priceOutX,2)
                  # determine if we need packsize 2 then overwrite computation for 2 packs
                  if priceU <= priceLimit: # $20?? original vendor price of unit without shipping
                      # we imake it 2 pack
                      itemTOut="[Pack Of 2] "+itemT
                      pkSize=2
                      priceX=(priceU*pkSize)+DefShipFee # 
                      markupAmount=(priceX*markupPct)
                      priceOutX=(priceX+markupAmount)
                      priceOut=round(priceOutX,2)
                  # proceed to create outfile
                  qtyOut=0 # this is what we show on the market channel FB or other
                  skuOut=prefix+sku
                  ##print(sku, addDesc)
                  if availability == INSTK:
                    qtyOut=DefQty  
                    lines = [skuOut,itemTOut,itemDesc,myLink,img,img2,brandN,qtyOut,availability,priceOut,condition,FB_CAT,GOOG_CAT]
                    writer.writerow(lines)
                  #here write out Bonanza update file 
                  #headerB=['id','title','quantity','price','force_update']  # just an update for Bnz 
                  #priceData=sku+","+priceIn+"\n"
                  linesB=skuOut+","+itemTOut+","+str(qtyOut)+","+str(priceOut)+","+"TRUE\n"
                  B.write(linesB)
#
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
              #skuIn=line[0]
              #line[0]='BD-'+skuIn
              #print(line[0])
              ##print(line[35])
              #shipWt=float(line[35])
              #print(shipWt*shipFeePerLb)
              #shipCost=(shipWt*shipFeePerLb)
              #totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              #print('total ship fee for sku= ',skuIn, totalShipCost)
              #Sprice=float(line[11])   ## sale price in vendor
              #print(Sprice)
              #pctOfprice = (Sprice*discountPct) #price discount
              #ourPrice = (Sprice-pctOfprice)+totalShipCost
              #print('ourPrice',ourPrice)
              #markupPrice = (ourPrice*markupPct)+ourPrice
              #line[10] = round(markupPrice,2) # here we use the street price col to store our computed price 
              #print('markuprice',line[10])
              #print('OurPrice for sku= ',skuIn, line[10])
              ## write out needed cols only
              ##print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              #### output variables defined
              #skuOut=line[0]
              #itemName=line[2]
              #desc1=line[6]
              #desc2=line[7] # details formated
              #condition=line[8]
              #status=line[9] # in-stock or out-of-stock
              #price=line[10]
              #img1=line[14] #main image
              #img2=line[15] # additional 1
              #img3=line[16] # additional 2
              #shipWtout=shipWt
              ##custom cols needed for uploading to marketplaces
              #pIdtype='GTIN'
              ###pId='PlaceHolder'   
              #pId=line[9]   # this place holder for GTIN for upload, we store the inventory status here for monitoring!
              #brandN='Generic'
              ##lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              ##lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              #writer.writelines(lines)
rf.close()
wf.close()
B.close()
#p.close()
#############################
