from decimal import Decimal as D

from django.utils.timezone import now

from oscar.core.loading import get_class, get_model


UnavailablePrice = get_class('partner.prices', 'Unavailable')
FixedPrice = get_class('partner.prices', 'FixedPrice')


def is_product_on_sale(product):
    ConditionalOffer = get_model('offer', 'ConditionalOffer')
    return product.includes.filter(
        benefit__offers__offer_type=ConditionalOffer.FLASH_SALE,
        benefit__offers__start_datetime__lt=now(),
        benefit__offers__end_datetime__gt=now(),
    ).exists()


def get_flash_sale_benefit(product):
    ConditionalOffer = get_model('offer', 'ConditionalOffer')
    if is_product_on_sale(product):
        range_ = product.includes.first()
        return range_.benefit_set.filter(offers__offer_type=ConditionalOffer.FLASH_SALE).first()


def calculate_product_price_incl_discounts(product, price_data):
    benefit = get_flash_sale_benefit(product)

    if not benefit:
        return D('0.00')

    price = price_data.incl_tax if price_data.is_tax_known else price_data.excl_tax

    result = benefit.apply_to_product(price)
    return price - result.discount
