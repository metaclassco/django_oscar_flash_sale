from oscar.core.loading import get_class


UnavailablePrice = get_class('partner.prices', 'Unavailable')
FixedPrice = get_class('partner.prices', 'FixedPrice')


def get_flash_price(request, product, purchase_info):
    price = purchase_info.price
    stockrecord = purchase_info.stockrecord

    if isinstance(price, UnavailablePrice):
        return UnavailablePrice()

    benefit = product.get_flash_price_benefit()
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
