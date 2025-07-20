import aiohttp
import json
from typing import Dict, List
from datetime import datetime, timedelta
from dateutil.parser import parse


async def handle(week: int) -> Dict:    #Getting the data in json from API referenced in README
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://edt-iut-info-limoges.vercel.app/api/timetable/A1/{week}") as response:
            content = await response.text()

            return json.loads(content)


async def filter_data(week: int, day: str, group: int, sub: int) -> List:
    content = await handle(week)

    if content["success"]:
        data = content["data"]
        all_lessons = get_lessons_by_day(data, day)
        amphi_lessons = get_amphi_lessons(all_lessons)
        td_lessons = get_td_lessons(all_lessons, group)
        tp_lessons = get_tp_lessons(all_lessons, group, sub)

        my_lessons = amphi_lessons + td_lessons + tp_lessons
        modified_and_sorted_lessons = modify_lessons_by_time_and_sort(my_lessons)

        return modified_and_sorted_lessons
    else:
        raise ConnectionError


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


def get_lessons_by_day(content: dict, day: str) -> List:
    res = [lesson for lesson in content["lessons"]
           if lesson.get("start_date").split("T")[0] == day]
    return res


def get_days_of_this_week() -> List:
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    dt = datetime.today()
    start = dt - timedelta(dt.weekday())

    for num, day in enumerate(days_list):
        date = start + timedelta(days=num)
        days_list[num] = (date.strftime("%Y-%m-%d"), day)

    return days_list

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
