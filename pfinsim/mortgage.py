from enum import Enum

from .common import perc_2_float


class MortgageType(Enum):
    LINEAR = 'linear'
    ANNUITY = 'annuity'


class Mortgage:
    def __init__(self, rate, size, duration, type: str):
        self._rate = perc_2_float(rate)
        self._original_size = int(size)
        self._size = int(size)
        self._duration = int(duration)
        self._type = MortgageType(type)
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
