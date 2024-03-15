import os
import sys
from typing import Union

import dominate
from dominate.tags import *
import pdfkit

from get_data import *


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def to_html(aws: list, save_path: Union[None, str] = None):
    chooses = []
    roles = []
    pictures = []
    reads = []
    for answer in aws:
        match answer:
            case Choose():
                chooses.append(answer)
            case Role():
                roles.append(answer)
            case Picture():
                pictures.append(answer)
            case Read():
                reads.append(answer)

    doc = dominate.document(title="result")
    with doc.head:
        meta(charset="utf-8")
    with doc.body:
        h1("听后选择")
        for choose in chooses:
            h2("原文：")
            for textual in choose.textual:
                p(textual)
            for c in choose.questions:
                h3(c['stem'])
                for option in c['options']:
                    p(option)
                h4(f"Answer: {c['answer']}")
                br()
            br()
        h1("听后回答")
        for role in roles:
            h2("原文")
            for textual in role.textual:
                p(textual)
            for ro in role.questions:
                h3(ro['stem'])
                for answer in ro['answer']:
                    p(answer)
            br()
        br()
        h1("听后转述")
        for picture in pictures:
            for answer in picture.answers:
                p(answer)
                br()
            br()
        h1("朗读短文")
        for read in reads:
            p(read.textual)

    if save_path is None:
        return doc.render()
    elif isinstance(save_path, str):
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(doc.render())


def to_pdf(aws: list, save_path, args: Namespace):
    doc = to_html(aws)
    # 将wkhtmltopdf.exe程序绝对路径传入config对象
    path_wkhtmltopdf = r"include\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=get_resource_path(path_wkhtmltopdf))
    # 生成pdf文件，to_file为文件路径
    pdfkit.from_string(doc, save_path, configuration=config, verbose=args.verbose)
