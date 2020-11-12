# Simulation to compare different (personal) financial scenarios
from enum import Enum

import matplotlib.pyplot as plt
import seaborn as sns

import yaml

settings_file = 'settings.yml'


def load_settings():
    with open(settings_file) as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
    return settings


class MortgageType(Enum):
    LINEAR = 'linear'
    ANNUITY = 'annuity'


def perc_2_float(perc: str):
    return float(perc.replace('%', '')) / 100


class Mortgage:
    def __init__(self, rate, size, duration, type: MortgageType):
        self._rate = perc_2_float(rate)
        self._original_size = int(size)
        self._size = int(size)
        self._duration = int(duration)
        self._type = type
        self._annuity = self._calc_annuity()

    def _calc_interest(self):
        # TODO should this be different than just a simple division by the amount of months?
        return self._size * self._rate / 12

    def _calc_annuity(self):
        # https: // www.hypotheekrente - annuiteitenhypotheek.nl / annuiteit - berekenen.php
        n_periods = self._duration * 12
        monthly_interest = self._rate / 12
        return (monthly_interest / (1 - ((1 + monthly_interest) ** -n_periods))) * self._original_size

    def repay(self):
        if self._type == MortgageType.LINEAR:
            interest = self._calc_interest()
            payoff = self._original_size / self._duration / 12
            self._size -= min(payoff, self._size)
            total_payment = payoff + interest
        else:
            interest = self._calc_interest()
            payoff = self._annuity - interest
            self._size -= min(payoff, self._size)
            total_payment = self._annuity

        return total_payment, interest

    @property
    def size(self):
        return self._size


def calc_nett_payment(gross_payment, interest_payment):
    payoff = gross_payment - interest_payment
    return payoff + (1 - 0.3705) * interest_payment


def simulate(mortgage: Mortgage, settings):
    gross_payments = []
    nett_payments = []
    interest_payments = []
    size = []
    for ii in range(settings['simulation']['length']*12):
        gross_payment, interest_payment = mortgage.repay()

        gross_payments.append(gross_payment)
        interest_payments.append(interest_payment)

        nett_payment = calc_nett_payment(gross_payment, interest_payment)
        nett_payments.append(nett_payment)

        size.append(mortgage._size)

    sns.set()
    print(gross_payments)
    print(nett_payments)
    print(interest_payments)

    plt.plot(gross_payments, label='gross')
    plt.plot(nett_payments, label='nett')
    plt.plot(interest_payments, label='interest')
    plt.legend()
    plt.ylim(0, max(gross_payments) * 1.1)
    plt.show()

    plt.plot(size)
    plt.show()


def init_mortgage(settings):
    rate = settings['interest_rate']
    size = settings['size']
    duration = settings['duration']
    mortgage_type = MortgageType(settings['type'])
    return Mortgage(rate, size, duration, mortgage_type)


def main():
    settings = load_settings()
    mortgage = init_mortgage(settings['mortgage'])
    simulate(mortgage, settings)


if __name__ == '__main__':
    main()
