import os
import re
import sys
from pyaws import ecs

ecs.setLicenseKey('1P5WQWG01FJRRNESE4G2')

bookFile=open('/home/rexa/code/python/kate-look-up/kate-book-list-original.csv')
bookStrings=bookFile.readlines()
#get rid of "Date Acquired:" entries
bookStrings=[entry for entry in bookStrings if entry[0:4]!="Date"]
authorStrings=bookStrings[0::3]
titleStrings=bookStrings[1::3]
for author, title in zip(authorStrings,titleStrings):
    print title.lstrip('Title: '),author.lstrip('Author: ')
    
    


#for fileDict in fileDictList:
    #if fileDict['ISBNNum']:
        #ISBNNum=fileDict['ISBNNum']
        #ISBNNumsOnly=ISBNNum.replace('-','')
        
        #try:
            #books = ecs.ItemLookup(ISBNNumsOnly,IdType='ISBN',SearchIndex='Books',ResponseGroup='ItemAttributes')
        #except Exception, e:
            #print e
    
        #topRes=books[0]
