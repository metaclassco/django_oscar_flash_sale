from django.db import models
from django.utils.translation import gettext_lazy as _

from oscar.apps.offer.abstract_models import AbstractConditionalOffer, AbstractBenefit
from oscar.core.loading import get_class


class ConditionalOffer(AbstractConditionalOffer):
    SITE, FLASH_SALE, VOUCHER, USER, SESSION = "Site", "Flash Sale", "Voucher", "User", "Session"
    TYPE_CHOICES = (
        (SITE, _("Site offer - available to all users")),
        (FLASH_SALE, _("Flash Sale offer - short-term discount for the specific product")),
        (VOUCHER, _("Voucher offer - only available after entering the appropriate voucher code")),
        (USER, _("User offer - available to certain types of user")),
        (SESSION, _("Session offer - temporary offer, available for a user for the duration of their session")),
    )
    offer_type = models.CharField(_("Type"), choices=TYPE_CHOICES, default=SITE, max_length=128)


class Benefit(AbstractBenefit):
    PERCENTAGE, FIXED, MULTIBUY, FIXED_PRICE, FIXED_PER_PRODUCT = (
        "Percentage", "Absolute", "Multibuy", "Fixed price", "Fixed per product")
    SHIPPING_PERCENTAGE, SHIPPING_ABSOLUTE, SHIPPING_FIXED_PRICE = (
        'Shipping percentage', 'Shipping absolute', 'Shipping fixed price')

    TYPE_CHOICES = (
        (PERCENTAGE, _("Discount is a percentage off of the product's value")),
        (FIXED, _("Discount is a fixed amount off of the product's value")),
        (FIXED_PER_PRODUCT, _("Discount is a fixed amount off of each product's value that match condition")),
        (MULTIBUY, _("Discount is to give the cheapest product for free")),
        (FIXED_PRICE,
         _("Get the products that meet the condition for a fixed price")),
        (SHIPPING_ABSOLUTE,
         _("Discount is a fixed amount of the shipping cost")),
        (SHIPPING_FIXED_PRICE, _("Get shipping for a fixed price")),
        (SHIPPING_PERCENTAGE, _("Discount is a percentage off of the shipping"
                                " cost")),
    )
    type = models.CharField(_("Type"), max_length=128, choices=TYPE_CHOICES, blank=True)

    def apply_to_product(self, price):
        if self.type in [self.PERCENTAGE, self.FIXED_PRICE, self.FIXED_PER_PRODUCT]:
            return self.proxy().apply_to_product(price)

    @property
    def proxy_map(self):
        custom_proxy_map = super().proxy_map
        custom_proxy_map[self.PERCENTAGE] = get_class('offer.benefits', 'CustomPercentageDiscountBenefit')
        custom_proxy_map[self.FIXED_PRICE] = get_class('offer.benefits', 'CustomFixedPriceBenefit')
        custom_proxy_map[self.FIXED_PER_PRODUCT] = get_class(
            'offer.benefits', 'CustomAbsoluteDiscountPerProductBenefit'
        )
        return custom_proxy_map


from oscar.apps.offer.models import *  # noqa isort:skip
from .benefits import *  # noqa isort:skip
