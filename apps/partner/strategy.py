from collections import namedtuple

from oscar.apps.partner.strategy import Default as CoreDefault
from oscar.core.loading import get_class


UnavailablePrice = get_class('partner.prices', 'Unavailable')
FixedPrice = get_class('partner.prices', 'FixedPrice')
TaxInclusiveFixedPrice = get_class('partner.prices', 'TaxInclusiveFixedPrice')


# A container for policies
PurchaseInfo = namedtuple('PurchaseInfo', ['price', 'flash_price', 'availability', 'stockrecord'])


class Selector:

    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)


class FlashSalePolicy:

    def get_flash_pricing_policy(self, product, stockrecord, pricing_policy):
        if isinstance(pricing_policy, UnavailablePrice):
            return UnavailablePrice()

        benefit = product.get_flash_price_benefit()
        if not benefit:
            return UnavailablePrice()

        flash_price = benefit.calculate_flash_price(pricing_policy.excl_tax)
        if not pricing_policy.tax:
            tax = pricing_policy.tax
        else:
            rate = self.get_rate(product, stockrecord)
            exponent = self.get_exponent(stockrecord)
            tax = (flash_price * rate).quantize(exponent)

        return FixedPrice(
            currency=pricing_policy.currency,
            excl_tax=flash_price,
            tax=tax,
        )

    def flash_pricing_policy(self, product, stockrecord, pricing_policy):
        return self.get_flash_pricing_policy(product, stockrecord, pricing_policy)

    def parent_flash_pricing_policy(self, product, pricing_policy):
        children_stock = self.select_children_stockrecords(product)
        return self.get_flash_pricing_policy(product, children_stock[0], pricing_policy)

    def fetch_for_product(self, product, stockrecord=None):
        super_purchase_info = super().fetch_for_product(product, stockrecord)
        return PurchaseInfo(
            flash_price=self.flash_pricing_policy(product, stockrecord, super_purchase_info.price),
            **super_purchase_info._asdict(),
        )

    def fetch_for_parent(self, product):
        super_purchase_info = super().fetch_for_parent(product)
        return PurchaseInfo(
            flash_price=self.parent_flash_pricing_policy(product, super_purchase_info.price),
            **super_purchase_info._asdict(),
        )


class Default(FlashSalePolicy, CoreDefault):
    pass
