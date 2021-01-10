from typing import List

from .asset import Asset
from .common import month_to_year, Period, INFINITY


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

        # Mortgage
        self.mortgage_interest_deduction = tax_parameters['mortgage_interest_deduction']

        # Capital gains tax parameters
        self.capital_gains_tax_savings_rate = tax_parameters['capital_gains_tax']['savings_rate']
        self.capital_gains_tax_investment_rate = tax_parameters['capital_gains_tax']['investment_rate']
        self.capital_gains_tax_rate = tax_parameters['capital_gains_tax']['tax_rate']
        self.capital_gains_tax_savings_weights = tax_parameters['capital_gains_tax']['savings_weights']
        self.capital_gains_tax_brackets = tax_parameters['capital_gains_tax']['brackets']

        self.total_taxable_capital = 0

    def calc_total_income_tax(self, gross_salary_y, period: Period = Period.YEAR):
        income_tax, _ = self.calc_income_tax(gross_salary_y)
        work_tax_discount = self.calc_work_tax_discount(gross_salary_y)
        general_tax_discount = self.calc_general_tax_discount(gross_salary_y)
        total_tax = income_tax - work_tax_discount - general_tax_discount
        if period == Period.MONTH:
            total_tax /= 12
        return total_tax

    def calc_highest_tax_bracket(self, gross):
        brackets = self.income_tax_brackets + [INFINITY]
        for ii, left_bracket in enumerate(brackets[:-1]):
            if left_bracket < gross < brackets[ii + 1]:
                return self.work_tax_rates[ii]

    def calc_income_tax(self, gross_y):
        total_tax = 0
        brackets = self.income_tax_brackets + [INFINITY]
        tax_per_bucket = []
        for ii, left_bracket in enumerate(brackets[:-1]):
            rate = self.income_tax_rates[ii]
            bucket_tax = 0
            if gross_y > left_bracket:
                right_bracket = brackets[ii + 1]
                bucket_size = min(right_bracket, gross_y) - left_bracket
                bucket_tax = bucket_size * rate
                total_tax += bucket_tax
            tax_per_bucket.append(bucket_tax)
        return total_tax, tax_per_bucket

    def calc_work_tax_discount(self, gross_y):
        brackets = self.work_tax_brackets + [INFINITY]
        for ii, left_bracket in enumerate(brackets):
            rate = self.work_tax_rates[ii]
            base_amount = self.work_tax_base_amounts[ii]
            right_bracket = brackets[ii + 1]
            if left_bracket <= gross_y <= right_bracket:
                work_tax_discount_y = base_amount + rate * (gross_y - left_bracket)
                return work_tax_discount_y

    def calc_general_tax_discount(self, gross_y):
        brackets = self.general_tax_discount_brackets + [INFINITY]
        for ii, left_bracket in enumerate(brackets):
            right_bracket = brackets[ii + 1]
            rate = self.general_tax_discount_rates[ii]
            if left_bracket <= gross_y <= right_bracket:
                general_tax_discount_y = self.general_tax_discount_base_amount[ii] + rate * (gross_y - left_bracket)
                return general_tax_discount_y

    def calculate_capital_gains_tax(self, month: int, assets: List[Asset]):
        if month % 12 == 0:
            self.total_taxable_capital = self._determine_total_taxable_capital(assets)
        elif month % 12 == 3:
            return self._calc_capital_gains_tax(self.total_taxable_capital)
        return 0

    @staticmethod
    def _determine_total_taxable_capital(assets: List[Asset]):
        total_taxable_capital = 0
        for asset in assets:
            if asset.exempt_from_capital_gains_tax:
                continue
            total_taxable_capital += asset.value
        return total_taxable_capital

    def _calc_capital_gains_tax(self, total_capital: float):
        brackets = self.capital_gains_tax_brackets + [INFINITY]
        capital_gains_tax = 0
        for ii, left_bracket in enumerate(brackets[0:-1]):
            if total_capital > left_bracket:
                savings_weight = self.capital_gains_tax_savings_weights[ii]
                fictitious_return_rate = self.capital_gains_tax_savings_rate * savings_weight + \
                                         self.capital_gains_tax_investment_rate * (1 - savings_weight)
                right_bracket = brackets[ii + 1]
                bucket_size = min(total_capital, right_bracket) - left_bracket
                bucket_rate = fictitious_return_rate * self.capital_gains_tax_rate
                capital_gains_tax += bucket_rate * bucket_size
        return capital_gains_tax

    def calc_mortgage_interest_tax(self, month, interest_payment, gross_yearly_salary):
        year = month_to_year(month)
        if year in self.mortgage_interest_deduction:
            max_deduction_rate = self.mortgage_interest_deduction[year]
        else:
            max_deduction_rate = self.mortgage_interest_deduction[max(self.mortgage_interest_deduction.keys())]

        highest_income_tax_bracket = self.calc_highest_tax_bracket(gross_yearly_salary)

        mortgage_tax_deduction_rate = min(max_deduction_rate, highest_income_tax_bracket)

        mortgage_interest_tax = - mortgage_tax_deduction_rate * interest_payment
        return mortgage_interest_tax
