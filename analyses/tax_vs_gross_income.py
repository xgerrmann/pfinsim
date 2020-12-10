from main import load_settings
from taxes import Taxes
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def plot_working_tax_discount(taxes: Taxes):
    gross_incomes = range(120000)
    discounts = []
    for gross_income in gross_incomes:
        tax_discount = taxes.calc_work_tax_discount(gross_income)
        discounts.append(tax_discount)

    plt.plot(gross_incomes, discounts)
    plt.title('Working tax discount')
    plt.xlabel('Gross income [€]')
    plt.ylabel('Tax discount [€]')
    plt.show()


def plot_general_tax_discount(taxes: Taxes):
    gross_incomes = range(120000)
    discounts = []
    for gross_income in gross_incomes:
        tax_discount = taxes.calc_general_tax_discount(gross_income)
        discounts.append(tax_discount)

    plt.plot(gross_incomes, discounts)
    plt.title('General tax discount')
    plt.xlabel('Gross income [€]')
    plt.ylabel('Tax discount [€]')
    plt.show()


def plot_income_tax_(taxes: Taxes):
    gross_incomes = range(1, 120000)
    tax_list = []
    tax_list_perc = []
    for gross_income in gross_incomes:
        nett, tax = taxes.calc_income_tax(gross_income)
        tax_list.append(tax)
        tax_list_perc.append(tax / gross_income)

    # plt.plot(gross_incomes, tax_list)
    plt.plot(gross_incomes, tax_list_perc)
    plt.title('Income vs tax')
    plt.xlabel('Gross income [€]')
    plt.ylabel('Tax [€]')
    plt.ylim([0.3, 0.45])
    plt.xlim([0, max(gross_incomes)])
    plt.show()


def plot_total_tax(taxes: Taxes):
    income_start = 5000
    income_end = 120000
    gross_incomes = range(income_start, income_end)
    tax_list = []
    tax_list_perc = []
    for gross_income in gross_incomes:
        nett, tax = taxes.calc_nett_income(gross_income)
        tax_list.append(tax)
        tax_list_perc.append(tax / gross_income * 100)

    plt.plot(gross_incomes, tax_list)
    plt.title('Inkomsten (bruto) vs belasting')
    plt.xlabel('Bruto [€]')
    plt.ylabel('Belasting [€]')
    plt.xlim([0, max(gross_incomes)])
    plt.ylim(0, max(tax_list))
    plt.show()

    plt.plot(gross_incomes, tax_list_perc)
    plt.title('Inkomsten (bruto) vs belasting druk')
    plt.xlabel('Bruto [€]')
    plt.ylabel('Belasting [%]')
    plt.ylim([0, 50])
    plt.xlim([0, max(gross_incomes)])
    plt.show()


def main():
    tax_settings = load_settings('../settings.yml')['taxes']
    taxes = Taxes(tax_settings)
    # plot_working_tax_discount(taxes)
    # plot_general_tax_discount(taxes)
    # plot_income_tax_(taxes)
    plot_total_tax(taxes)


if __name__ == "__main__":
    main()
