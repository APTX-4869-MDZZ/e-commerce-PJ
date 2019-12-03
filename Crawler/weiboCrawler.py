import requests
from bs4 import BeautifulSoup
import webbrowser
import sinaweibopy3
import json
import urllib
from requests.cookies import RequestsCookieJar
import time

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
summary_response = requests.get('http://s.weibo.com/top/summary?cate=realtimehot', headers=headers)
summary_html = BeautifulSoup(summary_response.text, 'html.parser')
hot_spot_td = summary_html.find_all('td', 'td-02')
hot_spot_a = [td.a for td in hot_spot_td]
hot_spots = list()
for hot_spot in hot_spot_a:
  hot_spots.append({
    'url': hot_spot['href'],
    'content': hot_spot.text
  })


# APP_KEY = '4278710059'
# APP_SECRET = '9065fb6f674b1d1203afb99f8b5c0156'
# REDIRECT_URL = 'http://api.weibo.com/oauth2/default.html'
# client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
# url = client.get_authorize_url()
# webbrowser.open_new(url)
# result = client.request_access_token(
#   input("please input code : "))
# print(result)
# client.set_access_token(result.access_token, result.expires_in)
# count = 200

cookie_jar = RequestsCookieJar()
cookie_jar.set("SUB", "_2A25w3ks7DeRhGeBO61sV8C3PyTuIHXVTqjvzrDV8PUNbmtBeLXWskW9NSioogSz1M0OUzPuxytkj106GYKwpCl39")
for i, hot_spot in enumerate(hot_spots):
  quote_hot = '#'+hot_spot['content']+'#'
  encode_hot = urllib.parse.quote(quote_hot)
  hot_spots_weibo = []
  for page in range(10):
    hot_weibo_page = requests.get('https://s.weibo.com/hot?q={}&xsort=hot&suball=1&tw=hotweibo&Refer=weibo_hot&page={}'.format(encode_hot, page), headers=headers, cookies=cookie_jar)
    hot_weibo_html = BeautifulSoup(hot_weibo_page.text, 'html.parser')
    cards = hot_weibo_html.find_all('div', 'card-wrap')
    for card in cards:
      if card.find('p') and card.get('mid'):
        print(card.find('p').text)
        hot_spots_weibo.append({
          'id': card['mid'],
          'content': card.find('p').text
        })
    time.sleep(2)
  with open('weibo_data/{}.json'.format(i), 'w', encoding='utf-8') as file:
    file.write(json.dumps({'title': hot_spot['content'], 'weibos': hot_spots_weibo}, ensure_ascii=False))
