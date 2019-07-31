from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.core.loading import get_model
from oscar.forms import widgets


Benefit = get_model('offer', 'Benefit')


class FlashSaleForm(forms.Form):
    start_datetime = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(), label=_("Start date"), required=False)
    end_datetime = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(), label=_("End date"), required=False)
    benefit_type = forms.ChoiceField(choices=Benefit.TYPE_CHOICES[0:2])
    benefit_value = forms.DecimalField()
