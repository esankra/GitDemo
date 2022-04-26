# parse koleimports csv
# Author : Sankar Ramaiah
# Date: 07/26/20
import csv
import io
with io.open('koleimp.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, quotechar='"')
        for row in reader:
            #print(row[0]) # row[-1] gives the last column
            print row[0], row[6]
csvfile.close()

