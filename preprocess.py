import codecs
import json

for i in range(216):
    zhihu_data = codecs.open('zhihu_data/'+str(i)+'.txt', 'r', 'utf-8')
    question_line = zhihu_data.readline()
    if len(question_line) == 0:
        continue
    question = json.loads(question_line)
    answers = []
    j = 0
    for answers_line in zhihu_data.readlines():
        try:
            sub_answers = json.loads(answers_line)
            answers.extend(sub_answers)
        except:
            print(i, j)
            print(sub_answers[0]['content'][0:20])
            raise RuntimeError('testError')
        j += 1
    zhihu_data.close()
    question['answers'] = answers
    with open('zhihuData/'+str(i)+'.txt', 'w', encoding='utf-8') as file:
        file.write(json.dumps(question, ensure_ascii=False))