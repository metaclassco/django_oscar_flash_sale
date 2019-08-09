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


def calculate_price_after_discount(request, product, purchase_info):
    price = purchase_info.price
    stockrecord = purchase_info.stockrecord

    if isinstance(price, UnavailablePrice):
        return UnavailablePrice()

    benefit = get_flash_sale_benefit(product)
    if not benefit:
        return UnavailablePrice()

    flash_price = benefit.calculate_flash_price(price.excl_tax)
    if not price.tax:
        tax = price.tax
    else:
        strategy = request.strategy
        rate = strategy.get_rate(product, stockrecord)
        exponent = strategy.get_exponent(stockrecord)
        tax = (flash_price * rate).quantize(exponent)

    return FixedPrice(
        currency=price.currency,
        excl_tax=flash_price,
        tax=tax,
    )
