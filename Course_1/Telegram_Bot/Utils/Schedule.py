from datetime import date, datetime, timedelta
from requests import Response
from typing import List

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Schedule(object):
    """API REQUESTS CLASS TO ruz.fa.ru"""
    GROUP_SCHEDULE: str = r"https://ruz.fa.ru/api/schedule/group/{}?start={}&finish={}&lng=1"
    SAMPLE_FORM: str = r'https://ruz.fa.ru/api/search?term={}&type=group'

    @staticmethod
    def __current_datetime() -> datetime: return datetime.now()

    @staticmethod
    def __week_delta() -> timedelta: return timedelta(days=6)

    @staticmethod
    def __current_date() -> str: return datetime.now().strftime("%Y.%m.%d")

    @staticmethod
    def __current_week() -> str:
        return Schedule.__current_date(), (Schedule.__current_datetime() + Schedule.__week_delta()).strftime("%Y.%m.%d")

    @classmethod
    def __group_id(cls, group: str = 'ПИ21-7') -> str:
        """Возвращает ID группы"""
        request = requests.get(cls.SAMPLE_FORM.format(group), verify=False)
        if request.status_code == 200:
            return request.json()[0]["id"]

    @classmethod
    def get_group_schedule(cls, group: str, start: date = None, end: date = None) -> List[dict]:
        """Возвращает JSON с информацией о расписании"""
        if start is None:
            start, end = cls.__current_week()
        group = cls.__group_id(group)
        request: Response = requests.get(cls.GROUP_SCHEDULE.format(group, start, end), verify=False, json=True)
        return request.json() if request.status_code == 200 else 'NO RESPONCE'
