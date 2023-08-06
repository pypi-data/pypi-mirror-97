#Python modules
import requests
import bs4
import pandas as pd
import numpy

#Local imports
from . import container
from . import exceptions


def scrapePrice(tickerSymbol):
	r = requests.get('https://finance.yahoo.com/quote/' + tickerSymbol)
	soup = bs4.BeautifulSoup(r.text, 'lxml')
	price = soup.find('div', {'class':'D(ib) Mend(20px)'}).find('span').text

	return price


def scrapeCallOptions(tickerSymbol):
	#Load the webpage content
	url = 'https://finance.yahoo.com/quote/' + tickerSymbol + '/options?p=' + tickerSymbol
	r = requests.get(url) 

	#Convert to bs object
	webpage = bs4.BeautifulSoup(r.content, features='lxml')

	date = webpage.select('section > section > div > span', {'datareactid':'47'})[2].text

	#Scrape data
	tables = webpage.select('table', attrs={'datareactid':'50'})

	callTable = tables[0]
	putTable = tables[1]

	columns = callTable.find('thead').findAll('th')
	columnNames = [c.text for c in columns]


	rows = callTable.find('tbody').findAll('tr')
	optionMatrix = []

	for row in rows:
		tds = row.findAll('td')
		option = [td.get_text() for td in tds]
		optionMatrix.append(option)

	try:
		df = pd.DataFrame(optionMatrix, columns=columnNames)
		if len(df.index) == 0:
			raise exceptions.EmptyOptionChainError
	except exceptions.EmptyOptionChainError:
		print("Scraped option chain was empty")

	optionObj = container.OptionObj(df, date, scrapePrice(tickerSymbol))

	return optionObj

def scrapePutOptions(tickerSymbol):
	#load the webpage content
	url = 'https://finance.yahoo.com/quote/' + tickerSymbol + '/options?p=' + tickerSymbol
	r = requests.get(url)

	webpage = bs4.BeautifulSoup(r.content, features='lxml')

	date = webpage.select('section > section > div > span', {'datareactid':'47'})[2].text

	tables = webpage.select("table", attrs={'datareactid':'50'})

	putTable = tables[1]

	columns = putTable.find('thead').findAll('th')
	columnNames = [c.get_text() for c in columns]

	rows = putTable.find('tbody').findAll('tr')
	optionMatrix = []

	for row in rows:
		tds = row.findAll('td')
		option = [td.get_text() for td in tds]
		optionMatrix.append(option)

	try:
		df = pd.DataFrame(optionMatrix, columns=columnNames)
		if len(df.index) == 0:
			raise exceptions.EmptyOptionChainError
	except exceptions.EmptyOptionChainError:
		print("Scraped option chain was empty")

	optionObj = container.OptionObj(df, date, scrapePrice(tickerSymbol))

	return optionObj

def scrapeAggregateOptions(tickerSymbol):
	#load the webpage content
	url = 'https://finance.yahoo.com/quote/' + tickerSymbol + '/options?p=' + tickerSymbol
	r = requests.get(url)

	webpage = bs4.BeautifulSoup(r.content, features='lxml')

	date = webpage.select('section > section > div > span', {'datareactid':'47'})[2].text

	tables = webpage.select("table", attrs={'datareactid':'50'})

	callTable = tables[0]
	putTable = tables[1]

	put_columns = putTable.find('thead').findAll('th')
	put_columnNames = [c.get_text() for c in put_columns]

	put_rows = putTable.find('tbody').findAll('tr')
	put_optionMatrix = []

	for row in put_rows:
		tds = row.findAll('td')
		option = [td.get_text() for td in tds]
		put_optionMatrix.append(option)

	call_columns = callTable.find('thead').findAll('th')
	call_columnNames = [c.get_text() for c in call_columns]

	call_rows = callTable.find('tbody').findAll('tr')
	call_optionMatrix = []

	for row in call_rows:
		tds = row.findAll('td')
		option = [td.get_text() for td in tds]
		call_optionMatrix.append(option)


	try:
		call_df = pd.DataFrame(call_optionMatrix, columns=call_columnNames)
		put_df = pd.DataFrame(put_optionMatrix, columns = put_columnNames)
		if len(call_df.index) == 0 or len(put_df.index) == 0:
			raise exceptions.EmptyOptionChainError
	except exceptions.EmptyOptionChainError:
		print("Scraped option chain was empty")

	optionObj = container.AggregateOptionObj(call_df, put_df, date, scrapePrice(tickerSymbol)) 

	return optionObj

