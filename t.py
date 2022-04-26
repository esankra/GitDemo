s="LM-5993"
comma=","
semic=";"
a=s[:3]
print("prefix= ",a)
quit()

useCol=3
try:
    int(s)
    i=int(s)
    print("i= ",i)
    if i <= 5000:
        # all col 1 match skus
        useCol=1
        print("use col1 for sku match")
except ValueError:
    useCol=1
    print("use col3 for sku match")
#
print("column to use found to be =",useCol)
#print("noprefix = ",a)
b=s.upper()
title="Adjustable Sofa Frame, Black - Metal Frame Black"
titleOut=title.replace(comma,semic)
print(titleOut)
