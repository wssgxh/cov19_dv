import requests

kw = {'wd': '长城'}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


response = requests.get("https://www.reddit.com/r/Coronavirus/comments/et53d8/reassurance_for_you_guys/", params=kw, headers=headers)




print(response.text)