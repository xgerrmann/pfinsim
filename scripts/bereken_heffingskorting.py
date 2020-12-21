import argparse

from simulation.common import load_settings
from simulation.job import Job
from simulation.taxes import Taxes

parser = argparse.ArgumentParser(description='Determine tax credits.',
                                 usage="'python3 -m scripts.bereken_heffingskorting'")
parser.add_argument('gross_salary_y', type=float, help='Total taxable yearly gross income')


def init():
    settings = load_settings('simulation/settings.yml')
    taxes = Taxes(settings['taxes'])
    job_settings = settings['salary']
    job_settings['amount'] = gross_y
    job = Job(job_settings)
    return job, taxes


def main():
    # Init
    job, taxes = init()

    # Calculations
    gross_y_excl_bonuses = gross_y / (1+job.holiday_allowance)
    work_tax_discount_y = taxes.calc_work_tax_discount(gross_y_excl_bonuses)
    general_tax_discount_y = taxes.calc_general_tax_discount(gross_y_excl_bonuses)
    work_tax_discount_m = work_tax_discount_y / 12
    general_tax_discount_m = general_tax_discount_y / 12

    salary_m = job.monthly_salary
    salary_y = salary_m * job.holiday_allowance
    holiday_allowance_y = job.get_holiday_allowance()
    holiday_allowance_fraction = job.holiday_allowance
    print('# GROSS SUMMARY')
    print(f'Total taxable income: {+gross_y:+10.2f} ({(1 + holiday_allowance_fraction) * 100:.0f}%)')
    print(f'Base salary:          {+salary_y:+10.2f} (100%)')
    print(f'Monthly salary:       {+salary_m:+10.2f} (100% / 12)')
    print(f'Holiday allowance:    {+holiday_allowance_y:+10.2f} ({holiday_allowance_fraction * 100:3.0f}%)')

    nett_y, tax_y = taxes.calc_income_tax(gross_y_excl_bonuses)

    total_dicounts_m = work_tax_discount_m + general_tax_discount_m
    tax_m = tax_y / 12
    print()
    print('# TAXES AND TAX CREDITS')
    print(f'Income tax:           {+tax_m:+10.2f}')
    print(f'Work tax discount:    {-work_tax_discount_m:+10.2f}')
    print(f'General tax discount: {-general_tax_discount_m:+10.2f}')
    print('------------------------------------ +')
    total_taxes_m = tax_m - total_dicounts_m
    print(f'Total taxes:          {total_taxes_m:10.2f}')

    nett_m = nett_y / 12
    nett_pay_m = nett_m + total_dicounts_m

    print()
    print('# NETT BASE INCOME')
    print(f'Montly gross salary:  {+salary_m:+10.2f}')
    print(f'Total taxes:          {-total_taxes_m:+10.2f}')
    print('------------------------------------ +')
    print(f'Montly nett salary:   {nett_pay_m:10.2f}')

    # TODO: Calculate nett holiday allowance
    nett_y, tax_y = taxes.calc_income_tax(gross_y)
    work_tax_discount_y = taxes.calc_work_tax_discount(gross_y_excl_bonuses)
    general_tax_discount_y = taxes.calc_general_tax_discount(gross_y_excl_bonuses)
    total_discounts_y = work_tax_discount_y + general_tax_discount_y
    total_nett_y_incl_holiday_allowance = nett_y + total_discounts_y


if __name__ == '__main__':
    args = parser.parse_args()
    gross_y = args.gross_salary_y
    print('python3 -m scripts.bereken_heffingskorting')
    main()
