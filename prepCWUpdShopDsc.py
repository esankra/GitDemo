# parse dropship txt data and build updated descriptions with specificiations
# prepare only relevant data from original csv file and create sku,qty and price files 
# Author : Sankar Ramaiah
# 4/5/22
import csv
import io
i=0
DefQty=1 # if row in vendor feed product is available, qty not provided 
markupPct=0.42 # may not use this here
INSTK='available'
recCount=0
filenameTxt="dropship.txt"
#
##
with open(filenameTxt, 'r') as rf: # origianl vendor feed 
     reader = csv.reader(rf, delimiter='\t')
     with open('CWUpdDesc.csv', 'w') as wf:  # create updated descriptions 4/5/22
          writer = csv.writer(wf, delimiter=',')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              recCount +=1
              #for i in range(0,35):
                #if not line[i].strip():
                     #print(line[i], 'has NO value - empty String?')
                      #line[i] = "NA"
                #else
              skuIn=line[1] # col 2 
              itemT=line[3]
              priceIn=line[4]  # 
              qtyIn=line[5]
              itemSpec=line[6] # detailed spec
              itemDesc=line[7]
              # build our final desc for shop updates
              itemDescOut=itemSpec+"<p>"+itemDesc
              ##print(line[0])
              #print(line[35])
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
              #UnitPriceOut = round(Sprice,2)
              #if status == INSTK:
              #    qty=1
              #else:
              #    qty=0
              #skuOut=skuIn.upper() # store sku upper case to match against vendor feed later
              skuOut=skuIn.lower() # store sku lower case to match against our inventory list from shopify
              lines = [skuOut,itemT,itemDescOut]
              writer.writerow(lines)
              #writer.writelines(lines)
print("Total records in feed = ",recCount)
rf.close()
wf.close()
##############################
