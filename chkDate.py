# importing datetime module
import datetime
import time
from dateutil import parser
#  
# date in yyyy/mm/dd format
#d1 = "2021-10-01 19:26:03+00:00" # avoid all recs afrer this date
#d1 = datetime.datetime(2018, 5, 3)
d2 = datetime.datetime(2018, 6, 1)
#
dtstr="Thu, 10 Dec 2021 19:26:03 +0000" #current
dtstr2="Thu, 28 Oct 2022 19:26:03 +0000"  # oct 28th 2021

#d3 = datetime.datetime(2018, 6, 1)

#parser.parse("Aug 28 1999 12:00AM")
d3=parser.parse(dtstr)
#
d1=parser.parse(dtstr2)  # constant date
#
print("parsed date d1 = ", d1)
print("parsed date d3 = ", d3)
#ioutput 2021-12-09 19:26:03+00:00
# Comparing the dates will return
# either True or False
print("d3 is greater than d1 : ", d3 > d1)
#print("d1 is less than d2 : ", d1 < d2)
#print("d1 is not equal to d2 : ", d1 != d2)
