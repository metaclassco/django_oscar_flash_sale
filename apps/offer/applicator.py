from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_model


class Applicator(CoreApplicator):

    def get_site_offers(self):
        """
        Return site offers that are available to all users
        """
        ConditionalOffer = get_model('offer', 'ConditionalOffer')
        qs = ConditionalOffer.active.filter(offer_type__in=[ConditionalOffer.SITE, ConditionalOffer.SALE])
        # Using select_related with the condition/benefit ranges doesn't seem
        # to work.  I think this is because both the related objects have the
        # FK to range with the same name.
        return qs.select_related('condition', 'benefit')
