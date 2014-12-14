#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, time, os
import codecs
from bs4 import BeautifulSoup
from urllib.request import urlopen

def stripHtmlTags(htmlTxt):
    if htmlTxt is None:
        return None
    else:
    	return ''.join(htmlTxt.findAll(text=True)) 

def GetEnough(cntr,params):
	if params[len(params)-1]=='!':
		params=params[:len(params)-2]
	if params==' ?':
		params=' '
	if params!='' and params!='—' and params!=' ?' and params!=' ':		
		if cntr==1:
			f1.write(TheWord+'; '+params+'; pres.p1.sg; vblex')
			f1.write(u"\r\n")		
		if cntr==2:
			f1.write(TheWord+'; '+params+'; pres.p2.sg; vblex')
			f1.write(u"\r\n")	
		if cntr==3:
			f1.write(TheWord+'; '+params+'; pres.p3.sg; vblex')
			f1.write(u"\r\n")	
		if cntr==4:				
			f1.write(TheWord+'; '+params+'; pres.p1.pl; vblex')
			f1.write(u"\r\n")	
			f1.write(TheWord+'; '+params+'; pres.p1.pl; vblex')
			f1.write(u"\r\n")	
			f1.write(TheWord+'; '+params+'; pres.p1.pl; vblex')
			f1.write(u"\r\n")	
		if cntr==5:
			f1.write(TheWord+'; '+params+'; past.p1.sg; vblex')
			f1.write(u"\r\n")	
		if cntr==6:
			f1.write(TheWord+'; '+params+'; past.p2.sg; vblex')
			f1.write(u"\r\n")	
		if cntr==7:
			f1.write(TheWord+'; '+params+'; past.p3.sg; vblex')
			f1.write(u"\r\n")	
		if cntr==8:
			f1.write(TheWord+'; '+params+'; past.p1.pl; vblex')
			f1.write(u"\r\n")	
			f1.write(TheWord+'; '+params+'; past.p1.pl; vblex')
			f1.write(u"\r\n")	
			f1.write(TheWord+'; '+params+'; past.p1.pl; vblex')
			f1.write(u"\r\n")
		if cntr==14:
			f1.write(TheWord+'; '+params+'; imp.p2.sg; vblex')
			f1.write(u"\r\n")		
		if cntr==16:
			f1.write(TheWord+'; '+params+'; imp.p2.pl; vblex')
			f1.write(u"\r\n")	
		if cntr==17:
			f1.write(TheWord+'; '+params+'; inf; vblex')
			f1.write(u"\r\n")	
		if cntr==18:
			f1.write(TheWord+'; '+params+'; pprs; vblex')
			f1.write(u"\r\n")	
		if cntr==19:
			f1.write(TheWord+'; '+params+'; pp; vblex')
			f1.write(u"\r\n")	
		if cntr==20:
			f1.write(TheWord+'; '+params+'; supn; vblex')
			f1.write(u"\r\n")	

URL = urlopen('https://en.wiktionary.org/wiki/Category:Faroese_verbs').read()
URL2 = urlopen('https://en.wiktionary.org/wiki/Category:Faroese_verbs').read()

f1 = codecs.open("Faroese_verbs.txt", 'a', encoding ='utf-16')

while True:

	soup = BeautifulSoup(URL)
	div = soup.find('div', id='mw-pages')
	for pages in div.find_all('a'):
		if str(pages.contents[0])=='next 200':
			URL2 = urlopen('https://en.wiktionary.org/' + pages.get('href')).read()

	print ("Getting nouns from new page..")
	for lis in div.find_all('li'):
		for links in lis.find_all('a'):
			TheWord = links.get('title')
			if TheWord[0]!='-':
				wordUrl = urlopen('https://en.wiktionary.org'+links.get('href')).read()

			try:
				soup = BeautifulSoup(wordUrl)
				for divs in soup.find_all('table'):
					if divs.get('id')=='w.fo.v.conj':
						div = soup.find('table',id='w.fo.v.conj')

				params=['']*21
				cnt=0
				cnt1=0
				cntr=0

				try:
					#try to find a table
					if div.find('tr').findNext('strong').contents[0]==TheWord:
						for trs in div.find_all('tr'):
							cnt=cnt+1
							cnt1=0
							if cnt>=5:
								for tds in trs.find_all('td'):
									cnt1=cnt1+1
									if cnt1>=2:
										cntr=cntr+1
										if stripHtmlTags(tds)=='':
											params=' '
										elif stripHtmlTags(tds)[len(stripHtmlTags(tds))-1]=='?':
											params=' '
										elif stripHtmlTags(tds)[len(stripHtmlTags(tds))-1]=='-':
											params=' '
										else:
											try:
												if stripHtmlTags(tds).find('(')!=-1:
													for lnks in tds.find_all('a'):
														params=lnks.get('title')
														if params.find('(')==-1:
															GetEnough(cntr,params)
														else:
															GetEnough(cntr,params[:params.find('(')-1])
												elif stripHtmlTags(tds).find('/')!=-1:
													for lnks in tds.find_all('a'):
														params=lnks.get('title')
														if params.find('(')==-1:
															GetEnough(cntr,params)
														else:
															GetEnough(cntr,params[:params.find('(')-1])
												else:
													params=stripHtmlTags(tds)
													GetEnough(cntr,params)
											except:
												params=tds.contents[0]
						cntr=0
						print ('Recorded: '+TheWord)
				except:
					cnt=0
			except:
				cnt=0
	if URL2 == URL:
		break
	else:
		URL = URL2
print ('Excellent! All Faroese verbs have been loaded!')