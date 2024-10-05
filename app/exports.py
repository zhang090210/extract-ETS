import pdfkit
from markdown import markdown
from bs4 import BeautifulSoup

from .question_type import *

def export_to_markdown(title, results, export_path = None):
    text = ""
    text += f"# {title}\n"
    for idx, result in enumerate(results):
        if isinstance(result, Choose):
            if idx == 0:
                text += "## 听后选择1\n"
            elif idx == 4:
                text += "## 听后选择2\n"
            text += f"{idx+1}. {result.Answer}\n"
        elif isinstance(result, FillInTheBlank):
            if idx == 14:
                text += "## 听后记录\n"
            text += f"{idx+1}. {result.Answer}\n"
        elif isinstance(result, Topic):
            text += f"## 听后转述\n"
            content = BeautifulSoup(result.Content, 'lxml')
            text += f"{''.join([i.text for i in content])}\n"
        elif isinstance(result, ReadChapter):
            text += f"## 短文朗读并回答问题\n"
            content = BeautifulSoup(result.Content, 'lxml')
            text += f"{''.join([i.text for i in content])}\n"
        else:
            raise ValueError("Invalid question type")
        idx += 1
    
    if export_path is None:
        return text
    else:
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(text)

def export_to_pdf(title, results, export_path = None):
    text = markdown(export_to_markdown(title, results))
    print(text)
    if export_path is None:
        return None
    else:
        htmltopdf = r'.\\includes\\wkhtmltopdf.exe'
        configuration = pdfkit.configuration(wkhtmltopdf=htmltopdf)
        pdfkit.from_string(text, export_path, configuration=configuration, options={'encoding': 'utf-8'})