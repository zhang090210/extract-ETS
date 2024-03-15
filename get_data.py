import json
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup


# 听后选择的类型
@dataclass
class Choose:
    textual: list
    questions: list

    def __init__(self, data: dict) -> None:
        self.data = data
        self.textual = [
            BeautifulSoup(data,'html.parser').get_text()
            for data in self.data['info']['st_nr'].split("</p>")
        ]
        self.questions = self.parse()

    def parse(self) -> list:
        resu = []
        for question in self.data['info']['xtlist']:
            options = [
                "{}.{}".format(option['xx_mc'], option['xx_nr'])
                for option in question['xxlist']
            ]
            ques = {
                'stem': BeautifulSoup(question['xt_nr'], 'html.parser').get_text(),
                'answer': question['answer'],
                'options': options
            }
            resu.append(ques)
        return resu


@dataclass
class Role:
    textual: list
    questions: list

    def __init__(self, data: dict) -> None:
        self.data = data
        self.textual = [
            data.replace("</p>", "")
            for data in self.data['info']['value'].replace("<p>", "").split("</p>")
        ]
        self.questions = self.parse()

    def parse(self) -> list:
        resu = []
        for question in self.data['info']['question']:
            answers = [
                answer['value']
                for answer in question['std']
            ]
            ques = {
                'stem': question['ask'],
                'answer': answers
            }
            resu.append(ques)
        return resu


@dataclass
class Picture:
    textual: list
    answers: list

    def __init__(self, data: dict) -> None:
        self.data = data
        self.textual: list = [
            data.replace("</p>", "")
            for data in self.data['info']['value'].replace("<p>", "").split("</p>")
        ]
        self.answers = self.parse()

    def parse(self) -> list:
        ans = []
        for answer in self.data['info']['std']:
            ans.append(answer['value'])
        return ans


@dataclass
class Read:
    textual: str

    def __init__(self, data: dict) -> None:
        self.data = data
        self.textual: str = self.data['info']['value'].replace("<p>", "").replace("</p>", "")


class QuestionType(Enum):
    choose = 0
    role = 1
    picture = 2
    read = 3

    @classmethod
    def from_json(cls, data: str):
        contents: dict = json.loads(data)
        match contents['structure_type']:
            case "collector.choose":
                return Choose(contents)
            case "collector.role":
                return Role(contents)
            case "collector.picture":
                return Picture(contents)
            case "collector.read":
                return Read(contents)
