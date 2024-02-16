import os

from generate import *

if __name__ == '__main__':
    # 获取所有题目答案文件
    datas = []
    for root, dirs, files in os.walk(".\\data", topdown=False):
        for name in files:
            if name == "content2.json":
                datas.append(os.path.join(root, name))

    answers = []
    for data in datas:
        with open(data, "r", encoding="utf-8") as f:
            content = f.read()
        ans = QuestionType.from_json(content)
        answers.append(ans)

    to_html(answers, "result.html")
    to_pdf(answers)
