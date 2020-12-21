import pytest

from simulation.main import load_settings
from simulation.taxes import Taxes


def test_load_settings():
    settings = load_settings('../simulation/settings.yml')
    assert settings


def test_income_taxes_zero():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 0
    nett, tax = taxes.calc_income_tax(gross)
    assert nett == 0
    assert tax == 0

def test_income_taxes_left_bracket():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 68508
    nett, tax = taxes.calc_income_tax(gross)
    assert pytest.approx(nett, 1e-6) == 42920.262
    assert pytest.approx(tax, 1e-6) == 25587.738


def test_income_taxes_right_bracket():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 100000
    nett, tax = taxes.calc_income_tax(gross)
    assert pytest.approx(nett, 1e-6) == 58823.722
    assert pytest.approx(tax, 1e-6) == 41176.278


def test_work_tax_discount_zero():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 0
    assert taxes.calc_work_tax_discount(gross) == 0


def test_work_tax_discount_max():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 98604
    assert taxes.calc_work_tax_discount(gross) == 0


def test_work_tax_discount_too_high():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 200000
    assert taxes.calc_work_tax_discount(gross) == 0


def test_work_tax_discount_50k():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 50000
    assert pytest.approx(taxes.calc_work_tax_discount(gross), 1e-6) == 2916.24


def test_general_tax_discount_zero():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 0
    assert pytest.approx(taxes.calc_general_tax_discount(gross), 1e-6) == 2711


def test_general_tax_discount_50k():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 50000
    assert pytest.approx(taxes.calc_general_tax_discount(gross), 1e-6) == 1049.72792


def test_general_tax_discount_too_high():
    settings = load_settings('../simulation/settings.yml')
    tax_parameters = settings['taxes']
    taxes = Taxes(tax_parameters)
    gross = 100000
    assert pytest.approx(taxes.calc_general_tax_discount(gross), 1e-6) == 0
