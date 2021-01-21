#функция получения текста страницы
def get_html(url):
    r = requests.get(url)
    return r.text
	
#функция получения количества страниц
def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')    
        total_pages = pages.split('=')[1].split('&')[0]
    except:
        total_pages = 1
    return int(total_pages)
	
