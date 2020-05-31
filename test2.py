import json,requests,time,os
from bs4 import BeautifulSoup

path = "source_data/MOH_webpage/" + str(time.strftime("%Y_%m_%d", time.localtime())) + '.txt'
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