import pytest

from pfinsim.common import load_settings
from pfinsim.taxes import Taxes


@pytest.fixture
def tax_parameters():
    settings = load_settings()
    tax_parameters = settings['taxes'][2020]
    return tax_parameters


def test_load_settings_file(tax_parameters):
    assert tax_parameters


def test_income_taxes_zero(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 0
    tax, _ = taxes.calc_income_tax(gross)
    assert tax == 0


def test_income_taxes_left_bracket(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 68508
    tax, _ = taxes.calc_income_tax(gross)
    assert pytest.approx(tax, 1e-6) == 25587.738


def test_income_taxes_right_bracket(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 100000
    tax, _ = taxes.calc_income_tax(gross)
    assert pytest.approx(tax, 1e-6) == 41176.278


def test_work_tax_discount_zero(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 0
    assert taxes.calc_work_tax_discount(gross) == 0


def test_work_tax_discount_max(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 98604
    assert taxes.calc_work_tax_discount(gross) == 0


def test_work_tax_discount_too_high(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 200000
    assert taxes.calc_work_tax_discount(gross) == 0


def test_work_tax_discount_50k(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 50000
    assert pytest.approx(taxes.calc_work_tax_discount(gross), 1e-6) == 2916.24


def test_general_tax_discount_zero(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 0
    assert pytest.approx(taxes.calc_general_tax_discount(gross), 1e-6) == 2711


def test_general_tax_discount_50k(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 50000
    assert pytest.approx(taxes.calc_general_tax_discount(gross), 1e-6) == 1049.72792


def test_general_tax_discount_too_high(tax_parameters):
    taxes = Taxes(tax_parameters)
    gross = 100000
    assert pytest.approx(taxes.calc_general_tax_discount(gross), 1e-6) == 0
