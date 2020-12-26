# Simulation to compare different (personal) financial scenarios
import argparse

from simulation.asset import Asset
from simulation.common import load_settings, Period
from simulation.job import Job
from simulation.mortgage import Mortgage
from simulation.taxes import Taxes
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Run personal finance simulation.',
                                 usage="'python3 -m simulation.simulation'")


def simulate(job: Job, mortgage: Mortgage, stock_account: Asset, taxes: Taxes, settings: dict):
    nett_mortgage_payments = []
    hist = pd.DataFrame()
    for ii in range(settings['simulation']['length'] * 12):
        print(f"Month: {ii} / {settings['simulation']['length'] * 12 - 1}")
        # Income
        gross_monthly_salary = job.get_salary(month=ii)
        gross_yearly_total_salary = job.total_salary

        # TODO: properly get the holiday allowance (the job class should use the tax class for the calculation)

        # Expenses and taxes
        # gross_mortgage_payment, mortgage_interest_payment = mortgage.repay()
        # mortgage_interest_tax = taxes.calc_mortgage_interest_tax(ii, mortgage_interest_payment,
        #                                                          gross_yearly_total_salary)
        gross_mortgage_payment = 0
        mortgage_interest_tax = 0
        mortgage_interest_payment = 0

        income_tax = taxes.calc_total_income_tax(gross_yearly_total_salary, period=Period.MONTH)

        capital_gains_tax = taxes.calculate_capital_gains_tax(ii, [stock_account])

        # Determine costs
        fixed_expenses = 500

        costs_total = capital_gains_tax + gross_mortgage_payment + income_tax + fixed_expenses + mortgage_interest_tax

        # Total income
        investable_amount = gross_monthly_salary - costs_total

        # Invest
        stock_account.advance()
        stock_account.add(investable_amount)

        # Store data for visualization
        hist = hist.append({'gross_pay': gross_monthly_salary,
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
    datA.plot(drawstyle="steps", alpha=0.5)
    plt.show()
    datB.plot(drawstyle="steps")
    plt.title('Net worth')
    plt.xlabel('Months')
    plt.ylabel('Amount [€]')
    plt.xlim([0, 360])
    plt.ylim([0, max(datB)])
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
    parser.parse_args()
    settings = load_settings('simulation/settings.yml')
    mortgage = init_mortgage(settings['mortgage'])
    taxes = Taxes(settings['taxes'])
    job = Job(settings['salary'])
    stock_account = init_stock_investment_account(settings['assets'])
    simulate(job, mortgage, stock_account, taxes, settings)


if __name__ == '__main__':
    main()
