import os
import re
import sys
from pyaws import ecs

ecs.setLicenseKey('1P5WQWG01FJRRNESE4G2')

bookFile=open('/home/rexa/code/python/kate-look-up/kate-book-list-original.csv')
bookStrings=bookFile.readlines()

#get rid of "Date Acquired:" entries
bookStrings=[entry for entry in bookStrings if entry[0:4]!="Date"]

authorStrings=bookStrings[1::3]
titleStrings=bookStrings[0::3]

for author, title in zip(authorStrings,titleStrings):
    titleCln=title.rstrip().strip('"').lstrip('Title: ')
    authorCln=author.rstrip().strip('"').lstrip('Author: ')
    


