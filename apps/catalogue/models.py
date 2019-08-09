from django.utils.timezone import now
from django.utils.functional import cached_property

from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Product(AbstractProduct):

    @cached_property
    def has_active_flash_sales(self):
        return self.includes.filter(
            benefit__offers__offer_type=ConditionalOffer.FLASH_SALE,
            benefit__offers__start_datetime__lt=now(),
            benefit__offers__end_datetime__gt=now(),
        ).exists()

    def get_flash_price_benefit(self):
        if self.has_active_flash_sales:
            range_ = self.includes.first()
            return range_.benefit_set.filter(offers__offer_type=ConditionalOffer.FLASH_SALE).first()


from oscar.apps.catalogue.models import *  # noqa isort:skip
