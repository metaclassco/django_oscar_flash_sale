from itertools import chain

from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Applicator(CoreApplicator):

    def get_sale_offers(self):
        qs = ConditionalOffer.active.filter(offer_type=ConditionalOffer.SALE)
        return qs.select_related('condition', 'benefit')

    def get_offers(self, basket, user=None, request=None):
        site_offers = self.get_site_offers()
        basket_offers = self.get_basket_offers(basket, user)
        user_offers = self.get_user_offers(user)
        session_offers = self.get_session_offers(request)
        sale_offers = self.get_sale_offers()

        return list(
            sorted(chain(
                session_offers, basket_offers, user_offers, site_offers, sale_offers),
                key=lambda o: o.priority, reverse=True
            )
        )
