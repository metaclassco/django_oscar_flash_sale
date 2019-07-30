from decimal import Decimal as D

from django.db import models
from django.utils.translation import gettext_lazy as _

from oscar.apps.offer.abstract_models import AbstractConditionalOffer, AbstractBenefit


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

    def calculate_flash_price(self, price):
        if self.type == self.PERCENTAGE:
            return price - self.value / D('100.0') * price

        elif self.type == self.FIXED:
            return price - self.value

        elif self.type == self.FIXED_PRICE:
            return self.value


from oscar.apps.offer.models import *  # noqa isort:skip
