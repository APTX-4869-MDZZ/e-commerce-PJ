import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from time import sleep
import json
import re
import codecs

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'user-agent': ': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
  'cookie': '_zap=775904c7-650c-49cc-a58e-16f0801e92d5; d_c0="AFDu7XwQWBCPTljIztnS-_L2AyijmBAJj10=|1573567809"; _xsrf=gr8hNhot8mvpKAYl2nOGxxxBSLluiZd6; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1573026345,1573482896,1573537949,1573567912; capsion_ticket="2|1:0|10:1573570033|14:capsion_ticket|44:MjIzOWNjODM5MzBiNGIwYjg4MGY3NDc2NGFkOTk5ZTk=|4d7696b5a11b756bb78450c1b678b7ed04ffb85c2de46f0f95670d4f9f13d3ef"; z_c0="2|1:0|10:1573570047|4:z_c0|92:Mi4xMXIzMkFRQUFBQUFBVU83dGZCQllFQ1lBQUFCZ0FsVk5feE80WGdCbnh0WGp5RXVpRXpoVzJuUldoQjIxUjZwQzZn|ad171eab66492267ef55551ebb067a7580d494083ee984729ef04285b8f93606"; tgw_l7_route=116a747939468d99065d12a386ab1c5f; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1573610499; tst=h; tshl='
}
cookie_jar = RequestsCookieJar()
cookie_jar.set("z_c0", "2|1:0|10:1573570047|4:z_c0|92:Mi4xMXIzMkFRQUFBQUFBVU83dGZCQllFQ1lBQUFCZ0FsVk5feE80WGdCbnh0WGp5RXVpRXpoVzJuUldoQjIxUjZwQzZn|ad171eab66492267ef55551ebb067a7580d494083ee984729ef04285b8f93606:FG=1")

def get_3days_hot():
  day3_hot = requests.get('https://tophub.today/n/mproPpoq6O', headers=headers, cookies=cookie_jar)
  return day3_hot
  
get_answer_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=20&offset={}&platform=desktop&sort_by=default'

hot_page = get_3days_hot()
with open('3days.html', 'w', encoding='utf-8') as file:
  file.write(hot_page.text)
hot_html = BeautifulSoup(hot_page.text, 'html.parser')
hot_items = hot_html.find_all('tr')
for i, hot_item in enumerate(hot_items):
  answer_file = codecs.open('zhihu_data/'+str(i)+'.txt', 'w', 'utf-8')
  title = hot_item.find('a').text
  question_url = hot_item.find('a')['href']
  question_hot = hot_item.find_all('td')[2].text
  hot_time = hot_item.find_all('td')[0].text
  if not re.match(r'https://www.zhihu.com/question/(.*)', question_url):
    continue
  question_id = re.match(r'https://www.zhihu.com/question/(.*)', question_url).groups()[0]
  
  try_times = 0
  while True:
    try:
      try_times += 1
      question_page = requests.get(question_url, headers=headers, cookies=cookie_jar)
      
      question_html = BeautifulSoup(question_page.text, 'html.parser')
      if question_html.find('div', attrs={'data-zop-question': True}):
        title_seg = question_html.find('div', attrs={'data-zop-question': True})['data-zop-question']
        question_dict = json.loads(title_seg)
        question_script = question_html.find('script', id='js-initialData').text
        question_script = json.loads(question_script)
        question_detail = question_script['initialState']['entities']['questions']
        question_dict['description'] = list(question_detail.values())[0]['detail']
      else:
        question_dict = dict()
        question_dict['title'] = title
      question_dict['hot'] = question_hot
      question_dict['hot_time'] = hot_time
      break
    except Exception as e:
      if try_times == 4:
        break
      print(e)
      print('sleepinggggg')
      sleep(60)
    
  answer_file.write(json.dumps(question_dict, ensure_ascii=False) + '\n')
