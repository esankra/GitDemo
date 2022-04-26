#!/usr/bin/env python3

import csv
with open('file.csv', newline='') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in linereader:
            print("From Key: %s\nFrom Name: %s" % (row[0], row[1]))
                            
