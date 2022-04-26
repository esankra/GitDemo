# parse dropship txt data and prepare walmart tempate data 1/30/2022
# prepare only relevant data from original csv file and create sku,qty and price files 
# Author : Sankar Ramaiah
# date : 12/30/2022
import csv
import io
i=0
minQty=15 # availability in vendor feed min requirment
DefQty=1 # if row in vendor feed product is available, qty not provided 
markupPct=0.40 # 
INSTK='available'
recCount=0
filenameTxt="dropship.txt"
catFurniture='furniture'
pkSize=1
prefix='CSW-'
line2=[]
#
##
with open(filenameTxt, 'r') as rf: # origianl vendor feed 
     reader = csv.reader(rf, delimiter='\t')
     with open('CWWlmtAdd.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              recCount +=1
              itemNumber=line[0]
              if line[0] == '*itemNOempty*':
                  itemNumber='NA'
              skuIn=line[1] # col 2 
              itemName=line[3]
              priceIn=line[4]  # 
              qtyIn=line[5]
              specIn=line[6]
              descIn=line[7]
              catIn=line[8]
              img1=line[11]
              img2=line[12]
              img3=line[13]
              #
              ##print(line[0])
              #print(line[35])
              # validate categories to skip - processing only furniture
              if catFurniture not in catIn.lower():
                  #skip it not furniture
                  continue
              ### basic data validations here
              try:
                  int(qtyIn)
              except ValueError:
                  print (skuIn,qtyIn,"Qty not integer.. skipping this row ...")
                  continue
              # validate price
              try:
                 float(priceIn)
                 #print('float')
              except ValueError:
                 print (skuIn,priceIn,"price Not a float.. skipping this row ...")
                 continue # loop
              qtyInt=int(qtyIn)
              if qtyInt <= minQty:
                  #skipping for low qty
                  continue
              # calc price here 
              priceUPC=float(priceIn)
              ourCost=(priceUPC*pkSize) # price of unit for pkSize Units
              markUp=(ourCost*markupPct)
              totalCost=(ourCost+markUp) #  add on markup value
              priceV=round(totalCost,2)
              priceOut=str(priceV) # we need this to build our new file
              qty=1
              #prepare description 
              descOut=descIn+"<p>"+specIn+"<p>"+" Item No: "+itemNumber
              skuOut=prefix+skuIn
              # write walmt template output
              lines = [skuOut,"GTIN","GTINValue",itemName,"Generic",priceOut,"1",descOut,img1,img2,img3]
              writer.writerow(lines)
              #write out our master list 
              #line2 = [skuOut,itemName,qty,priceIn]
              #writer.writelines(lines)
print("Total records in feed = ",recCount)
rf.close()
wf.close()
##############################
