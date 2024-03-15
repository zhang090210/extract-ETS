import json
from argparse import Namespace
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
            BeautifulSoup(data, 'html.parser').get_text()
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

    def __init__(self, data: dict, args: Namespace) -> None:
        self.data = data
        self.textual = [
            data.replace("</p>", "")
            for data in self.data['info']['value'].replace("<p>", "").split("</p>")
        ]
        if args.answer_sorted:
            self.questions = self.parse(sort=True, role_answers_limit=args.role_answers_limit)
        else:
            self.questions = self.parse(role_answers_limit=args.role_answers_limit)

    def parse(self, role_answers_limit: int, sort: bool = False) -> list:
        resu = []
        for question in self.data['info']['question']:
            answers = [
                answer['value']
                for answer in question['std']
            ]
            if sort:
                answers.sort(key=len)
            ques = {
                'stem': question['ask'],
                'answer': answers[:role_answers_limit]
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
    def from_json(cls, data: str, args: Namespace):
        contents: dict = json.loads(data)
        match contents['structure_type']:
            case "collector.choose":
                return Choose(contents)
            case "collector.role":
                return Role(contents, args)
            case "collector.picture":
                return Picture(contents)
            case "collector.read":
                return Read(contents)
