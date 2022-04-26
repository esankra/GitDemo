# parse homeroot.csv
# prepare all active cars from DC with 42% markup for FB data source on commerce manager 11-28-21
# Author : Sankar Ramaiah
##
import csv
import io
i=0
#shipFeePerOrder=4.70
#shipFeePerItem=0.30
#shipFeePerLb=0.75
#discountPct=0.20
maxTitleLen=150
markupPct=0.42
INSTK='in stock'
fig1='Figurine'
fig2='Figurines'
fig3='figurine'
fig4='figurines'
fig5='figure'
fig6='figures'
fig7='Figure'
fig8='Figures'

skipCount=0
#
myLink='https://salesshoppers.com/collections/model-cars'  # main collection page
#
#header[]
header=['id','title','description','link','image_link','brand','quantity_to_sell_on_facebook','availability','price','condition','fb_product_category','google_product_category']
FB_CAT=43
GOOG_CAT=3551
#
with open('products.csv', 'r') as rf:  # raw vendor input
     reader = csv.reader(rf, delimiter=',')
     with open('cars-fb-load-4000+.csv', 'w') as wf: # data source on html folder on vm2
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
              ## removing loop to set NA - not needed as we dont write out these columns
              #for i in range(0,35):
                #if not line[i].strip():
                     #print(line[i], 'has NO value - empty String?')
                      #line[i] = "NA"
                #else
              skuIn=line[2]  # dc code sku col3
              line[0]='DC-'+skuIn
              skuOut=line[0]  # id
              itemName=line[3] # title
              # fix long titles - fb requires it to be under 150 chars
              if len(itemName) > maxTitleLen:
                  itemName=itemName[0:148]
              # skip all figurene or figurenes 12-6-21 chng
              if  fig1 in itemName or fig2 in itemName or fig3 in itemName or fig4 in itemName or fig5 in itemName or fig6 in itemName or fig7 in itemName or fig8 in itemName:
                  #print(skuOut,"skiping figurines",itemName)
                  skipCount +=1
                  continue
              #shipCost=(shipWt*shipFeePerLb)
              #totalShipCost=shipCost+shipFeePerItem+shipFeePerOrder
              ####print('total ship fee for sku= ',skuIn, totalShipCost)
              Spricestr=line[7]
              try:
                 float(Spricestr)
                 #print('float')
              except ValueError:
                 print (skuOut,Spricestr,"price Not a float.. skipping this row and continue to next")
                 continue # loop
              Sprice=float(Spricestr)   ##
              ##Sprice=float(line[7])   ## price in vendor
              ##print(Sprice)
              #pctOfprices = (Sprice*discountPct) #price discount
              ourPrice = Sprice
              ###print('ourPrice',ourPrice)
              markupPrice = (ourPrice*markupPct)+ourPrice
              #line[8] = round(markupPrice,2) # here we use the street price col to store our computed price 
              ##print('markuprice',line[10])
              ##print('OurPrice for sku= ',skuIn, line[10])
              # write out needed cols only
              #print(line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35])
              ## output variables defined
              brandN=line[4]   #'Generic'
              # out col 3 = myLink shopify collection
              desc1=line[6] #desc
              #desc2=line[7] # details formated
              condition='new'
              qty=1
              availability=INSTK
              price=round(markupPrice,2) # here we use the street price col to store our computed price 
              #price=line[8]
              img1=line[27] #main image
              ##pId='PlaceHolder'   
              #pId=line[9]   # this place holder for GTIN for upload, we store the inventory status here for monitoring!
              #lines = [line[0],line[2],line[6],line[8],line[9],line[10],line[14],line[15],line[35]]
              ##lines = [skuOut,pIdtype,pId,itemName,brandN,price,shipWtout,desc1+desc2,img1,img2,img3]
              # writeout relevant data for monitoring and translate status to qty available
              #if status == INSTK:
              #    qty=1
              #else:
              #    qty=0
              lines = [skuOut,itemName,desc1,myLink,img1,brandN,qty,availability,price,condition,FB_CAT,GOOG_CAT]
              writer.writerow(lines)
              #writer.writelines(lines)
##
print ("Number of rows skipped as Figurine/Figurines = ",skipCount)
#
rf.close()
wf.close()
