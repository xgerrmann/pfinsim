import pytest

from main import load_settings, Taxes


def test_load_settings():
    settings = load_settings('../settings.yml')
    assert settings


def test_income_taxes_zero():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 0
    assert taxes.income_gross_to_nett(gross) == 0


def test_income_taxes_left_bracket():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 68508
    assert pytest.approx(taxes.income_gross_to_nett(gross), 1e-6) == 42920.262


def test_income_taxes_right_bracket():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 100000
    assert pytest.approx(taxes.income_gross_to_nett(gross), 1e-6) == 58823.722


def test_work_tax_discount_zero():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 0
    assert taxes.calc_work_tax_discounts(gross) == 0


def test_work_tax_discount_too_high():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 98604
    assert taxes.calc_work_tax_discounts(gross) == 0


def test_work_tax_discount_50k():
    settings = load_settings('../settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 50000
    assert pytest.approx(taxes.calc_work_tax_discounts(gross), 1e-6) == 2916.24
