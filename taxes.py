import numpy as np

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

    def income_gross_to_nett(self, gross):
        nett = 0
        # TODO: dont append, but cipy, otherwise array will gro with each call
        self.income_tax_brackets.append(np.inf)
        for ii, left_bracket in enumerate(self.income_tax_brackets[:-1]):
            rate = self.income_tax_rates[ii]
            right_bracket = min(self.income_tax_brackets[ii + 1], gross)
            bucket_size = right_bracket - left_bracket
            if bucket_size <= 0:
                break
            nett += bucket_size * (1 - rate)
        return nett

    def calc_work_tax_discounts(self, gross):
        # TODO: dont append, but cipy, otherwise array will gro with each call
        self.work_tax_brackets.append(np.inf)
        for ii, left_bracket in enumerate(self.work_tax_brackets):
            rate = self.work_tax_rates[ii]
            base_amount = self.work_tax_base_amounts[ii]
            right_bracket = self.work_tax_brackets[ii + 1]
            if left_bracket <= gross <= right_bracket:
                work_tax_discount = base_amount + rate * (gross - left_bracket)
                return work_tax_discount

    def calc_general_tax_discount(self, gross):
        # TODO: dont append, but cipy, otherwise array will gro with each call
        self.general_tax_discount_brackets.append(np.inf)
        for ii, left_bracket in enumerate(self.general_tax_discount_brackets):
            right_bracket = self.general_tax_discount_brackets[ii+1]
            rate = self.general_tax_discount_rates[ii]
            if left_bracket <= gross <= right_bracket:
                print(f'left: {left_bracket}, right: {right_bracket}, rate: {rate}')
                general_tax_discount = self.general_tax_discount_base_amount[ii] + rate * (gross - left_bracket)
                return general_tax_discount