# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 08/06/20
# 10-9-2020 revised to exlude UNPUBLISHED instead of RETIRED
import csv
import io
import sys

#print ("The script has the name %s" % (sys.argv[1]))
prefixIn=(sys.argv[1])
RETD="RETIRED"
PUB="PUBLISHED"
ACT="ACTIVE"
fpath="/home/esankra/inventory/mws/data/"
NColumns=38
NRetd=0
NP=0
lagTime="7"
# lag time setup file 
##lf= open("wlmt-lagtime.csv","w")   # overwrites
#lf= open("wlmt-lagtime.csv","a+")   # file to append for lag time default setup
print ("prefix input = ", prefixIn)
#print ('Number of arguments', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
outFileN=(fpath+prefixIn+'wlmt.txt')
print ("outfileN = ",outFileN) 
with open('wlmt.csv', 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open(outFileN, 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #desired_column = [6]
          for line in reader:
              #upcColumn = list(line[i] for i in desired_column)
            ###  itemNColumn = line[2]
              #if len(upcColumn) == 0:
              #if not upcColumn.strip():
              for i in range(0, NColumns):
                  if not line[i]:
                    line[i]="*NA*"
              lifeCycle=line[10]
              pubStatus=line[8]
              sku=line[1]
              skuPrefix=sku[0:3]
              skuInput=sku[3:]
              #print(skuPrefix,skuInput)
              if skuPrefix == prefixIn:
                line[1] = skuInput
                ##print(skuInput+'\t',line[2]+'\t',line[3]+'\t',line[4]+'\t',line[11]+'\t',line[16]+'\t',line[37], file=wf)
                #print(skuInput,line[2],line[3],line[4],line[11],line[16],line[37], file=wf)
                ######  print(sku+","+lagTime, file=lf) # creating this in lowlevel scripts in qty chk
                #if pubStatus == PUB:
                if lifeCycle == ACT:
                    writer.writerow(line)
                else:    
                    NP = NP + 1
                    #print(skuInput, "skipping ** RETIRED **")
                    ##writer.writerow(line)
print("skipped lifecycle Not ACTIVE items Count =", NP) 
rf.close()
wf.close()
##lf.close()
