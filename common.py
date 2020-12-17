import yaml


def load_settings(file_name='settings.yml'):
    with open(file_name) as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
    return settings


def perc_2_float(perc: str):
    return float(perc.replace('%', '')) / 100
