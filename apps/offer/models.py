from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.apps.offer.abstract_models import AbstractConditionalOffer


class ConditionalOffer(AbstractConditionalOffer):
    SITE, SALE, VOUCHER, USER, SESSION = "Site", "Sale", "Voucher", "User", "Session"
    TYPE_CHOICES = (
        (SITE, _("Site offer - available to all users")),
        (SALE, _("Sale offer - available to all users")),
        (VOUCHER, _("Voucher offer - only available after entering the appropriate voucher code")),
        (USER, _("User offer - available to certain types of user")),
        (SESSION, _("Session offer - temporary offer, available for a user for the duration of their session")),
    )
    offer_type = models.CharField(_("Type"), choices=TYPE_CHOICES, default=SITE, max_length=128)


from oscar.apps.offer.models import *  # noqa isort:skip
