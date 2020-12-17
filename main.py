# Simulation to compare different (personal) financial scenarios

from asset import Asset
from common import load_settings
from mortgage import Mortgage
from taxes import Taxes
import pandas as pd


class Job:
    def __init__(self, job_parameters):
        self.total_salary = job_parameters['amount']
        self.holiday_allowance = job_parameters['holiday_allowance']
        self.monthly_salary = self.total_salary / (1 + self.holiday_allowance) / 12

    def get_salary(self, month):
        pay = self.monthly_salary
        if month % 12 + 1 == 5:
            pay += self.total_salary * self.holiday_allowance / (1 + self.holiday_allowance)
        return pay


# Mortgage related
def calc_nett_mortgate_payment(gross_payment, interest_payment):
    payoff = gross_payment - interest_payment
    # TODO: put this parameter in the settings
    net_payment = payoff + (1 - 0.3705) * interest_payment
    tax = gross_payment - net_payment
    return net_payment, tax


def simulate(job: Job, mortgage: Mortgage, stock_account: Asset, taxes: Taxes, settings: dict):
    nett_mortgage_payments = []
    hist = pd.DataFrame()
    for ii in range(settings['simulation']['length'] * 12):
        # Income
        gross_pay = job.get_salary(month=ii)

        # Expenses and taxes
        gross_mortgage_payment, mortgage_interest_payment = mortgage.repay()
        nett_mortgage_payment, tax = calc_nett_mortgate_payment(gross_mortgage_payment, mortgage_interest_payment)

        fixed_expenses = 500

        income_tax = taxes.calc_total_income_tax(gross_pay)

        capital_gains_tax = taxes.calculate_capital_gains_tax(ii, [stock_account])

        # Determine costs
        costs_total = capital_gains_tax + nett_mortgage_payment + income_tax + fixed_expenses

        # Total income
        investable_amount = gross_pay - costs_total

        # Invest
        stock_account.advance()
        stock_account.add(investable_amount)

        # Store data for visualization
        hist.append({'gross_pay': gross_pay,
                     'costs_total': costs_total,
                     'capital_gains_tax': capital_gains_tax,
                     'nett_mortgage_payment': nett_mortgage_payments,
                     'mortgage_interest_payment': mortgage_interest_payment,
                     'nett_mortgage_payment': nett_mortgage_payment,
                     'income_tax': income_tax,
                     'fixed_expenses': fixed_expenses
                     })

    # sns.set()
    # print(gross_mortgage_payments)
    # print(nett_mortgage_payments)
    # print(interest_payments)
    #
    # plt.plot(gross_mortgage_payments, label='gross')
    # plt.plot(nett_mortgage_payments, label='nett')
    # plt.plot(interest_payments, label='interest')
    # plt.legend()
    # plt.ylim(0, max(gross_mortgage_payments) * 1.1)
    # plt.show()
    #
    # plt.plot(size)
    # plt.show()


def init_mortgage(settings):
    rate = settings['interest_rate']
    size = settings['size']
    duration = settings['duration']
    mortgage_type = settings['type']
    return Mortgage(rate, size, duration, mortgage_type)


def init_stock_investment_account(settings):
    initial_value = settings['stocks']['start_value']
    return_rate = settings['stocks']['returns']
    return Asset(initial_value, return_rate)


def main():
    settings = load_settings()
    mortgage = init_mortgage(settings['mortgage'])
    taxes = Taxes(settings['taxes'])
    job = Job(settings['salary'])
    stock_account = init_stock_investment_account(settings['assets'])
    simulate(job, mortgage, stock_account, taxes, settings)


if __name__ == '__main__':
    main()
