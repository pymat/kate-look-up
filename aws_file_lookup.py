import os
import re
import sys
from pyaws import ecs

ecs.setLicenseKey('1P5WQWG01FJRRNESE4G2')

bookFile=open('/home/rexa/code/python/kate-look-up/kate-book-list-original.csv')
bookStrings=bookFile.readlines()
bookStrings=[entry for entry in bookStrings if entry!='\n']
authorStrings=bookStrings[0::2]
titleStrings=bookStrings[1::2]
for title, author in zip(titleStrings,authorStrings):
    print title,author
    


#for fileDict in fileDictList:
    #if fileDict['ISBNNum']:
        #ISBNNum=fileDict['ISBNNum']
        #ISBNNumsOnly=ISBNNum.replace('-','')
        
        #try:
            #books = ecs.ItemLookup(ISBNNumsOnly,IdType='ISBN',SearchIndex='Books',ResponseGroup='ItemAttributes')
        #except Exception, e:
            #print e
    
        #topRes=books[0]
