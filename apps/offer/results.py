from oscar.apps.offer.results import BasketDiscount


class ProductDiscount(BasketDiscount):
    def __str__(self):
        return '<Product discount of %s>' % self.discount
