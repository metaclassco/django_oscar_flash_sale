from django import template


from apps.offer.utils import get_flash_price


register = template.Library()


@register.simple_tag
def flash_sale_price(request, product, purchase_info):
    return get_flash_price(request, product, purchase_info)
