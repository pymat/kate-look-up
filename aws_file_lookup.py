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
    

#pdfDir='/home/rexa/Desktop/books/Python/'
pdfDir='/home/rexa/Desktop/books/hardcases/'
res=os.listdir(pdfDir)
res.sort()
resPDF=[resFile for resFile in res if re.search(r'\.pdf$',resFile)]
basePath=pdfDir
fileDictList=list()
    
for file in resPDF:
    pdfFilePath=pdfDir+file    
    
    rePDF=re.compile(r'\.pdf')
    reCHM=re.compile(r'\.chm')
    reISBN=re.compile(r'ISBN')
    reISBNLine=re.compile(r'^.*?ISBN.*?$')
    
    
    if rePDF.search(file):  
        fileEsc=file
        fileEsc=re.sub(r'\'','\\\'',fileEsc)
        fileEsc=re.sub(r' ','\ ',fileEsc)
        fileEsc=re.sub(r'-','\-',fileEsc)
        fileEsc=re.sub(r'\'','\'',fileEsc)
        fileEsc=re.sub(r'\(','\(',fileEsc)
        fileEsc=re.sub(r'\)','\)',fileEsc)
        fileEsc=re.sub(r'\&','\&',fileEsc)
        
        
        filePath=basePath+file
        filePathEsc=basePath+fileEsc
              
        pdfStr='pdftotext -f 1 -l 6 '+filePathEsc+' -'
        fd=os.popen(pdfStr)
        pdfLines=fd.readlines()
        
        ISBNNum=0
        for line in pdfLines:
            if (line.find('ISBN') >=0):
                startPos=line.find('ISBN')
                try:
                    ISBNLine=line[startPos:startPos+30]
                except Exception, e:
                    ISBNLine=line[startPos:]
                
                if len(ISBNLine.split(' ')[1]) < 10:
                    ISBNNum=ISBNLine.split(' ')[2]
                    ISBNNum=ISBNNum.rstrip("\n")
                else:
                    ISBNNum=ISBNLine.split(' ')[1]
                    ISBNNum=ISBNNum.rstrip("\n")                                        
                print ISBNNum + '  '+ file
                break #break from the loop over lines
            
        fileMain=file.rstrip('.pdf')
        fileNameStr=' '.join(fileMain.split('.'))
        print fileNameStr
        
        fileDict={'ISBNNum':ISBNNum,\
                  'pathToFile':filePath,\
                  'pathToFileEsc':filePathEsc,\
                  'fileSearchString':fileNameStr}
        
        fileDict.values()
        fileDict['ISBNNum']
        
        fileDictList.append(fileDict)
        
        if (not fileDict['ISBNNum']):
            nameStr=filePath+"!!!_ISBNSearchFail"
            msgFile=open(nameStr,'w')
            msgFile.close()
            
        else:
            nameStr=filePath+"___"+str(ISBNNum)
            msgFile=open(nameStr,'w')
            msgFile.close()
                    
print len(fileDictList)

#for fileDict in fileDictList:
    #if fileDict['ISBNNum']:
        #ISBNNum=fileDict['ISBNNum']
        #ISBNNumsOnly=ISBNNum.replace('-','')
        
        #try:
            #books = ecs.ItemLookup(ISBNNumsOnly,IdType='ISBN',SearchIndex='Books',ResponseGroup='ItemAttributes')
        #except Exception, e:
            #print e
    
        #topRes=books[0]
