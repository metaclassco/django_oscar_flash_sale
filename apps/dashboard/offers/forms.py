from django import forms

from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class MetaDataForm(forms.ModelForm):
    offer_type = forms.ChoiceField(choices=ConditionalOffer.TYPE_CHOICES[:2])

    class Meta:
        model = ConditionalOffer
        fields = 'name', 'description', 'offer_type'
