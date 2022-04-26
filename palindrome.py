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
    txtOut=txtIn[::-1]
    if txtIn.lower() == txtOut.lower():
        print(txtIn, "given text is a palindrome")
    else:
        print(txtIn,"txt Not Palindrome")
#exit()

