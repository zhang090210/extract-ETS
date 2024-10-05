# 获取e听说题库信息
import os
from typing import List, Union
from pathlib import Path
from sqlite3 import Cursor

from dataclasses import dataclass
from typing import Optional

@dataclass
class HomeWorkInfo:
    """表示作业的相关信息及其属性的类."""
    UserNo: str  # 用户编号
    HomeworkID: str  # 作业编号
    Set_ID: str  # 集合编号
    Begin: int  # 作业开始时间
    End: int  # 作业结束时间
    IsFinished: int  # 是否完成标识
    IsExpired: int  # 是否过期标识
    Point: float  # 作业评分
    AvgPoint: float  # 平均分
    TotalPoint: float  # 总分
    Complete: float  # 完成度
    Status: int  # 状态
    Expire: int  # 过期状态
    EssayID: str  # 文章编号
    SeqID: str  # 序列编号
    Exam: int  # 考试标识
    Remark: str  # 备注
    Marked: int  # 标记状态
    NeedMark: int  # 是否需要评分
    ShowAnswerTime: int  # 显示答案时间
    UnitName: str  # 单元名称
    Column: str  # 列名
    Type: int  # 类型
    Name: str  # 作业名称
    Use_time: int  # 使用时间
    Limit_time: Optional[int]  # 假设 Limit_time 可能不存在，因此使用 Optional 类型
    SetType: int  # 设置类型
    Lock: int  # 锁定状态
    FirstColumnID: str  # 第一列编号
    FirstColumnName: str  # 第一列名称
    SetModuleID: str  # 设置模块编号
    SetModuleName: str  # 设置模块名称
    EngineArea: str  # 引擎区域
    Link: str  # 链接
    FollowType: int  # 跟随类型
    Introduction: str  # 介绍
    offline: int  # 离线状态
    ResID: str  # 资源编号
    ShowRank: int  # 显示排名
    Operation: int  # 操作标识
    Competition: int  # 竞争状态
    LastUseTime: int  # 最后使用时间
    SubmitTime: str  # 提交时间
    RegionName: str  # 地区名称
    RejectScore: int  # 拒绝分数
    Overtime: int  # 超时状态
    AllowOvertime: int  # 允许超时状态
    PlanType: str  # 计划类型
    Week: int  # 周数
    HWOrd: float  # 作业顺序
    ParentHWID: str  # 父作业编号
    PlanBegin: int  # 计划开始时间
    Mock: int  # 模拟状态
    DifficultyRate: float  # 难度系数
    PassLine: float  # 及格线
    Pass: int  # 及格状态
    OnSentence: int  # 句子状态
    PractiseCount: int  # 练习次数
    CompleteCount: int  # 完成次数
    IsInstruction: int  # 是否为指导
    InstructionStatus: int  # 指导状态
    pk: int  # 主键        


def get_homeworks_info(cursor: Cursor) -> List[HomeWorkInfo]:
    """
    获取e听说题库信息
    :param cursor: sqlite3.Cursor
    :return: 题库信息
    """
    cursor.execute("SELECT * FROM HomeworkList")
    rows = cursor.fetchall()
    homeworks = []
    for row in rows:
        homework = HomeWorkInfo(*row)
        homeworks.append(homework)
    return homeworks


@dataclass
class PaperInfo:
    """表示试卷的相关信息及其属性的类."""
    PaperID: int  # 试卷编号
    Paper_mc: str
    Paper_jc: str
    Publish_no: str  # 发布编号
    Publish_mc: str  # 发布名称
    Lev1_no: str  # 一级分类编号
    Lev1_mc: str  # 一级分类名称
    Lev2_no: str  # 二级分类编号
    Lev2_mc: str  # 二级分类名称
    FileName: str  # 文件名称
    Section_count: int  # 章节数量
    Item_count: int  # 题目数量
    Category: str  # 分类
    Score_max: float  # 总分
    Paper_order: int  # 试卷顺序
    Interface_sim: str  # 接口相似度

def get_paper_info(cursor: Cursor, set_id: int) -> PaperInfo:
    """
    获取e听说试卷信息
    :param cursor: sqlite3.Cursor
    :return: 试卷信息
    """
    cursor.execute(f"SELECT * FROM Paper WHERE Publish_no = {set_id}")
    row = cursor.fetchone()
    paper = PaperInfo(*row)
    return paper

@dataclass
class SectionInfo:
    """表示章节的相关信息及其属性的类."""
    SecID: int  # 章节编号
    Sec_mc: str  # 章节序号
    PaperID: int  # 试卷编号
    Category: str  # 分类
    Score_max: float  # 总分
    Sec_order: int  # 章节顺序
    Item_count: int  # 题目数量
    SecTypeID: int  # 章节类型编号

def get_section_info(cursor: Cursor, paper_id: int) -> List[SectionInfo]:
    cursor.execute(f"SELECT * FROM Section WHERE Paperid = {paper_id}")
    rows = cursor.fetchall()
    sections = []
    for row in rows:
        section = SectionInfo(*row)
        sections.append(section)
    return sections

if __name__ == '__main__':
    fp = r"C:\Program Files (x86)\ETS"
    homeworks = get_homeworks_info(fp)
    for homework in homeworks:
        print(homework)