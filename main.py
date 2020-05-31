import time
import os
import json
import requests
import webbrowser

from functions import log
##from pyecharts import Map
from pyecharts import Map
from bs4 import BeautifulSoup


def save_daily_MOH_data():

	path = "source_data/MOH_webpage/MOH_" + str(time.strftime("%Y_%m_%d", time.localtime())) + '.txt'
	url = "https://www.moh.gov.sg/covid-19"

	data = requests.get(url)
	soup= BeautifulSoup(data.content, "html5lib")

	#print(soup)

	div_dict = {'Active Cases':'ContentPlaceHolder_contentPlaceholder_C072_Col00',
				'Discharged':'ContentPlaceHolder_contentPlaceholder_C072_Col01',
				'Discharge to Isolation':'ContentPlaceHolder_contentPlaceholder_C073_Col00',
				'Hospitalised (Stable)':'ContentPlaceHolder_contentPlaceholder_C073_Col01',
				'Hospitalised (Critical)':'ContentPlaceHolder_contentPlaceholder_C073_Col02',
				'Deaths':'ContentPlaceHolder_contentPlaceholder_C073_Col03'
				}

	result_dict = {}
	result_dict['date'] = time.strftime("%Y_%m_%d", time.localtime())

	for key in (div_dict.keys()):

		data = soup.find('div',id=div_dict[key]).b.get_text().replace(',',"")
		result_dict[key] = data

	print(result_dict)

	f = open(path, mode='w', encoding="utf-8")
	f.write(str(result_dict))
	f.close()



def save_daily_source_data(data):

    path = "source_data/Tencent_news/" + str(time.strftime("%Y_%m_%d", time.localtime())) + '.txt'

    #if (os.path.isfile(path)) == False:
    if False == False:

        f = open(path, mode='w',encoding="utf-8")

        data = str(data).replace("\'", "\"").replace("False","\"False\"").replace("True","\"True\"").replace("None","\"None\"")

        #print(data)

        f.write(str(data))

        f.close()
        log("0011",None,"Successfully save today's data")

def catch_distribution():
    """take source data from Tencent news"""

    result = dict()
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback'
    data = json.loads(requests.get(url=url).json()['data'])

    save_daily_source_data(data)

    for item in data['areaTree'][0]['children']:

        if item['name'] not in result:
            result.update({item['name']: 0})
        for city in item['children']:
            result[item['name']] = int(city['total']['confirm']) + result[item['name']]

    log("0021", None, "get data from Tencent news")
    return result



province_distribution = catch_distribution()
save_daily_MOH_data()

provice = list(province_distribution.keys())
values = list(province_distribution.values())
map = Map("China", '', width=1200, height=600)
map.add("Province", provice, values, visual_range=[0, 6000], maptype='china', is_visualmap=True,is_map_symbol_show=False,
        visual_text_color='#000')
map.render(path="China Map.html")
log("0031", None, "China Map Saved")



