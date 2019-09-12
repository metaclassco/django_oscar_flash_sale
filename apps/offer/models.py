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

    def get_price_incl_discount(self, price):
        if self.type in [self.PERCENTAGE, self.FIXED]:
            return price - self.proxy().get_discount(price)

    @property
    def proxy_map(self):
        custom_proxy_map = super().proxy_map
        custom_proxy_map[self.PERCENTAGE] = get_class('offer.benefits', 'CustomPercentageDiscountBenefit')
        custom_proxy_map[self.FIXED] = get_class('offer.benefits', 'AbsoluteDiscountBenefit')
        return custom_proxy_map


from oscar.apps.offer.models import *  # noqa isort:skip
from .benefits import *  # noqa isort:skip
