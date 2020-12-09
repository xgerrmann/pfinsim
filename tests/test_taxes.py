import pytest

from main import load_settings, Taxes


def test_load_settings():
    settings = load_settings('../settings.yml')
    assert settings


def test_taxes_left_bracket():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 68508
    assert pytest.approx(taxes.income_gross_to_nett(gross), 1e-6) == 42920.262


def test_taxes_right_bracket():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 100000
    assert pytest.approx(taxes.income_gross_to_nett(gross), 1e-6) == 58823.722
