import sinaweibopy3
import json
import webbrowser
from time import sleep
import codecs

keys = ['4278710059', '152557326', '646317177', '2507409448', '1006844052', '4052393024', '3777270742', '3181433703', '1744249797', '2606580009']
secrets = ['9065fb6f674b1d1203afb99f8b5c0156', '6945fe41a4796de948ab2174a403812c', '81aa30fe112ed9bebed31b5130b3e2d1', 
  '5e9e0c40e9219b83442bedaaaa4d2a5c', 'd58e7f4aa8aa8ccd5fa231d118cc94df', 'b138a3ec2d48ea1416da1e80c8e36614', '6ad2cee33ca07c5f74574d06f21ede2c',
  '906110cba1b9b0af5d1705dabc13e5b9', '59d41e7f9ceb96a944d75e17826f1053', '1d45d42c21f8e94777d506d83f22464c']
APP_KEY = keys[9]
APP_SECRET = secrets[9]
REDIRECT_URL = 'http://api.weibo.com/oauth2/default.html'
client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
url = client.get_authorize_url()
webbrowser.open_new(url)
result = client.request_access_token(
  input("please input code : "))
print(result)
client.set_access_token(result.access_token, result.expires_in)

for i in range(165, 166):
  with open('weibo_data/{}.txt'.format(i), 'r', encoding='utf-8') as file:
    try:
      mid = json.loads(file.readline())['mid']
    except:
      continue
  detail_file = codecs.open('weibo_data/{}.txt'.format(i), 'a', 'utf-8')
  weibo_detail = []
  for page in range(1, 11):
    while True:
      try:
        detail = client.get.comments__show(id=mid, count=200, page=page)
        if len(detail) == 0:
          break
        detail_file.write('\n'+json.dumps(detail, ensure_ascii=False))
        sleep(5)
        break
      except Exception as e:
        print(e)
        print('sleepinggg')
        sleep(10)
  detail_file.close()
