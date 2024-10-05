from dataclasses import dataclass

@dataclass
class ChooseAndFilled:
    PaperID: int
    SecID: int
    ItemID: int
    EntityID: int
    Order: int
    Score: int
    MaxScore: int
    Choose: str
    Answer: str
    IsUpdated: bool
    RecordTime: str

@dataclass
class TopicAndRead:
    ItemID: int
    Publishid: str
    PaperID: int
    SecID: int
    Score_max: float
    Content: str
    Content_bz: str
    Translate: str
    Analyze: str
    Symbol_ifly: str
    Symbol_split: str
    Symbol_std: str
    AudioFilename: str
    ImgFilename: str
    BeginTime: float
    EndTime: float
    Role: str

@dataclass
class Choose(ChooseAndFilled):
    """听后选择"""

@dataclass
class FillInTheBlank(ChooseAndFilled):
    """听后填空"""

@dataclass
class Topic(TopicAndRead):
    """听后记录"""

@dataclass
class ReadChapter(TopicAndRead):
    """短文朗读"""