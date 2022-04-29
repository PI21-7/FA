from datetime import datetime, timedelta
from typing import List
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Schedule(object):
    GROUP_SCHEDULE = r'https://ruz.fa.ru/api/schedule/group/{}?start={}&finish={}&lng=1'

    @staticmethod
    def __current_datetime() -> datetime:
        return datetime.now()

    @staticmethod
    def __week_delta() -> timedelta:
        return timedelta(days=6)

    @staticmethod
    def __current_week() -> str:
        return Schedule.__current_date(), (Schedule.__current_datetime() + Schedule.__week_delta()).strftime("%Y.%m.%d")

    @staticmethod
    def __current_date() -> str:
        return datetime.now().strftime("%Y.%m.%d")

    @staticmethod
    def __group_id(group: str = 'ПИ21-7'):
        form = r'https://ruz.fa.ru/api/search?term={}&type=group'
        request = requests.get(form.format(group), verify=False)
        if request.status_code == 200:
            return request.json()[0]["id"]

    @classmethod
    def get_group_schedule(cls, group: str, start: str = None, end: str = None) -> List[dict]:
        if start is None:
            start, end = cls.__current_week()
        group = cls.__group_id(group)
        request = requests.get(cls.GROUP_SCHEDULE.format(group, start, end), verify=False)
        if request.status_code == 200:
            return request.json()


