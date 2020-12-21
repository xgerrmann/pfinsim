# Simulation to compare different (personal) financial scenarios

from simulation.asset import Asset
from simulation.common import load_settings
from simulation.job import Job
from simulation.mortgage import Mortgage
from simulation.taxes import Taxes
import pandas as pd
import matplotlib.pyplot as plt

# def visualize():
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


def simulate(job: Job, mortgage: Mortgage, stock_account: Asset, taxes: Taxes, settings: dict):
    nett_mortgage_payments = []
    hist = pd.DataFrame()
    for ii in range(settings['simulation']['length'] * 12):
        # Income
        gross_monthly_salary = job.get_salary(month=ii)
        gross_yearly_salary = job.total_salary

        # TODO: aftrekposten van bruto salaris aftrekken voordat netto wordt berekend

        # Expenses and taxes
        gross_mortgage_payment, mortgage_interest_payment = mortgage.repay()
        mortgage_interest_tax = taxes.calc_mortgage_interest_tax(ii, mortgage_interest_payment, gross_yearly_salary)

        fixed_expenses = 500

        income_tax = taxes.calc_total_income_tax(gross_monthly_salary, gross_yearly_salary)

        capital_gains_tax = taxes.calculate_capital_gains_tax(ii, [stock_account])

        # Determine costs
        costs_total = capital_gains_tax + gross_mortgage_payment + income_tax + fixed_expenses + mortgage_interest_tax
        print('#####COST BREAKDOWN')
        print(capital_gains_tax)
        print(gross_mortgage_payment)
        print(income_tax)
        print(fixed_expenses)
        print(mortgage_interest_tax)

        # Total income
        investable_amount = gross_pay - costs_total
        print(investable_amount)

        # Invest
        stock_account.advance()
        stock_account.add(investable_amount)

        # Store data for visualization
        hist = hist.append({'gross_pay': gross_pay,
                            'costs_total': costs_total,
                            'capital_gains_tax': capital_gains_tax,
                            'nett_mortgage_payment': nett_mortgage_payments,
                            'mortgage_interest_payment': mortgage_interest_payment,
                            'gross_mortgage_payment': gross_mortgage_payment,
                            'income_tax': income_tax,
                            'fixed_expenses': fixed_expenses,
                            'equity': stock_account.value
                            }, ignore_index=True)

    datA = hist.copy().drop(columns=['equity'])
    datB = hist['equity']
    print(hist.head())
    datA.plot()
    plt.show()
    datB.plot()
    plt.show()
    # visualize(hist)


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
