from decimal import Decimal as D

from oscar.core.loading import get_class

from .results import ProductDiscount


PercentageDiscountBenefit = get_class('offer.benefits', 'PercentageDiscountBenefit')
AbsoluteDiscountBenefit = get_class('offer.benefits', 'AbsoluteDiscountBenefit')


__all__ = ['PercentageDiscountBenefit', 'AbsoluteDiscountBenefit']


class CustomPercentageDiscountBenefit(PercentageDiscountBenefit):

    def apply_to_product(self, price):
        discount = self.round(self.value / D('100.0') * price)
        return ProductDiscount(discount)


class CustomAbsoluteDiscountBenefit(AbsoluteDiscountBenefit):

    def apply_to_product(self, price):
        discount = self.round(self.value)
        return ProductDiscount(discount)
