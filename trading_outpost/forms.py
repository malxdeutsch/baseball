from django import forms
from django.forms import ModelForm
from .models import Card, Trade, Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['card']
        
    def __init__(self, user, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['card'].queryset= user.profile.deck.all()
        
# class OfferForm (forms.Form):
#     trade = forms.ModelChoiceField(queryset=Card.objects.all())
#     def __init__(self, *args, **kwargs):
#         super(OfferForm, self).__init__(*args, **kwargs)