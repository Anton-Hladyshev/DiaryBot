import aiohttp
import asyncio
import json
from typing import Dict, List, Tuple
from datetime import datetime
from dateutil.parser import parse


async def handle(week: int) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://edt-iut-info-limoges.vercel.app/api/timetable/A1/{week}") as response:
            content = await response.text()
            return json.loads(content)["data"]


async def filter_data(week: int, group: int, sub: int) -> List:
    content = await handle(week)
    today_lessons = get_today_lessons(content)
    amphi_lessons = get_amphi_lessons(today_lessons)
    td_lessons = get_td_lessons(today_lessons, group)
    tp_lessons = get_tp_lessons(today_lessons, group, sub)

    my_lessons = amphi_lessons + td_lessons + tp_lessons
    modified_and_sorted_lessons = modify_lessons_by_time_and_sort(my_lessons)

    return modified_and_sorted_lessons


def modify_lessons_by_time_and_sort(content: list):
    for lesson in content:
        lesson["start_date"] = parse(lesson.get("start_date").split("T")[1].split('.')[0]).time()
        lesson["end_date"] = parse(lesson.get("end_date").split("T")[1].split('.')[0]).time()

    content.sort(key=lambda lesson: lesson.get("start_date"))

    count_double_lessons = 0

    for index in range(len(content) - 2):
        if (content[index]["content"] == content[index + 1]["content"] and
                content[index].get("end_date") == content[index + 1].get("start_date")):

            count_double_lessons += 1
            content[index]["end_date"] = content[index + 1]["end_date"]
            alter_idx = index + 1

            while alter_idx < (len(content) - 1):
                content[alter_idx + 1] = content[alter_idx]
                alter_idx += 1

    return content[:len(content) - count_double_lessons]

            




def get_today_lessons(content: dict) -> List:
    res = [lesson for lesson in content["lessons"]
           if lesson.get("start_date").split("T")[0] == str(datetime.today()).split(' ')[0]]
    return res


def get_amphi_lessons(content: list) -> List:
    res = [lesson for lesson in content if lesson.get("group") is None]
    return res


def get_td_lessons(content: list, group: int) -> List:
    res = [lesson for lesson in content
                    if lesson.get("group") is not None and lesson.get("group").get("main") == group and lesson.get("group").get("sub") is None]
    return res


def get_tp_lessons(content: list, group: int, sub: int) -> List:
    res = [lesson for lesson in content
           if lesson.get("group") is not None and lesson.get("group").get("main") == group and lesson.get("group").get("sub") == sub]
    return res


#if __name__ == "__main__":