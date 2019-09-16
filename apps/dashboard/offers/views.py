from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from oscar.core.loading import get_model

from .forms import FlashSaleForm


Product = get_model('catalogue', 'Product')
Range = get_model('offer', 'Range')
Condition = get_model('offer', 'Condition')
ConditionalOffer = get_model('offer', 'ConditionalOffer')
Benefit = get_model('offer', 'Benefit')


class FlashSaleCreateView(FormView):
    form_class = FlashSaleForm
    template_name = 'oscar/dashboard/offers/flash_sale_form.html'

    def dispatch(self, request, *args, **kwargs):
        product_pk = self.kwargs.get('product_pk', None)
        self.product = get_object_or_404(Product, pk=product_pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        benefit_type = form.cleaned_data['benefit_type']
        benefit_value = form.cleaned_data['benefit_value']
        start_datetime = form.cleaned_data['start_datetime']
        end_datetime = form.cleaned_data['end_datetime']
        range_name = 'Product range for product "%s(#%s)"' % (self.product.get_title(), self.product.pk)
        product_range, created = Range.objects.get_or_create(name=range_name)
        if created:
            product_range.add_product(self.product)

        condition = Condition.objects.create(range=product_range, type=Condition.COUNT, value=1)
        benefit = Benefit.objects.create(range=product_range, type=benefit_type, value=benefit_value)
        offer_name = 'Flash sale for product "%s(#%s)" from %s till %s' % (
            self.product.get_title(),
            self.product.pk,
            start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        )
        offer = ConditionalOffer.objects.create(
            name=offer_name, offer_type=ConditionalOffer.FLASH_SALE, condition=condition, benefit=benefit,
            start_datetime=start_datetime, end_datetime=end_datetime
        )
        url = reverse_lazy('dashboard:offer-detail', args=(offer.pk,))
        return HttpResponseRedirect(url)
