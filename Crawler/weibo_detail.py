import sinaweibopy3
import json
import webbrowser
import time
import codecs

APP_KEY = '4278710059'
APP_SECRET = '9065fb6f674b1d1203afb99f8b5c0156'
REDIRECT_URL = 'http://api.weibo.com/oauth2/default.html'
client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
url = client.get_authorize_url()
webbrowser.open_new(url)
result = client.request_access_token(
  input("please input code : "))
print(result)
client.set_access_token(result.access_token, result.expires_in)

for i in range(1):
  detail_file = codecs.open('weibo_detail/{}.json'.format(i), 'a', 'utf-8')
  weibo_detail = []
  with open('2019-11-24-23-05/weibo_data/{}.json'.format(i), 'r', encoding='utf-8') as file:
    weibos = json.loads(file.read())['weibos']
  for weibo in weibos[75:]:
    # mids = [weibo['id'] for weibo in weibos[j * 50: min(j*50+50, weibo_nums)]]
    # mids = ','.join(mids)
    mid = int(weibo['id'])
    detail = client.get.comments__show(id=mid, count=1)
    
    detail_file.write(json.dumps(detail.get('status', {}), ensure_ascii=False))
    time.sleep(3)
  detail_file.close()

# for i in range(51):
#   weibo_detail = []
#   with open('2019-11-24-23-05/weibo_data/{}.json'.format(i), 'r', encoding='utf-8') as file:
#     weibos = json.loads(file.read())['weibos']
#     weibo_nums = len(weibos)
#   for j in range(weibo_nums // 50):
#     mids = [weibo['id'] for weibo in weibos[j * 50: min(j*50+50, weibo_nums)]]
#     mids = ','.join(mids)
#     detail = client.get.statuses__show_batch(ids=mids)
#     print(detail)
#     weibo_detail.extend(detail)
#     time.sleep(3)
#   with open('weibo_detail/{}.json'.format(i), 'w', encoding='utf-8') as file:
#     file.write(json.dumps(weibo_detail, ensure_ascii=False))

