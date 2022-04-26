# read scents world csv and prep FB DS 12-19-21
# Author : Sankar Ramaiah
import csv
import io
i=0
#shipPct=0.20
DefShipFee=9.95 # 8 + dmage protection 
markupPct=0.40
priceLimit=20.00
prefix="SW-"
minQty=10 # 
DefQty=1 # 
skipStr1="Trundle"
skipStr2="trundle"
#
header=['id','title','description','link','image_link','additional_image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
#header BNZ - we prepare both files at one time  - 
#headerB=['id','title','quantity','price','force_update']  # just an update for Bnz 
#
#302    health & beauty > beauty > fragrances
FB_CAT=302  # home > home goods > home decor
#479    Health & Beauty Personal Care   Cosmetics   Perfume & Cologne           
GOOG_CAT=479  # google category (home & Garden)
INSTK='in stock'
OSTK='out of stock'
sampleStr="(Sample)"  # we skip samples
myLink='https://salesshoppers.com/collections/perfumes'  # main collection page
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
with open('swproducts.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('SW_FB_Datasource.csv', 'w') as wf:  # for FB Datasource scents world = SW
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(header)
          #desired_column = [6]
          for line in reader:  # original vendor feed
              skuIn=line[0]
              itemT=line[1]  # product name
              itemDesc=line[2] # product desc (appears same as title)
              itemCat=line[3]
              brandN=line[4]
              manfctr=line[5]
              img=line[7] # large 
              img2=line[8] # medium img
              priceIn=line[11] # product price (discounted for dropshipper)
              qtyIn=line[12]  # vendor qty 
              gender=line[13] #men women
              itemWt=line[14] # shipping wt
              countryO=line[15] # country of origin
              itemUpc=line[16]
              ###############################  DATA Validations ############################
              try:
                  int(qtyIn)
              except ValueError:
                  print (skuIn,qtyIn,"Qty not integer.. skipping this row ...")
                  continue
              # validate price
              try:
                 float(qtyIn)
                 #print('float')
              except ValueError:
                 print (skuIn,qtyIn,"price Not a float.. skipping this row ...")
                 continue # loop
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
              # check length of title and truncate as neededa
              itemTOut=itemT
              if len(itemT) > 150:
                  itemTOut=itemT[:148]  # take 149 characters to avoid limit excess
                  print(skuIn,"Title too long",itemT)
              ######################################################################################
              # if we make it here - compute price now
              #######################################################################################
              price=float(priceIn) # here price is UNIT cost not marked up
              pkSize=1
              # Add markup next
              priceX=(price*pkSize)+DefShipFee # consider pksize as it doubles shipping for higher price
              markupAmount=(priceX*markupPct)
              priceOutX=(priceX+markupAmount)
              priceOut=round(priceOutX,2)
              # proceed to create outfile
              skuOut=prefix+skuIn
              qtyOut=DefQty  
              ### customize description
              #itemDescOut=itemDesc+" "+itemCat+" By "+manfctr+" Brand "+brandN+" County of Origin "+countryO
              itemDescOut=itemDesc+" By "+manfctr+"\nBrand:"+brandN+"\nCounty of Origin: "+countryO+"\n"+itemCat
              print(itemDescOut)
              #itemDescOut=itemDesc+"\n"+itemDescA+itemDescC+itemDescD+"\n" ##+"prop65 Reason "+prop65 #  +assembleYN #+" prop65 "+prop65

              # write out
              lines = [skuOut,itemTOut,itemDescOut,myLink,img,img2,brandN,qtyOut,availability,priceOut,condition,FB_CAT,GOOG_CAT]
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
