import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

from simulation.simulation import load_settings
from simulation.taxes import Taxes

from matplotlib.ticker import FormatStrFormatter
import numpy as np

# sns.set()

SHOWPLOTS = False

plt.style.use('../../simulation/plot_style.mplstyle')
mpl.rcParams['toolbar'] = 'None'

import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

n_colors = 5
cmap = matplotlib.cm.get_cmap('tab20')
colors = cmap(np.linspace(0, 1, n_colors))
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

# hfont = {'fontname':'Lato'}
hfont = {'fontname': 'Lato', 'fontweight': 'light'}


def set_tick_formatting():
    plt.gca().xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.gca().yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    for spine in plt.gca().spines:
        plt.gca().spines[spine].set_visible(False)

    plt.xticks(**hfont)
    plt.yticks(**hfont)
    plt.gca().xaxis.set_tick_params(width=0)
    plt.gca().yaxis.set_tick_params(width=0)

    plt.grid(linewidth=0.5)


def plot_working_tax_discount(taxes: Taxes):
    gross_incomes = range(120000)
    discounts = []
    for gross_income in gross_incomes:
        tax_discount = taxes.calc_work_tax_discount(gross_income)
        discounts.append(tax_discount)

    plt.plot(gross_incomes, discounts)
    plt.title('Arbeidsheffingskorting', **hfont)
    plt.xlabel('Bruto jaarinkomen [€]', **hfont)
    plt.ylabel('Korting [€]', **hfont)
    set_tick_formatting()
    plt.tight_layout()
    plt.savefig('working_tax_discount.png')


def plot_general_tax_discount(taxes: Taxes):
    gross_incomes = range(120000)
    discounts = []
    for gross_income in gross_incomes:
        tax_discount = taxes.calc_general_tax_discount(gross_income)
        discounts.append(tax_discount)

    plt.figure()
    plt.plot(gross_incomes, discounts)
    plt.title('Algemene heffingskorting', **hfont)
    plt.xlabel('Bruto jaarinkomen [€]', **hfont)
    plt.ylabel('Korting [€]', **hfont)
    set_tick_formatting()
    plt.tight_layout()
    plt.savefig('general_tax_discount.png')


def plot_income_tax_(taxes: Taxes):
    gross_incomes = range(1, 120000)
    tax_list = []
    tax_list_perc = []
    for gross_income in gross_incomes:
        nett, tax = taxes.calc_income_tax(gross_income)
        tax_list.append(tax)
        tax_list_perc.append(tax / gross_income * 100)

    plt.figure()
    plt.plot(gross_incomes, tax_list_perc)
    plt.title('Inkomen versus salaris', **hfont)
    plt.xlabel('Bruto jaarinkomen [€]', **hfont)
    plt.ylabel('Belasting [%]', **hfont)
    set_tick_formatting()
    plt.ylim([30, 45])
    plt.xlim([0, max(gross_incomes)])

    plt.tight_layout()
    plt.savefig('income_tax.png')


def plot_total_tax(taxes: Taxes):
    income_start = 1
    income_end = 120000
    gross_incomes = range(income_start, income_end)
    tax_list = []
    tax_list_perc = []
    for gross_income in gross_incomes:
        nett, tax = taxes.calc_nett_income(gross_income)
        tax_list.append(tax)
        tax_list_perc.append(tax / gross_income * 100)

    plt.figure()
    plt.plot(gross_incomes, tax_list)
    plt.title('Inkomsten (bruto) vs belasting', **hfont)
    plt.xlabel('Bruto jaarinkomen [€]', **hfont)
    plt.ylabel('Belasting [€]', **hfont)
    set_tick_formatting()
    plt.xlim([0, max(gross_incomes)])
    plt.tight_layout()
    plt.savefig('total_tax.png')

    plt.figure()
    plt.plot(gross_incomes, tax_list_perc)
    plt.title('Belasting als deel van (bruto) inkomsten', **hfont)
    plt.xlabel('Bruto jaarinkomen [€]', **hfont)
    plt.ylabel('Belasting [%]', **hfont)
    set_tick_formatting()
    plt.ylim([0, 50])
    plt.xlim([0, max(gross_incomes)])
    plt.tight_layout()
    plt.savefig('total_tax_perc.png')


def main():
    tax_settings = load_settings('../../simulation/settings.yml')['taxes']
    taxes = Taxes(tax_settings)
    plot_working_tax_discount(taxes)
    plot_general_tax_discount(taxes)
    plot_income_tax_(taxes)
    plot_total_tax(taxes)
    SHOWPLOTS and plt.show()


if __name__ == "__main__":
    main()
    # import matplotlib.font_manager
    # # flist = matplotlib.font_manager.get_fontconfig_fonts()
    # # names = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist]
    # # print('\n'.join(names))
    # fontList = matplotlib.font_manager.fontManager.ttflist
    # # fontList = matplotlib.font_manager.findSystemFonts()
    # print(fontList[0].__dir__())
    # fonts = sorted([elem.name for elem in fontList])
    # # fonts = sorted([elem for elem in fontList])
    # print('\n'.join(fonts))

    # import matplotlib.font_manager
    #
    # weights = ['ultralight', 'light', 'normal', 'regular', 'book', 'medium',
    #            'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy',
    #            'extra bold', 'black']
    #
    # print('weight' + 6 * ' ', 'file name', '\n' + 70 * '-')
    # for weight in weights:
    #     fprops = matplotlib.font_manager.FontProperties(family='HelveticaNeue',
    #                                                     weight=weight)
    #     print(weight + (12 - len(weight)) * ' ', matplotlib.font_manager.findfont(fprops))
    # import matplotlib.font_manager
    # fpnts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    # print(fonts)
