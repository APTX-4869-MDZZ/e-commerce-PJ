import requests
from bs4 import BeautifulSoup
import webbrowser
import sinaweibopy3
import json
import urllib
from requests.cookies import RequestsCookieJar
from time import sleep
import codecs

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
cookie_jar = RequestsCookieJar()
cookie_jar.set("SUB", "_2A25w_0WkDeRhGeBO61sV8C3PyTuIHXVTjTBsrDV_PUNbm9AfLUbukW9NSioogRlevQs0U0wl6XO624qxkcxnCl5k")
def get_2days_hot():
  day2_hot = requests.get('https://tophub.today/n/VaobJ98oAj', headers=headers, cookies=cookie_jar)
  return day2_hot

hot_page = get_2days_hot()
with open('2days.html', 'w', encoding='utf-8') as file:
  file.write(hot_page.text)
hot_html = BeautifulSoup(hot_page.text, 'html.parser')
hot_items = hot_html.find_all('tr')
for i, hot_item in enumerate(hot_items):
  answer_file = codecs.open('weibo_data/'+str(i)+'.txt', 'w', 'utf-8')
  title = hot_item.find('a').text
  question_url = hot_item.find('a')['href']
  question_hot = hot_item.find_all('td')[2].text
  hot_time = hot_item.find_all('td')[0].text
  question_dict = dict()
  question_dict['title'] = title
  question_dict['hot'] = question_hot
  question_dict['hot_time'] = hot_time
  
  try_times = 0
  while True:
    try:
      try_times = try_times + 1
      question_page = requests.get(question_url, headers=headers)
      
      question_html = BeautifulSoup(question_page.text, 'html.parser')
      title_seg = question_html.find('div', attrs={'action-type': True, 'mid': True})
      question_dict['mid'] = title_seg['mid']
      description = title_seg.find('div', 'card').text
      question_dict['description'] = description
      sleep(3)
      break
    except Exception as e:
      if try_times == 4:
        break
      print(e)
      print('sleepingggggg.')
      sleep(60)
  answer_file.write(json.dumps(question_dict, ensure_ascii=False))
