from enum import Enum
import importlib.resources
from typing import Optional
from . import resources
import yaml

INFINITY = float('inf')


def load_settings(file_name: Optional[str] = None):
    if file_name:
        with open(file_name) as file:
            settings = yaml.load(file, Loader=yaml.FullLoader)
    else:
        settings = yaml.load(importlib.resources.read_text(resources, 'settings.yml'), Loader=yaml.FullLoader)
    return settings


def perc_2_float(perc: str):
    return float(perc.replace('%', '')) / 100


def month_to_year(month: int):
    return 2021 + floor(month / 12)


class Period(Enum):
    YEAR = 'year'
    MONTH = 'month'
