from dataclasses import dataclass
import winreg
import os
import sqlite3
from app.get_info import *
from app.exports import *
from app.parsed import *


class ETS:
    app_path: str
    def __init__(self) -> None:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\ETS")
        self.app_path, _ = os.path.split(winreg.QueryValueEx(key, "DisplayIcon")[0][1:])
        self.conn = sqlite3.connect(os.path.join(self.app_path, 'localdata', 'ETS.db'))
        self.conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        self.cursor = self.conn.cursor()

    def get_homework_list(self) -> HomeWorkInfo:
        return get_homeworks_info(self.cursor)[0]
    
    def get_paper_info(self, set_id: int) -> PaperInfo:
        return get_paper_info(self.cursor, set_id)
    
    def get_section_info(self, paper_id: int) -> List[SectionInfo]:
        return get_section_info(self.cursor, paper_id)[:-1]
    
    def parse_homework(self, homework_info: HomeWorkInfo):
        papers_info = self.get_paper_info(homework_info.Set_ID)
        print(homework_info)
        print(papers_info)
        sections_info = self.get_section_info(papers_info.PaperID)

        results = []
        for section in sections_info:
            if "听后选择" in section.Sec_mc:
                results += parse_chooses(self.cursor, papers_info.PaperID, section.SecID)
            elif "听后记录" in section.Sec_mc:
                results += parse_fill_in_the_blanks(self.cursor, papers_info.PaperID, section.SecID)
            elif "听后转述" in section.Sec_mc:
                results.append(parse_topic(self.cursor, papers_info.PaperID, section.SecID))
            elif "短文朗读" in section.Sec_mc:
                results.append(parse_read_chapter(self.cursor, papers_info.PaperID, section.SecID))
            else:
                raise ValueError("Unknown section type")
        return results
    
    def export_to_markdown(self, results, output_path: Union[str, None]):
        export_to_markdown(self.get_homework_list().Name, results, output_path)

    def export_to_pdf(self, results, output_path: str):
        export_to_pdf(self.get_homework_list().Name, results, output_path)
        

if __name__ == "__main__":
    ets = ETS()
    homework_info = ets.get_homework_list()
    restults = ets.parse_homework(homework_info)
    # for result in restults:
    #     print(result)

    ets.export_to_markdown(restults, "output.md")
    ets.export_to_pdf(restults, "output.pdf")