import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from PIL import Image 
import base64
from time import sleep
import time
import hmac
from hashlib import sha1
import json
import re

def simulate_login():
  session=requests.session()
  headers={
      'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
  }
  session.headers.update(headers)
  picture=None
  signature=None
  picture_url=None

  message=session.get(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en').json()  
  print(message)
  if message['show_captcha'] == False:
    picture=''
  else:
    picture_url = session.put(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en').json()
    # 采用base64格式将验证码通过图片格式显示出来
    with open('captcha.jpg','wb') as f:
        f.write(base64.b64decode(picture_url['img_base64']))
    image=Image.open('captcha.jpg')
    image.show()
    picture=input('请输入验证码')
    sleep(2)
    message1=session.post(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',data={'input_text':picture}).json()    # post 验证码
    print(message1)

  a=hmac.new('d1b964811afb40118a12068ff74a12f4'.encode('utf-8'),digestmod=sha1)
  a.update('qaz7417417474741'.encode('utf-8'))
  a.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
  a.update(b'com.zhihu.web')
  a.update(str(int(time.time()*1000)).encode())
  signature=a.hexdigest()

  data={
    'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',#'c3cef7c66a1843f8b3a9e6a1e3160e20',
    'grant_type':'password',
    'timestamp':str(int(time.time()*1000)),
    'source':'com.zhihu.web',
    'signature':signature,
    'username':'xxxxxx@sina.com',
    'password':'xxxxxxx',
    'captcha':picture,
    'lang':'en'
  }

  headers = {
      'content-type':'application/x-www-form-urlencoded',
      'x-zse-83':'3_2.0',
      }
  message=session.post(url='https://www.zhihu.com/api/v3/oauth/sign_in', headers=headers, data=data)
  message.encoding='utf-8'
  print(message.text)
  print(json.loads(message.text)['error']['message'])
  hot_page = session.get('https://www.zhihu.com/hot', headers=headers)
  return hot_page


headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'user-agent': ': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
  'cookie': '_zap=775904c7-650c-49cc-a58e-16f0801e92d5; d_c0="AFDu7XwQWBCPTljIztnS-_L2AyijmBAJj10=|1573567809"; _xsrf=gr8hNhot8mvpKAYl2nOGxxxBSLluiZd6; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1573026345,1573482896,1573537949,1573567912; capsion_ticket="2|1:0|10:1573570033|14:capsion_ticket|44:MjIzOWNjODM5MzBiNGIwYjg4MGY3NDc2NGFkOTk5ZTk=|4d7696b5a11b756bb78450c1b678b7ed04ffb85c2de46f0f95670d4f9f13d3ef"; z_c0="2|1:0|10:1573570047|4:z_c0|92:Mi4xMXIzMkFRQUFBQUFBVU83dGZCQllFQ1lBQUFCZ0FsVk5feE80WGdCbnh0WGp5RXVpRXpoVzJuUldoQjIxUjZwQzZn|ad171eab66492267ef55551ebb067a7580d494083ee984729ef04285b8f93606"; tgw_l7_route=116a747939468d99065d12a386ab1c5f; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1573610499; tst=h; tshl='
}
cookie_jar = RequestsCookieJar()
cookie_jar.set("z_c0", "2|1:0|10:1573570047|4:z_c0|92:Mi4xMXIzMkFRQUFBQUFBVU83dGZCQllFQ1lBQUFCZ0FsVk5feE80WGdCbnh0WGp5RXVpRXpoVzJuUldoQjIxUjZwQzZn|ad171eab66492267ef55551ebb067a7580d494083ee984729ef04285b8f93606:FG=1")
def use_cookies():
  hot_page = requests.get('https://www.zhihu.com/hot', headers=headers, cookies=cookie_jar)
  return hot_page
  
get_answer_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'

hot_page = use_cookies()
hot_html = BeautifulSoup(hot_page.text, 'html.parser')
hot_items = hot_html.find_all('section', 'HotItem')
for i, hot_item in enumerate(hot_items):
  question_url = hot_item.a['href']
  hot_name = hot_item.a['title']
  if not re.match(r'https://www.zhihu.com/question/(.*)', question_url):
    continue
  question_id = re.match(r'https://www.zhihu.com/question/(.*)', question_url).groups()[0]
  
  question_page = requests.get(question_url, headers=headers, cookies=cookie_jar)
  question_html = BeautifulSoup(question_page.text, 'html.parser')

  answers = []
  for offset in range(0, 46, 5):
    answer_res = requests.get(get_answer_url.format(question_id, offset), headers=headers)
    answers.extend(json.loads(answer_res.text)['data'])
    sleep(3)
  with open('zhihu_data/'+str(i)+'.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps({'title': hot_name, 'answers': answers}, ensure_ascii=False))