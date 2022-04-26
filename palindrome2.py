# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 07/26/20
import csv
import io
while (True):
    #
    txtIn= input("Enter string?")
    if len(txtIn) == 0:
        print("nothing entered, exiting..")
        exit()
    l = len(txtIn) 
    print(l,"length")
    rStr=""
    #txtOut=txtIn[::-1] # reverse it in one line
    for i in range(l-1, -1, -1):
        print(i)
        rStr=rStr+txtIn[i]
        #i -=1
    print("reversed string = ",rStr)
    txtOut=rStr
    if txtIn.lower() == txtOut.lower():
        print(txtIn, "given text is a palindrome")
    else:
        print(txtIn,"txt Not Palindrome")
#exit()


