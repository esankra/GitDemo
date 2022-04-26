# parse bbd.csv created by bbd inentory fetch or weekly monitor program
# 12-1-21 modified wlmt bd upload py to handle errors and skip over critical data errors for fb datasource
# for uploading new items to walmart from Blancho - use this module 11-27-21
# Author : Sankar Ramaiah
##
import csv
import io
#
shipFeePerOrder=4.70
shipFeePerItem=0.30
shipFeePerLb=0.75
discountPct=0.20
markupPct=0.45
# FB upload of blancho bedding
#header[]
header=['id','title','description','link','image_link','additional_image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
FB_CAT=349 # home > bedding
GOOG_CAT=4171   # Home & Garden   Linens & Bedding                    
INSTK='in stock'
OSTK='out of stock'
sampleStr="(Sample)"  # we skip samples
itemStr="Blancho Bedding -"  # we  replace this with empty string
myLink='https://salesshoppers.com/collections/home-garden'  # main collection page
#
with open('bbd.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open('bbd-fb-datasource.csv', 'w') as wf:
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
              itemName=line[1]   # use title some rows in vendor missing item name
              if sampleStr in itemName:
                  print(skuOut,itemName,"item is sample , skipping ....")
                  continue
              skuIn=line[0]
              line[0]='BD-'+skuIn
              print(line[0])
              #print(line[35])
              # check if wt is all decimals before floating it
              #print(shipWt*shipFeePerLb)
              shipWtstr=line[35]
              try:
                 float(shipWtstr)
                 #print('float')
              except ValueError:
                 print (shipWtstr,"ship wt Not a float..skipping this row ...")
                 continue # skip row and continue loop
              shipWt=float(shipWtstr)
              shipCost=(shipWt*shipFeePerLb)
              totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              ##print('total ship fee for sku= ',skuIn, totalShipCost)
              # again validate price if not valid skip over
              Spricestr=line[11]
              try:
                 float(Spricestr)
                 #print('float')
              except ValueError:
                 print ("price Not a float.. skipping this row and continue to next")
                 continue # loop
              Sprice=float(Spricestr)   ## sale price in vendor
              #Sprice=float(line[11])   ## sale price in vendor
              print(Sprice)
              pctOfprice = (Sprice*discountPct) #price discount
              ourPrice = (Sprice-pctOfprice)+totalShipCost
              #print('ourPrice',ourPrice)
              markupPrice = (ourPrice*markupPct)+ourPrice
              line[10] = round(markupPrice,2) # here we use the street price col to store our computed price 
              #print('markuprice',line[10])
              print('OurPrice for sku= ',skuIn, line[10])
              # write out needed cols only
              #print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              ## output variables defined
              skuOut=line[0]
              desc1=line[6]
              desc2=line[7] # details formated
              #condition=line[8]
              condition='new'  # bbd use New
              status=line[9] # in-stock or out-of-stock
              price=line[10]
              img1=line[14] #main image
              img2=line[15] # additional 1
              img3=line[16] # additional 2
              shipWtout=shipWt
              #custom cols needed for uploading to marketplaces
              pIdtype='GTIN'
              ##pId='PlaceHolder'   
              pId=line[9]   # this place holder for GTIN for upload, we store the inventory status here for monitoring!
              brandN='Generic'
              # drop blancho bedding in title
              if itemStr in itemName:
                  itemName=itemName.replace(itemStr, '')
                  print(skuOut,itemName,"item name replaced ....")
                  pass
              availability=OSTK
              Addimgs=img2,img3
              # stk status for fb in stock or out of stock (no -) and we write out only in stock
              if status == 'in-stock':
                  availability=INSTK
                  qty=1
                  lines = [skuOut,itemName,desc1+desc2,myLink,img1,Addimgs,brandN,qty,availability,price,condition,FB_CAT,GOOG_CAT]
                  writer.writerow(lines)
              #
              #lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              ##lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              ## fb datasource format here
              #lines = [skuOut,itemName,desc1,myLink,img1,brandN,qty,availability,price,condition,FB_CAT,GOOG_CAT]
              #lines = [skuOut,itemName,desc1,myLink,img1,brandN,qty,availability,price,condition,FB_CAT,GOOG_CAT]
              #writer.writerow(lines)
              #writer.writelines(lines)
rf.close()
wf.close()
#
#######################################END SCRIPT ##########################################################
