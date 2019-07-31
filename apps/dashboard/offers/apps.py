from django.conf.urls import url

import oscar.apps.dashboard.offers.apps as apps
from oscar.core.loading import get_class


class OffersDashboardConfig(apps.OffersDashboardConfig):
    label = 'offers_dashboard'
    name = 'apps.dashboard.offers'
    verbose_name = 'Offers dashboard'

    def ready(self):
        super().ready()
        self.flash_sale_create_view = get_class('dashboard.offers.views', 'FlashSaleCreateView')

    def get_urls(self):
        urls = [
            url(r'^new/flash-sale/(?P<product_pk>\d+)/$', self.flash_sale_create_view.as_view(),
                name='create-flash-sale'),
        ]
        return super().get_urls() + self.post_process_urls(urls)
