# read Brybelly.csv and prep BB2 multipack items for upload to walmart
# Author : Sankar Ramaiah
# 3/31/2022
import csv
import io
import string
i=0
#shipPct=0.20
#DefShipFee=10.95
markupPct=0.40
priceLimit=20.00
prefix="BB2-"  # multipack sku (adding as new items to walmart wit new upc codes)
minQty=20 # 
DefQty=1 # 
DefShipFee=19.95  # 
skipStr1="- None -"  # any row has this we skip
skipStr2="trundle"
#updated header for walmart
header=['SKU','PID type','PID(GTIN value)','Product Name','Brand','Price','ShipWt','Desc','Main Img','Img2','Img3']
##header=['id','title','description','link','image_link','additional_image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
# header BNZ - we prepare both files at one time  - 
#headerB=['id','title','quantity','price','force_update']  # just an update for Bnz 
#
FB_CAT=50  # toy and games
#GOOG_CAT=536  # google category (home & Garden)
GOOG_CAT=1239  # Toys Games
INSTK='in stock'
OSTK='out of stock'
sampleStr="(Sample)"  # we skip samples
myLink='https://salesshoppers.com/collections/toys'  # main collection page
#
maxLeadT=2
recCtr=0
condition="new"
# here we open BNZ KH out file and write out header
#B=open('KH_BNZ_Datasource.csv', 'w') # for bonanza upload
#B.write(headerB)
          #writerB = csv.writer(wfB, delimiter=',')
          #writerB.writerow(headerB)
#
with open('BrybellyCatalog.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('BB2_WMT_ADD.csv', 'w') as wf:  # for onetime upload of multipack BB items
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:  # original vendor file
              skuIn=line[0]
              itemT=line[1]
              qtyIn=line[2]  # vendor qty 
              itemUpc=line[3]
              priceIn=line[4] # unit cost per item without markup and shipping
              brandN="Brybelly"
              itemWt=line[6]
              # cleanup wt
              wtStr=itemWt.replace('lbs.', '')
              itemSpec=line[7]
              itemDesc=line[8] # Detailed desc 
              ############# makeup the image URLS based on sku  ###########
              img="https://www.brybelly.com/site/product-images/"+skuIn+"_alt-01.jpg"
              img2="https://www.brybelly.com/site/product-images/"+skuIn+"_alt-02.jpg"
              img3="https://www.brybelly.com/site/product-images/"+skuIn+"_alt-03.jpg"
              ###############################  DATA Validations ############################
              if skipStr1 in line:
                  print("Skipping none...",skuIn,itemT)
                  continue
              # validate wt
              try:
                  float(wtStr)
              except ValueError:
                 print (skuIn,wtStr,"weight str data error..skipping this row ...")
                 continue
              wtF=float(wtStr)
              wt=round(wtF,2)
              print (wt," weight")
              if wt > 1.00:
                 print (skuIn,wtStr,"weight more than 1 lb.skipping this row ...")
                 continue  # we skip 
              # validate qty
              try:
                  int(qtyIn)
              except ValueError:
                  print (skuIn,qtyIn,"Qty not integer.. skipping this row ...")
                  continue
              qtyOut=int(qtyIn)
              # validate price
              try:
                 float(priceIn)
                 #print('float')
              except ValueError:
                 print (skuIn,priceIn,"price Not a float.. skipping this row ...")
                 continue # loop
              # found and img string is NOT empty process the record other skip
              if not img: 
                  continue  #skip record in loop if first image empty
              #
              # prepare final output here
              availability=OSTK # default it
              qty=int(qtyIn)
              if qty >= minQty:
                  #
                  availability=INSTK
              else:
                  continue  # we skip this row and move fwd
                  #

              ######################################################################################
              # if we make it here - compute price now
              #######################################################################################
              price=float(priceIn) # here price is UNIT cost not marked up
              ######################## PKSIZE based on price so that we can offset shipping cost #####
              pkSize=1 # defaut
              if price <= 5.00:
                  pkSize = 4
              elif price <= 10:
                    pkSize=3
              elif price <= 20.00:
                       pkSize = 2
              # change title to indicate pksize 
              if pkSize > 1:
                  itemTx="[Pack of "+str(pkSize)+"] - "+itemT
              else:
                  itemTx =  itemT
              # Add markup next
              priceX=(price*pkSize)+DefShipFee # consider pksize if needed
              markupAmount=(priceX*markupPct)
              priceOutX=(priceX+markupAmount)
              priceOut=round(priceOutX,2)
              # proceed to create outfile
              skuOut=prefix+skuIn
              qtyOut=DefQty  
              ### customize description
              #itemDescA=("Dimensions in Inches (HeightxWidthxDepth) = "+itemH+"x"+itemW+"x"+itemD+"\n")
              #itemDescB=("Material= "+itemMaterial+"\n")
              #itemDescC=("Color= "+itemColor+"\n")
              #itemDescD=("Item Weight= "+itemWt+"\n")
              itemDescOut=itemDesc+" Dimensions "+itemSpec
              # write out
              lines = [skuOut,'GTIN','<insert GTIN>',itemTx,brandN,priceOut,wt,itemDescOut,img,img2,img3]
              #lines = [skuOut,itemTx,itemDescOut,myLink,img,img2,brandN,qtyOut,availability,priceOut,condition,FB_CAT,GOOG_CAT]
              writer.writerow(lines)
              recCtr +=1
#
print("Total number of records in input ",recCtr)
###
rf.close()
wf.close()
#B.close()
#p.close()
#############################
