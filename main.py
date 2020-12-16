# Simulation to compare different (personal) financial scenarios
import matplotlib.pyplot as plt
import seaborn as sns

import yaml

from asset import Asset
from mortgage import Mortgage, MortgageType
from taxes import Taxes


def load_settings(file_name='settings.yml'):
    with open(file_name) as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
    return settings


def perc_2_float(perc: str):
    return float(perc.replace('%', '')) / 100


class Job:
    def __init__(self, job_parameters, taxes: Taxes):
        self.total_salary = job_parameters['amount']
        self.holiday_allowance = job_parameters['holiday_allowance']
        self.monthly_salary = self.total_salary / (1 + self.holiday_allowance) / 12

    def get_salary(self, month):
        pay = self.monthly_salary
        if month % 12 + 1 == 5:
            pay += self.total_salary * self.holiday_allowance / (1 + self.holiday_allowance)
        return pay


# Mortgage related
def calc_nett_payment(gross_payment, interest_payment):
    payoff = gross_payment - interest_payment
    return payoff + (1 - 0.3705) * interest_payment


def simulate(job: Job, mortgage: Mortgage, stock_account: Asset, settings: dict):
    gross_mortgage_payments = []
    nett_mortgage_payments = []
    interest_payments = []
    size = []
    for ii in range(settings['simulation']['length'] * 12):
        gross_payment, interest_payment = mortgage.repay()

        # Trek betaalde hypotheekrente af van totaal salaris / inkomen
        gross_pay = job.get_salary(month=ii)
        # nett_pay =
        # total_taxable_income += gross_pay

        gross_mortgage_payments.append(gross_payment)
        interest_payments.append(interest_payment)

        nett_payment = calc_nett_payment(gross_payment, interest_payment)
        nett_mortgage_payments.append(nett_payment)

        size.append(mortgage._size)

    sns.set()
    print(gross_mortgage_payments)
    print(nett_mortgage_payments)
    print(interest_payments)

    plt.plot(gross_mortgage_payments, label='gross')
    plt.plot(nett_mortgage_payments, label='nett')
    plt.plot(interest_payments, label='interest')
    plt.legend()
    plt.ylim(0, max(gross_mortgage_payments) * 1.1)
    plt.show()

    plt.plot(size)
    plt.show()


def init_mortgage(settings):
    rate = settings['interest_rate']
    size = settings['size']
    duration = settings['duration']
    mortgage_type = settings['type']
    return Mortgage(rate, size, duration, mortgage_type)


def init_stock_investment_account(settings):
    initial_value = settings['stocks']['initial_value']
    return_rate = settings['stocks']['rate']
    return Asset(initial_value, return_rate)


def main():
    settings = load_settings()
    mortgage = init_mortgage(settings['mortgage'])
    taxes = Taxes(settings['taxes'])
    job = Job(settings['salary'], taxes)
    stock_account = init_stock_investment_account(settings['stocks'])
    simulate(job, mortgage, stock_account, settings)


if __name__ == '__main__':
    main()
