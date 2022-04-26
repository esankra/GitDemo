# new py to parse all listing and identify pksize for all LM- skus build LEM_SKU_MASTER2.csv
# Author : Sankar Ramaiah
# Date: 12-30-21
# rev: 1/4/22 - add a second file to show title and pksize for verification and debugging purposes only
#
import csv
import io
##
prefixLM="LM-"
pk2Str="Pack of 2"
pk3Str="Pack of 3"
pk4Str="Pack of 4"
pk6Str="Pack of 6"
pk8Str="Pack of 8"
pk10Str="Pack of 10"
pk12Str="Pack of 12"
##
L = open('mws/data/LMPksize.txt', 'w')  # here we log sku and item name and pksize so we can check any issues
#logOut=[{}]*3
logOut=""
lineOut=[{}]*6  # 6 column sku master for price qty montioring 
i=0
with open('mws/data/lmlist.txt', 'r') as rf:
     reader = csv.reader(rf, delimiter='\t')
     with open('mws/data/LEM_SKU_MASTER2.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          #desired_column = [6]
          for line in reader:
              skuIn=line[0]  # seler sku in amzn report
              skuInPrefix=skuIn[:3] # get prefix
              if skuInPrefix == prefixLM:
                  asinIn=line[1]
                  itemName=line[2]
                  priceL=line[3]
                  qtyL=line[4]
                  lineOut[0]=skuIn
                  #lineOut[1]=itemName                    ####for debuging if you need to show item name 
                  lineOut[1]=asinIn
                  lineOut[2]=priceL
                  lineOut[3]=qtyL
                  lineOut[4]=skuIn[3:]  #vendor item number w/out prefix for match against vendor feed
                  pkSize=1 #default as pksize not available in amzn report
                  lineOut[5]=pkSize # default pksize to 1
                  #determine correct packsize dynamically and create sku master output
                  if pk2Str.lower() in itemName.lower():
                      pkSize=2
                      lineOut[5]=pkSize
                  elif pk3Str.lower() in itemName.lower():
                      pkSize=3
                      lineOut[5]=pkSize
                  elif pk4Str.lower() in itemName.lower():
                      pkSize=4
                      lineOut[5]=pkSize
                  elif pk6Str.lower() in itemName.lower():
                      pkSize=6
                      lineOut[5]=pkSize
                  elif pk8Str.lower() in itemName.lower():
                      pkSize=8
                      lineOut[5]=pkSize
                  elif pk10Str.lower() in itemName.lower():
                      pkSize=10
                      lineOut[5]=pkSize
                  elif pk12Str.lower() in itemName.lower():
                      pkSize=12
                      lineOut[5]=pkSize

              #if len(line) == 0:
              #   print('length of line is 0?')
              #   continue
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[0]    # sku
              #line[4] = "***NULLIFIED-Not Used***"
              #if len(itemNColumn) == 0:
              #if not upcColumn.strip():
              #for i in range(0,15):
              #  if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
              #        line[i] = "*Empty*"
              writer.writerow(lineOut)
              # build and write log 
              #logOut[0]=skuIn
              #logOut[1]=itemName
              #logOut[2]=pkSize
              logOut=skuIn+"\t"+itemName+"\t"+str(pkSize)+"\n"
              L.write(logOut)
rf.close()
wf.close()
L.close()
