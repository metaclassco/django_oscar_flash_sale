from django import template

from apps.offer import utils


register = template.Library()


@register.simple_tag
def is_product_on_sale(product):
    return utils.is_product_on_sale(product)


@register.simple_tag
def calculate_price_after_discount(request, product, purchase_info):
    return utils.calculate_price_after_discount(request, product, purchase_info)
