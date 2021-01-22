'''
module to parse some data from www.avito.ru
'''
import re

import json
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_random_user_agent():
	response = requests.get('https://fake-useragent.herokuapp.com/browsers/0.1.11')
	agents_dictionary = json.loads(response.text)
	random_browser_number = str(random.randint(0, len(agents_dictionary['randomize'])))
	random_browser = agents_dictionary['randomize'][random_browser_number]
	user_agents_list = agents_dictionary['browsers'][random_browser]
	user_agent = user_agents_list[random.randint(0, len(user_agents_list)-1)]	
	return {'User-Agent': user_agent}

def get_html(url):
	'''
	get text function
	#функция получения текста страницы
	'''
	headers = get_random_user_agent()
	req = requests.get(url, headers = headers)
	return req.text

def get_total_pages(html):
	'''
	func rerurns number of pages
	функция получения количества страниц
	'''
	soup = BeautifulSoup(html, 'lxml')
	try:
		pages = soup.find('div', class_='pagination-pages')\
			.find_all('a', class_='pagination-page')[-1].get('href')
		total_pages = pages.split('=')[1].split('&')[0]
	except AttributeError:
		total_pages = 1
	return int(total_pages)


def get_page_data(html, df):
	'''
	function returns dataframe with data - id, price, url and location
	'''
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('div',class_=re.compile('^items-items'))\
		.find_all('div', class_=re.compile('^iva-item-body-'))
	for ad in ads:
		try:
			#title = ad.find('div', class_ = 'description').find('h3').text.strip()
			title = ad.find('span',class_=re.compile('^title-root')).text.strip()
		except AttributeError:
			title = ''
		try:
			#url = ad.find('div', class_ = 'description').find('h3').find('a').get('href')
			url = ad.find('a',class_=re.compile('^link-link'))['href'] #.text.strip()
		except TypeError:
			url = ''
		try:
			price = int(ad.find('meta',itemprop='price')['content'])
		except TypeError:
			price = 0 #заменить на Nan
		try:
			#id_=int(ad.get("id").replace('i',''))
			id_ = int(url.split('/')[-1].split('?')[0].split('_')[-1])
		except ValueError:
			id_ = 0
		try:
			#id_=int(ad.get("id").replace('i',''))
			location = ad.find('div',class_=re.compile('^geo-root')).find('span').find('span').text.strip()
		except AttributeError:
			location = 'unknown'
		data = {
			'id_': id_,
			'title': title,
			'price': price,
			'url': 'https://www.avito.ru' + url,
			'location': location,
		}
		#write_csv(data)
		#add_to_df(data)

		if df[df.index == data['id_']]['id_'].count() == 0:
			#print(data['id_'])
			sr = pd.Series(data, name=data['id_'])
			df = df.append(sr)

	return df
