from typing import List

import numpy as np

from asset import Asset


class Taxes:
    def __init__(self, tax_parameters):
        self.income_tax_brackets = tax_parameters['income_tax']['brackets']
        self.income_tax_rates = tax_parameters['income_tax']['rates']
        self.work_tax_brackets = tax_parameters['work_discount']['brackets']
        self.work_tax_rates = tax_parameters['work_discount']['rates']
        self.work_tax_base_amounts = tax_parameters['work_discount']['base_amounts']
        self.general_tax_discount_brackets = tax_parameters['regular_tax_discount']['brackets']
        self.general_tax_discount_base_amount = tax_parameters['regular_tax_discount']['base_amount']
        self.general_tax_discount_rates = tax_parameters['regular_tax_discount']['rates']
        self.capital_gains_tax_brackets = tax_parameters['capital_gains_tax']['brackets']
        self.capital_gains_tax_rates = tax_parameters['capital_gains_tax']['rates']

        self.total_taxable_capital = 0

    def calc_total_income_tax(self, gross):
        _, income_tax = self.calc_income_tax(gross)
        work_tax_discount = self.calc_work_tax_discount(gross)
        general_tax_discount = self.calc_general_tax_discount(gross)
        total_tax = income_tax - work_tax_discount - general_tax_discount
        return total_tax

    def calc_income_tax(self, gross):
        nett = 0
        tax = 0
        brackets = self.income_tax_brackets + [np.inf]
        for ii, left_bracket in enumerate(brackets[:-1]):
            rate = self.income_tax_rates[ii]
            if gross > left_bracket:
                right_bracket = brackets[ii + 1]
                bucket_size = min(right_bracket, gross)- left_bracket
                bucket_tax = bucket_size * rate
                nett += bucket_size - bucket_tax
                tax += bucket_tax
        return nett, tax

    def calc_work_tax_discount(self, gross):
        brackets = self.work_tax_brackets + [np.inf]
        for ii, left_bracket in enumerate(brackets):
            rate = self.work_tax_rates[ii]
            base_amount = self.work_tax_base_amounts[ii]
            right_bracket = brackets[ii + 1]
            if left_bracket <= gross <= right_bracket:
                work_tax_discount = base_amount + rate * (gross - left_bracket)
                return work_tax_discount

    def calc_general_tax_discount(self, gross):
        brackets = self.general_tax_discount_brackets + [np.inf]
        for ii, left_bracket in enumerate(brackets):
            right_bracket = brackets[ii+1]
            rate = self.general_tax_discount_rates[ii]
            if left_bracket <= gross <= right_bracket:
                general_tax_discount = self.general_tax_discount_base_amount[ii] + rate * (gross - left_bracket)
                return general_tax_discount

    def calculate_capital_gains_tax(self, month: int, assets: List[Asset]):
        if month % 12 == 0:
            self.total_taxable_capital = self._determine_total_taxable_capital(assets)
        elif month % 12 == 3:
            self._calc_capital_gains_tax(self.total_taxable_capital)

    @staticmethod
    def _determine_total_taxable_capital(assets: List[Asset]):
        total_taxable_capital = 0
        for asset in assets:
            if asset.exempt_from_capital_gains_tax:
                continue
            total_taxable_capital += asset.value
        return total_taxable_capital

    def _calc_capital_gains_tax(self, total_capital: float):
        brackets = self.capital_gains_tax_brackets + [np.inf]
        capital_gains_tax = 0
        for ii, left_bracket in enumerate(brackets):
            if total_capital > left_bracket:
                right_bracket = brackets[ii + 1]
                bucket_size = min(total_capital, right_bracket) - left_bracket
                rate = self.capital_gains_tax_rates[ii]
                capital_gains_tax += rate * bucket_size
        return capital_gains_tax
