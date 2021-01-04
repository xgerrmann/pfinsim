from enum import Enum

import yaml

INFINITY = float('inf')


def load_settings(file_name='settings.yml'):
    with open(file_name) as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
    return settings


def perc_2_float(perc: str):
    return float(perc.replace('%', '')) / 100


def month_to_year(month: int):
    return 2021 + floor(month / 12)


class Period(Enum):
    YEAR = 'year'
    MONTH = 'month'
