import os
import argparse

from generate import *

if __name__ == '__main__':
    # 获取命令行参数
    parser = argparse.ArgumentParser(description="used for test")

    # 添加版本提示
    parser.add_argument('--version', '-V', action='version',
                        version='%(prog)s version : v2.0.0',
                        help='show the version')
    # 指定数据文件路径
    parser.add_argument('--data_path', dest='file_path',
                        type=str, default='.\\data',
                        help='The location where the data files are stored')

    # 指定输出文件路径
    parser.add_argument('--output_path', dest='output_path',
                        type=str, default='.\\output',
                        help='The location where the output files are stored')

    # 指定输出文件名
    parser.add_argument('--output_name', dest='output_name',
                        type=str, default='result',
                        help='The name of the output file')

    parser.add_argument('--output_file_type', dest='output_type',
                        type=str, default='pdf', choices=['pdf', 'html'],
                        help='The name of the output file')

    parser.add_argument('--answer_sorted', dest='answer_sorted', action='store_true',
                        help='Whether to sort the answer by the order of the questions')

    parser.add_argument("--role_answers_limit", dest="role_answers_limit",
                        type=int, default=5,
                        help='The number of answers for listen and answer')

    args = parser.parse_args()

    if not os.path.isdir(args.output_path):
        # 创建文件夹
        os.makedirs(args.output_path)

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
        ans = QuestionType.from_json(content, args)
        answers.append(ans)

    match args.output_type:
        case "pdf":
            to_pdf(answers, save_path=os.path.join(args.output_path, args.output_name + ".pdf"))
        case "html":
            to_html(answers, save_path=str(os.path.join(args.output_path, args.output_name + ".html")))
