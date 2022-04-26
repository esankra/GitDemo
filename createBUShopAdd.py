# prepare add Butler to shopify
# Author : Sankar Ramaiah
# Date:03-08-22
# 
import csv
import io
#
#lineOut=[]*20
prefix="BU-"
i=0
headerOut= ["Handle","Image Src","Image Position","Collection","Title","Variant Price","Body (HTML)","Vendor","Tags","Published","Option1 Name","Option1 Value","Variant Requires Shipping","Variant Taxable","Variant Fulfillment Service","Variant Inventory Policy","Variant Inventory Tracker","Variant SKU","Variant Grams","Gift Card"] 
with open('buCat.txt', 'r') as rf:
     reader = csv.reader(rf, delimiter='\t')
     with open('BuAddShop.csv', 'w') as wf:
          writer = csv.writer(wf, delimiter=',')
          writer.writerow(headerOut)
          for line in reader:
              skuIn=prefix+line[0]
              itemT=line[1]
              b1=" Dimensions: "+line[17]  #dimensions
              b2=" Finish: "+line[3]
              b3=" Materials: "+line[22]
              b4=" Color: "+line[31]
              b5=" Type: "+line[11]
              itemPrice="9999.99"
              itemDescX=line[60] # Details
              img1=line[67].strip()
              img2=line[69].strip()
              img3=line[71].strip()
              #img4=line[73]
              #img5=line[75]
              #
              if not img1:
                  #check img2
                  if img2:
                      img1=img2
                  else:
                      #
                      if img3:
                          #
                          img1=img3
                      else:
                          #
                          continue
#                      
              itemDesc=itemDescX+"<p>"+b1+"</p>"+"<p>"+b2+"</p>"+"<p>"+b3+"</p>"+"<p>"+b4+"</p>"+"<p>"+b5+"</p>"
              lineOut=[skuIn,img1,"1","Home Decor",itemT,itemPrice,itemDesc,"Sales Shoppers","BZ-Bulk","TRUE","Title","Default Title","TRUE","TRUE","manual","deny","shopify",skuIn,"0","FALSE"]
              writer.writerow(lineOut) 
              # second img
              if img2:
                  #
                  lineOut=[skuIn,img2,"2"]
                  writer.writerow(lineOut)                
              # 3rd img
              if img3:
                  #
                  lineOut=[skuIn,img3,"3"]
                  writer.writerow(lineOut)
              # clear out images
              img1=""
              img2=""
              img3=""
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
rf.close()
wf.close()
