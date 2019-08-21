from decimal import Decimal as D

from oscar.core.loading import get_class

PercentageDiscountBenefit = get_class('offer.benefits', 'PercentageDiscountBenefit')
AbsoluteDiscountBenefit = get_class('offer.benefits', 'AbsoluteDiscountBenefit')


class CustomPercentageDiscountBenefit(PercentageDiscountBenefit):

    def get_discount(self, price):
        return self.round(self.value / D('100.0') * price)


class CustomAbsoluteDiscountBenefit(AbsoluteDiscountBenefit):

    def get_discount(self, price):
        return self.round(self.value)
