import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from time import sleep
import time
import json
import re
import codecs

headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'user-agent': ': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
  'cookie': '_zap=4c840422-3c05-430f-821d-fecd9fe245a5; _xsrf=c2d0ef41-ecce-4fac-a211-d20638a185e2; d_c0="AACl-01IhhCPTgY5ztkhzdUNjkIlqPr5Y4Q=|1576669448"; tgw_l7_route=66cb16bc7f45da64562a077714739c11; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1576745671,1576745870,1576758370,1576759998; capsion_ticket="2|1:0|10:1576760010|14:capsion_ticket|44:OTU1OThmZDAyYWQyNGQyOWFmNGU2M2QyYmFmNTY0YjI=|7f237e311a50fdb0867308e5b4418b5e9abedadae3bb0c1b756d5480c9f45f1e"; z_c0="2|1:0|10:1576760038|4:z_c0|92:Mi4xMXIzMkFRQUFBQUFBQUtYN1RVaUdFQ1lBQUFCZ0FsVk41Y0RvWGdDMWRxMEpGSW5GNUZvdlE0bVpHOE91eUczNUl3|8a822fc33ae8743301b3ed9768526fd2a2d10b3d057984a9edfd86e1dca70dc9"; unlock_ticket="ABCM5N-ShQgmAAAAYAJVTe15-11y77N73oufrIYPrsYBe8jCWKjL0A=="; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1576760049; anc_cap_id=2d040b8e3791483f8784274bae2088bf'
}
cookie_jar = RequestsCookieJar()
cookie_jar.set("z_c0", "2|1:0|10:1576760038|4:z_c0|92:Mi4xMXIzMkFRQUFBQUFBQUtYN1RVaUdFQ1lBQUFCZ0FsVk41Y0RvWGdDMWRxMEpGSW5GNUZvdlE0bVpHOE91eUczNUl3|8a822fc33ae8743301b3ed9768526fd2a2d10b3d057984a9edfd86e1dca70dc9")
get_answer_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=2&offset={}&platform=desktop&sort_by=default'

for i in range(63, 64):
  with open('zhihu_data/'+str(i)+'.txt', 'r', encoding='utf-8') as file:
    question_id = json.loads(file.readline()).get('id', None)
  if not question_id:
    continue

  answer_file = codecs.open('zhihu_data/'+str(i)+'.txt', 'a', 'utf-8')
  for offset in range(0, 20, 2):
    while True:
      try:
        answer_res = requests.get(get_answer_url.format(question_id, offset), headers=headers)
        if len(json.loads(answer_res.text)['data']) == 0:
          break
        answer_file.write(json.dumps(json.loads(answer_res.text)['data'], ensure_ascii=False) + '\n')
        sleep(3)
        break
      except Exception as e:
        print(e)
        print('sleepinggggg')
        sleep(20)
    if len(json.loads(answer_res.text)['data']) == 0:
      break
  print(i+1, 'question get!')