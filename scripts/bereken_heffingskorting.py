import argparse

from simulation.common import load_settings
from simulation.taxes import Taxes

parser = argparse.ArgumentParser(description='Determine tax credits.',
                                 usage="'python3 -m scripts.bereken_heffingskorting'")
parser.add_argument('gross_salary_y', type=float, help='Total taxable yearly gross income')


def main():
    settings = load_settings('simulation/settings.yml')
    taxes = Taxes(settings['taxes'])
    work_tax_discount = taxes.calc_work_tax_discount(gross_y)
    general_tax_discount = taxes.calc_general_tax_discount(gross_y)
    print(f'Work tax discount:    {work_tax_discount:8.{2}f}')
    print(f'General tax discount: {general_tax_discount:8.{2}f}')


if __name__ == '__main__':
    args = parser.parse_args()
    gross_y = args.gross_salary_y
    print('python3 -m scripts.bereken_heffingskorting')
    main()
