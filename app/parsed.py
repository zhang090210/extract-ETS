from sqlite3 import Cursor, connect
from .question_type import *

def parse_chooses(cursor: Cursor, paper_id: int, sec_id: int) -> list[Choose]:
    cursor.execute(f"SELECT * FROM ScoreForChoose WHERE PaperID = {paper_id} AND SecID = {sec_id} ORDER BY EntityID")
    rows = cursor.fetchmany(14)
    chooses = []
    for row in rows:
        chooses.append(Choose(*row))
    return chooses

def parse_fill_in_the_blanks(cursor: Cursor, paper_id: int, sec_id: int) -> list[FillInTheBlank]:
    cursor.execute(f"SELECT * FROM ScoreForChoose WHERE PaperID = {paper_id} AND SecID = {sec_id} ORDER BY EntityID")
    rows = cursor.fetchmany(18)[-4:]
    fill_in_the_blanks = []
    for row in rows:
        fill_in_the_blanks.append(FillInTheBlank(*row))
    return fill_in_the_blanks

def parse_topic(cursor: Cursor, paper_id: int, sec_id: int) -> Topic:
    cursor.execute(f"SELECT * FROM Word WHERE PaperID = {paper_id} AND SecID = {sec_id}")
    row = cursor.fetchone()
    return Topic(*row)

def parse_read_chapter(cursor: Cursor, paper_id: int, sec_id: int) -> ReadChapter:
    cursor.execute(f"SELECT * FROM Word WHERE PaperID = {paper_id} AND SecID = {sec_id}")
    row = cursor.fetchone()
    return ReadChapter(*row)


if __name__ == '__main__':
    conn = connect(r'C:\Program Files (x86)\ETS\localdata\ETS.db')
    cursor = conn.cursor()

    chooses = parse_chooses(cursor, 3, 13)
    for choose in chooses:
        print(choose)
    chooses = parse_chooses(cursor, 3, 14)
    for choose in chooses:
        print(choose)

    print("\n\n")

    fill_in_the_blanks = parse_fill_in_the_blanks(cursor, 3, 15)
    for fill_in_the_blank in fill_in_the_blanks:
        print(fill_in_the_blank)
        
    print("\n\n")
    topic = parse_topic(cursor, 3, 16)
    print(topic)

    print("\n\n")
    read_chapter = parse_read_chapter(cursor, 3, 18)
    print(read_chapter)