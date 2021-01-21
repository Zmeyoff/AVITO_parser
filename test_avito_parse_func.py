from avito_parse_func import get_total_pages, get_page_data
import pandas as pd

def test_import_modile():
	import avito_parse_func
	from avito_parse_func import get_total_pages, get_page_data
	
	
def test_get_html():
	pass
	
	
def test_get_total_pages():
	with open("kotofey_html3.html", encoding='utf-8') as fin:
		htm = fin.read()
	cnt = get_total_pages(htm)
	
	expected_val = 100
	
	assert expected_val == cnt
	
	
def test_get_total_pages():	
	htm = '<a>hello</a>'
	cnt = get_total_pages(htm)

	expected_val = 1
	
	assert expected_val == cnt
	
def test_get_page_data():
	with open("kotofey_html3.html", encoding='utf-8') as fin:
		htm = fin.read()
	df = pd.DataFrame(columns=['title', 'price', 'url', 'id_', 'location'])
	df_val = get_page_data(htm, df)
	
	expected_val = 51
	
	assert expected_val == df_val['id_'].count()
	
def test_get_page_data_with_empty_doc():
	htm = '<div class="items-items-sdsa><div class="iva-item-body-asfasas"></div></div>"'
	df = pd.DataFrame(columns=['title', 'price', 'url', 'id_', 'location'])
	df_val = get_page_data(htm, df)
	
	expected_val = 0
	
	assert expected_val == df_val['id_'].count()