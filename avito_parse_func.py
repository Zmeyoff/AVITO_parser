import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_html(url):
	'''
	get text function
	#функция получения текста страницы
	'''
	r = requests.get(url)
	return r.text
	
def get_total_pages(html):
	'''+
	функция получения количества страниц
	'''
	soup = BeautifulSoup(html, 'lxml')
	try:
		pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')    
		total_pages = pages.split('=')[1].split('&')[0]
	except:
		total_pages = 1
	return int(total_pages)
	
	
def get_page_data(html, df):
	
    soup = BeautifulSoup(html, 'lxml')    
    ads = soup.find('div',class_=re.compile('^items-items')).find_all('div', class_=re.compile('^iva-item-body-'))
    for ad in ads:
        try:
            #title = ad.find('div', class_ = 'description').find('h3').text.strip()
            title = ad.find('span',class_=re.compile('^title-root')).text.strip()
        except:
            title = ''
        try:
            #url = ad.find('div', class_ = 'description').find('h3').find('a').get('href')
            url = ad.find('a',class_=re.compile('^link-link'))['href'] #.text.strip()
        except:
            url = ''
        try:
            #price = int(ad.find('div', class_ = 'about').text.strip().replace(' руб.', '').replace(' ', '').replace('₽', ''))
            price = int(ad.find('meta',itemprop='price')['content'])
        except:
            price = 0 #заменить на Nan
        try:
            #id_=int(ad.get("id").replace('i',''))
            id_ = int(url.split('/')[-1].split('?')[0].split('_')[-1])
        except:
            id_ = 0
        try:
            #id_=int(ad.get("id").replace('i',''))
            location = ad.find('div',class_=re.compile('^geo-root')).find('span').find('span').text.strip()
        except:
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
