# read homeroots.txt and build HR FB DS for LeadT < 3
# Author : Sankar Ramaiah
import csv
import io
i=0
#shipPct=0.20
#DefShipFee=10.95
markupPct=0.40
priceLimit=20.00
prefix="KHD-"
minQty=20 # 
DefQty=1 # 
DefShipFee=0.00  # 
prefix="HR-"
skipStr1="Trundle"
skipStr2="trundle"
#
header=['id','title','description','link','image_link','additional_image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
# header BNZ - we prepare both files at one time  - 
#headerB=['id','title','quantity','price','force_update']  # just an update for Bnz 
#
FB_CAT=375  # home > home goods > home decor
GOOG_CAT=536  # google category (home & Garden)
INSTK='in stock'
OSTK='out of stock'
sampleStr="(Sample)"  # we skip samples
myLink='https://salesshoppers.com/collections/home-garden'  # main collection page
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
with open('homeroots.txt', 'r') as rf:
     reader = csv.reader(rf, delimiter='\t')
     with open('HR_FB_Datasource.csv', 'w') as wf:  # for FB Datasource
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:  # original homeroots.txt file lines
              skuIn=line[0]
              itemUpc=line[1]
              brandN=line[2]
              itemT=line[3]
              itemDesc=line[4] # 
              itemWt=line[7]
              itemH=line[9]
              itemW=line[10]
              itemD=line[11]
              leadTIn=line[12]
              qtyIn=line[13]  # vendor qty 
              Spricestr=line[14] # Dropship cost in vendor  variable used for validations
              priceIn=line[14] # unit cost per item without markup and shipping
              img=line[20]
              img2=line[21]
              itemColor=line[31]
              itemMaterial=[32]
              assembleYN=[39]
              prop65=[71] # last column
              ###############################  DATA Validations ############################
              if skipStr1 in itemT:
                  print("Skipping Trundles...",skuIn,itemT)
              try:
                 int(leadTIn)
              except ValueError:
                 print (skuIn,leadTIn,"Lead Time Not integer..skipping this row ...")
                 continue # skip row and continue loop
              leadTI=int(leadTIn)
              # skip items with higher lead time
              if leadTI > maxLeadT:
                  #print("LeadT high sku = ",skuIn,leadTIn)
                  continue
              try:
                  int(qtyIn)
              except ValueError:
                  print (skuIn,qtyIn,"Qty not integer.. skipping this row ...")
                  continue
              qtyOut=int(qtyIn)
              # validate price
              try:
                 float(Spricestr)
                 #print('float')
              except ValueError:
                 print (skuIn,Spricestr,"price Not a float.. skipping this row ...")
                 continue # loop
              Sprice=float(Spricestr)   ## sale price in vendor
              # found and img string is NOT empty process the record other skip
              if not img: 
                  continue  #skip record in loop
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
              pkSize=1
              # Add markup next
              priceX=(price*pkSize) # consider pksize as it doubles shipping for higher price
              markupAmount=(priceX*markupPct)
              priceOutX=(priceX+markupAmount)
              priceOut=round(priceOutX,2)
              # proceed to create outfile
              skuOut=prefix+skuIn
              qtyOut=DefQty  
              ### customize description
              itemDescA=("Dimensions in Inches (HeightxWidthxDepth) = "+itemH+"x"+itemW+"x"+itemD+"\n")
              #itemDescB=("Material= "+itemMaterial+"\n")
              itemDescC=("Color= "+itemColor+"\n")
              itemDescD=("Item Weight= "+itemWt+"\n")
              itemDescOut=itemDesc+"\n"+itemDescA+itemDescC+itemDescD+"\n" ##+"prop65 Reason "+prop65 #  +assembleYN #+" prop65 "+prop65

              # write out
              lines = [skuOut,itemT,itemDescOut,myLink,img,img2,brandN,qtyOut,availability,priceOut,condition,FB_CAT,GOOG_CAT]
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
