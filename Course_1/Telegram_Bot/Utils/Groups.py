import string

import requests

from ast import literal_eval


class Groups:
    GROUPS_LIST = r'https://ruz.fa.ru/api/search?term={}&type=group'

    @classmethod
    def __get_groups(cls, item: str) -> dict:
        request = requests.get(cls.GROUPS_LIST.format(item), verify=False)
        if request.status_code == 200:
            return request.json()

    @classmethod
    def get_groups_on_one_letter(cls):
        low = [chr(i) for i in range(ord('а'), ord('а') + 32)]
        dictionary = dict()
        for first_letter in low:
            result = Groups.__get_groups(first_letter)
            for res in result :
                if 'факультет' in res['description'].lower():
                    desc = res['description'][:res['description'].find('|') - 1]
                    if desc not in dictionary.keys():
                        dictionary.setdefault(desc, [res['label']])
                    else:
                        dictionary[desc].append(res['label'])

        return dictionary

    @classmethod
    def get_groups_on_two_letters(cls):
        low = [chr(i) for i in range(ord('а'), ord('а') + 32)]
        dictionary = dict()
        for first_letter in low:
            for second_letter in low:
                result = Groups.__get_groups(first_letter + second_letter)
                for res in result:
                    if 'факультет' in res['description'].lower():
                        desc = res['description'][:res['description'].find('|') - 1]
                        if desc not in dictionary.keys():
                            dictionary.setdefault(desc, [res['label']])
                        else:
                            dictionary[desc].append(res['label'])

        return dictionary

    @classmethod
    def get_groups_on_two_letters_with_digits(cls):
        low = [chr(i) for i in range(ord('а'), ord('а') + 32)]
        nums = string.digits
        dictionary = dict()
        for first_letter in low:
            for second_letter in low:
                for number in nums:
                    result = Groups.__get_groups(first_letter + second_letter + number)
                    for res in result:
                        if 'факультет' in res['description'].lower():
                            desc = res['description'][:res['description'].find('|') - 1]
                            label = res['label']
                            if desc not in dictionary.keys():
                                dictionary.setdefault(desc, [label])
                            elif '17' not in label and '18' not in label:
                                dictionary[desc].append(label)

        return dictionary

    @classmethod
    def __get_all_groups(cls):  # TODO
        one_letter = cls.get_groups_on_one_letter()
        two_letters = cls.get_groups_on_two_letters()
        two_letters_and_digits = cls.get_groups_on_two_letters_with_digits()
        result = one_letter | two_letters | two_letters_and_digits
        result = {key: list(set(value)) for key, value in result.items()}
        return result

    @staticmethod
    def __read_log(path: str = 'Utils/Groups.txt') -> list:
        result = list()
        with open(path, 'r', encoding='utf-8') as file:
            for row in file.readlines():
                result.append(literal_eval(row))
        return result

    @classmethod
    def get_groups(cls):  # TODO
        return cls.__read_log()

    @classmethod
    def get_faculties_list(cls):  # TODO
        return list(map(lambda x: x[0], cls.__read_log()))

    @classmethod
    def get_groups_by_faculty(cls, faculty: str):  # TODO
        return [item[1] for item in cls.__read_log() if item[0] == faculty][0]

    @classmethod
    def get_groups_by_initial(cls, initial):
        result = list()
        for item in cls.__read_log():
            for i in item[1]:
                if i[:cls.__first_digit(i)] == initial and '17' not in i and '18' not in i:
                    result.append(i)
        return sorted(result)

    @staticmethod
    def __first_digit(element):
        for ind, let in enumerate(element):
            if let.isdigit():
                return ind

    @classmethod
    def get_groups_types(cls, array):
        return list(set(map(lambda x: x[:cls.__first_digit(x)], array)))


if __name__ == '__main__':
    print(*Groups.get_faculties_list(), sep='\n\n')