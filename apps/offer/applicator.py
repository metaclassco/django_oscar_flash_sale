from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Applicator(CoreApplicator):

    def get_site_offers(self):
        qs = ConditionalOffer.active.filter(offer_type__in=[ConditionalOffer.SITE, ConditionalOffer.SALE])
        return qs.select_related('condition', 'benefit')
