import time
import os
import urlgrabber
import re
import sys
from BeautifulSoup import BeautifulSoup
from pyaws import ecs

ecs.setLicenseKey('1P5WQWG01FJRRNESE4G2')

bookFile=open('/home/rexa/code/python/kate-look-up/book-list-4.txt')
bookStrings=bookFile.readlines()
outFile=open('/home/rexa/Desktop/out.test','w')

#get rid of "Date Acquired:" entries
bookStrings=[entry for entry in bookStrings if entry[0:4]!="Date"]

authorStrings=bookStrings[1::3]
titleStrings=bookStrings[0::3]

for author, title in zip(authorStrings,titleStrings):
    titleCln=title.rstrip().strip('"').replace('Title: ','')
    titleCln=titleCln.replace('A-List, The:','')
    
    #titleCln=re.sub('\(.*Internet.*\)','',titleCln)
    #titleCln=re.sub('\(.*Best.*\)','',titleCln)    
    titleCln=re.sub(r'\(.*\)','',titleCln)    
    titleCln=re.sub(r'Book #[\d]','',titleCln)
    authorCln=author.rstrip().strip('"').replace('Author: ','')
    authorCln=authorCln.replace('/',' ')
    
    
    titleQry=titleCln.replace(' ','+');
    authorQry=authorCln.replace(' ','+')
    queryStr=titleQry+'+'+authorQry
    titleSearchURL='http://books.google.com/books?client=firefox-a&um=1&q='+titleQry+'&btnG=Search+Books'
    advSearchURL='http://books.google.com/books?as_q=&num=10&client=firefox-a&btnG=Google+Search&as_epq=&as_oq=&as_eq=&as_libcat=0&as_brr=0&lr=&as_vt='+titleQry+'&as_auth='+authorQry+'&as_pub=&as_sub=&as_drrb=c&as_miny=&as_maxy=&as_isbn='
    basSearchURL='http://books.google.com/books?client=firefox-a&um=1&q='+queryStr+'&btnG=Search+Books'
    
    
    
    searchURL=advSearchURL;
    searchResPage=urlgrabber.urlopen(searchURL)
    searchResSoup=BeautifulSoup(searchResPage)
    
    bookLinkList=searchResSoup.find('h2','resbdy');
    
    if not bookLinkList:
        searchURL=basSearchURL;
        searchResPage=urlgrabber.urlopen(searchURL)
        searchResSoup=BeautifulSoup(searchResPage)
    
        bookLinkList=searchResSoup.find('h2','resbdy');
        
    if not bookLinkList:
        searchURL=titleSearchURL;
        searchResPage=urlgrabber.urlopen(searchURL)
        searchResSoup=BeautifulSoup(searchResPage)
    
        bookLinkList=searchResSoup.find('h2','resbdy');
    
    preInfo=[authorCln,queryStr,titleCln,'']
    preInfo=[entry+'\n' for entry in preInfo]
    print ''.join(preInfo)
    #outFile.writelines(preInfo)
    
    
    for bookLink in bookLinkList:
        linkURL=bookLink.attrs[0][1]
        #get rid of everything except the book id
        linkURL=linkURL.split('&')[0]
        bookPage=urlgrabber.urlopen(linkURL)
        bookPageSoup=BeautifulSoup(bookPage)
        infoSects=bookPageSoup.findAll('div',{'class':re.compile('^bookinfo_section_line')})
        infoStrs=[info.string.encode('ascii','ignore') for info in infoSects]
        
        
        bookTitle=bookAuth=bookPub=bookYear=bookISBN10=bookISBN13=bookPages='NA'
        bookTitle=infoStrs[0];
        bookAuth=[entry for entry in infoStrs if entry.startswith('By ')][0]
        bookAuth=bookAuth[3:]
        bookPub=[entry for entry in infoStrs if entry.startswith('Published by ')][0]
        bookYear=bookPub.split(',')[-1].strip()
        bookPub=','.join(bookPub.split(',')[0:-1])
        bookPub=bookPub[13:]
        
        try:
            bookISBNs=[entry for entry in infoStrs if entry.startswith('ISBN')]
            bookISBNs=bookISBNs[0][5:]
            bookISBN10=bookISBNs.split(', ')[0]
            bookISBN13=bookISBNs.split(', ')[1]
        except Exception,e:
            bookISBNs='NA'
        try:
            bookPages=[entry for entry in infoStrs if entry.endswith(' pages')][0].strip().rstrip(' pages')
        except Exception, e:
            bookPages='NA'

        fmtList=[bookTitle,bookAuth,bookPub,bookYear,bookISBN10,bookISBN13,bookPages]
        fmtStr =  '\t'.join([bookTitle,bookAuth,bookPub,bookYear,bookISBN10,bookISBN13,bookPages+'\n'])
        
        
        print fmtStr
        outFile.writelines(fmtStr)
        
        time.sleep(.2)
        