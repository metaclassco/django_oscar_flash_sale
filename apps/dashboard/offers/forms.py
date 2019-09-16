from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.core.loading import get_model
from oscar.forms import widgets


Benefit = get_model('offer', 'Benefit')


class FlashSaleForm(forms.Form):
    TYPE_CHOICES = (
        (Benefit.PERCENTAGE, _("Discount is a percentage off of the product's value")),
        (Benefit.FIXED_PRICE, _("Get the products that meet the condition for a fixed price")),
        (Benefit.FIXED_PER_PRODUCT, _("Discount is a fixed amount off of each product's value that match condition")),
    )

    start_datetime = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(), label=_("Start date"), required=False)
    end_datetime = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(), label=_("End date"), required=False)
    benefit_type = forms.ChoiceField(choices=TYPE_CHOICES)
    benefit_value = forms.DecimalField()
