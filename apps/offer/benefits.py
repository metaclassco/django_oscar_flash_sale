from decimal import Decimal as D

from oscar.apps.offer.benefits import AbsoluteDiscountBenefit, FixedPriceBenefit, PercentageDiscountBenefit
from .results import ProductDiscount


__all__ = ['PercentageDiscountBenefit', 'AbsoluteDiscountBenefit']


class CustomPercentageDiscountBenefit(PercentageDiscountBenefit):

    def apply_to_product(self, price):
        discount = self.round(self.value / D('100.0') * price)
        return ProductDiscount(discount)


class CustomFixedPriceBenefit(FixedPriceBenefit):
    def apply_to_product(self, price):
        discount = price - self.value
        return ProductDiscount(discount)


class CustomAbsoluteDiscountPerProductBenefit(AbsoluteDiscountBenefit):
    """
    Benefit, analogous to absolute discount benefit, but applicable to each
    and every item, matched by condition. E.g. if there are 3 products in
    the basket, applicable for discount, discount value will be applied 3
    times.
    """

    def apply_to_product(self, price):
        discount = self.round(self.value)
        return ProductDiscount(discount)

    def apply(self, basket, condition, offer, discount_amount=None,
              max_total_discount=None, **kwargs):

        line_tuples = self.get_applicable_lines(offer, basket)
        max_affected_items = self._effective_max_affected_items()
        num_affected_items = 0
        lines_to_discount = []
        for price, line in line_tuples:
            if num_affected_items >= max_affected_items:
                break
            qty = min(
                line.quantity_without_offer_discount(offer),
                max_affected_items - num_affected_items,
                line.quantity
            )
            lines_to_discount.append((line, price, qty))
            num_affected_items += qty

        discount_amount = self.value * num_affected_items
        return super().apply(
            basket, condition, offer, discount_amount=discount_amount, max_total_discount=max_total_discount, **kwargs
        )
