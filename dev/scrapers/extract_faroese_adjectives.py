#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  extract_faroese_adjectives.py
#  
#  Copyright 2014 Mikhail Ivchenko <ematirov@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#

import requests, logging
from lxml import html


log = logging.getLogger("logger")

WIKI_URL = "https://en.wiktionary.org"
INDEX_PAGE="/wiki/Category:Faroese_adjectives"
#INDEX_PAGE="/wiki/Category:Faroese_adjective_superlative_forms"
LINK_FOR_ARTICLE_XPATH = "body/div/div/div/div/div/div/table/tr/td/ul/li/a"
LINK_FOR_ARTICLE_WITHOUT_TABLE_XPATH = "body/div/div/div/div/div/div/ul/li/a"
LINK_FOR_PAGE_XPATH = "body/div/div/div/div/div/a"
SUBCATEGORY_XPATH = "body/div/div/div/div/div/div/ul/li/div/div/a"
CONTENT_XPATH = "//*[@id='mw-content-text']"
LANG = "Faroese"

visitedPages = []

def parseIndex(indexPage):

	response = requests.get(WIKI_URL + indexPage)

	articles = []
	if response.ok:
		visitedPages.append(indexPage)
		log.info(WIKI_URL + indexPage)
		doc = html.document_fromstring(response.text)
		linksForArticles = doc.xpath(LINK_FOR_ARTICLE_XPATH)
		#for link in linksForArticles:
		#	articles.append(link.get("href"))
		#linksForArticles = doc.xpath(LINK_FOR_ARTICLE_WITHOUT_TABLE_XPATH)
		for link in linksForArticles:
			articles.append(link.get("href"))
		linksForPages = doc.xpath(LINK_FOR_PAGE_XPATH)
		nextPage = ""
		if len(linksForPages) > 2:
			#We have a links to prev page and to next page.
			nextPage = linksForPages[1].get("href")
		elif linksForPages:
			#We have a links to prev page or to next page.
			if "prev" in linksForPages[0].text:
				#We have only a link to prev page. End of work.
				pass
			else:
				nextPage = linksForPages[0].get("href")
		if nextPage:
			if nextPage not in visitedPages:
				articles = articles + parseIndex( nextPage )
		linksForSubcategory = doc.xpath(SUBCATEGORY_XPATH)
		for link in linksForSubcategory:
			#Visit subcategories
			if link.get("href") not in visitedPages	:
				articles = articles + parseIndex( link.get("href") )
	else:
		log.error("Error "+ str(response.status_code) + " " + WIKI_URL + indexPage )
	return articles

def parseArticle(article):
	response = requests.get(WIKI_URL + article)
	
	if response.ok:
		log.error(WIKI_URL+article)
		doc = html.document_fromstring(response.text)
		content = doc.xpath(CONTENT_XPATH)[0]
		children = content.getchildren()
		currentLangFound = False
		adjectiveFound = False
		for i in range(len(children)):
			if children[i].tag == "h2":
				if children[i].getchildren()[0].text == LANG:
					currentLangFound = True
				else:
					currentLangFound = False
			if children[i].tag == "h3":
				if children[i].getchildren()[0].text == "Adjective":
					adjectiveFound = True
				else:
					adjectiveFound = False
			if children[i].tag == "table" and currentLangFound and adjectiveFound:
				words = parseTabel(children[i])
				if words:
					return words
		log.error("Table cannot be found! "+WIKI_URL+article)
	else:
		log.error("Error "+ str(response.status_code) + " " + WIKI_URL + article )
	return []

def getTextFromElement(element):
	if element.text and element.text != "(" and element.text != ")":
		return element.text
	if element.getchildren():
		return getTextFromElement(element.getchildren()[0])
	return ""

def parseTabel(table):
	tds = table.xpath("tr/td")
	if len(tds)>=34:
		t = [getTextFromElement(tds[6]),getTextFromElement(tds[7]),getTextFromElement(tds[8]),getTextFromElement(tds[10]),getTextFromElement(tds[11]),getTextFromElement(tds[13]),getTextFromElement(tds[14]),getTextFromElement(tds[15]),getTextFromElement(tds[17]),getTextFromElement(tds[18]),getTextFromElement(tds[19]),getTextFromElement(tds[26]),getTextFromElement(tds[27]),getTextFromElement(tds[28]),getTextFromElement(tds[30]),getTextFromElement(tds[32]),getTextFromElement(tds[34])]
		return t
	return []

articlesIndex = parseIndex(INDEX_PAGE)

words = []

for article in articlesIndex:
	a = parseArticle(article)
	if a and a not in words:
		words.append(a)

for a in words:
	print(a[0]+"; "+a[0]+"; m.sg.nom; adj")
	print(a[0]+"; "+a[1]+"; f.sg.nom; adj")
	print(a[0]+"; "+a[2]+"; nt.sg.nom; adj")
	print(a[0]+"; "+a[11]+"; m.pl.nom; adj")
	print(a[0]+"; "+a[12]+"; f.pl.nom; adj")
	print(a[0]+"; "+a[13]+"; nt.pl.nom; adj")
	print(a[0]+"; "+a[3]+"; m.sg.acc; adj")
	print(a[0]+"; "+a[4]+"; f.sg.acc; adj")
	print(a[0]+"; "+a[2]+"; nt.sg.acc; adj")
	print(a[0]+"; "+a[14]+"; m.pl.acc; adj")
	print(a[0]+"; "+a[12]+"; f.pl.acc; adj")
	print(a[0]+"; "+a[13]+"; nt.pl.acc; adj")
	print(a[0]+"; "+a[5]+"; m.sg.dat; adj")
	print(a[0]+"; "+a[6]+"; f.sg.dat; adj")
	print(a[0]+"; "+a[7]+"; nt.sg.dat; adj")
	print(a[0]+"; "+a[15]+"; m.pl.dat; adj")
	print(a[0]+"; "+a[15]+"; f.pl.dat; adj")
	print(a[0]+"; "+a[15]+"; nt.pl.dat; adj")
	print(a[0]+"; "+a[8]+"; m.sg.gen; adj")
	print(a[0]+"; "+a[9]+"; f.sg.gen; adj")
	print(a[0]+"; "+a[10]+"; nt.sg.gen; adj")
	print(a[0]+"; "+a[16]+"; m.pl.gen; adj")
	print(a[0]+"; "+a[16]+"; f.pl.gen; adj")
	print(a[0]+"; "+a[16]+"; nt.pl.gen; adj")

