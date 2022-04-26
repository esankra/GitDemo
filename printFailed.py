# parse homeroot.csv
# Author : Sankar Ramaiah
# 5/18/21 - convert Le daily catalog to text file with filling empty columns
import csv
import io
F="FAILED"
i=0
a=[]*3

with open('data.txt', 'r') as rf:
     reader = csv.reader(rf, delimiter=' ')
     with open('dataout.txt', 'w') as wf:
          writer = csv.writer(wf, delimiter='\t')
          #writer = csv.writer(wf, delimiter='|')
          #desired_column = [6]
          for line in reader:
              if F.lower() in line[2].lower():
              #if line[2] == "FAILED":
                  # load only failed records 
                  a.append(line)
              #if line[3] == :
              #   print('length of line is 0?')
              #   continue
              #upcColumn = list(line[i] for i in desired_column)
              #itemNColumn = line[0]    # sku
              #line[4] = "***NULLIFIED-Not Used***"
              #if len(itemNColumn) == 0:
              #if not upcColumn.strip():
              #line[6] = "NA"
              #for i in range(0,30):
               # if not line[i].strip():
                      #print(line[i], 'has NO value - empty String?')
                #      line[i] = "NA"
              writer.writerow(line)
a.sort(reverse=True) # sort descending
#print (a)
for x in a:
    print(x[0],x[1],x[2])
rf.close()
wf.close()
