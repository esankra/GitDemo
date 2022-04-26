# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 11-19-20
# convert LM SHOP PRICE file to txt - one time use 
import csv
import io
import sys

#print ("The script has the name %s" % (sys.argv[1]))
#prefixIn=(sys.argv[1])
RETD="RETIRED"
PUB="PUBLISHED"
InFileN="/home/esankra/inventory/mws/data/LM_SHOP_PRICE_MASTER.csv"
NColumns=38
NRetd=0
NP=0
lagTime="7"
#print ('Argument List:', str(sys.argv))
outFileN='LM_SHOP_PRICE_MASTER.txt'
print ("outfileN = ",outFileN) 
with open(InFileN, 'r') as rf:
     reader = csv.reader(rf, delimiter=',')
     with open(outFileN, 'w') as wf:
        writer = csv.writer(wf, delimiter='\t')
        for line in reader:
          #desired_column = [6]
          writer.writerow(line)
#print("skipped Not Published items Count =", NP) 
rf.close()
wf.close()
