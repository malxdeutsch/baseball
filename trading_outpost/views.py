from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from django.contrib.auth.models import User
from .models import Card, Trade, Offer
from django.contrib import messages
# Create your views here.
from .forms import OfferForm


class UnacceptedOffersListView(ListView):
    model = Trade
    template_name = 'homepage.html'
    queryset = Trade.objects.filter(is_completed=False)


class TradeDetailView(DetailView):
    model = Trade
    template_name = 'tradedetails.html'
    queryset = Trade.objects.filter(is_completed=False)


class TradeCreateView(RedirectView):
    pattern_name = 'homepage'

    def get_redirect_url(self, *args, **kwargs):
        card = Card.objects.get(id=self.kwargs['card_pk'])
        if card in self.request.user.profile.deck.all():
            trade, created = Trade.objects.get_or_create(
                card=card, profile=self.request.user.profile, is_completed=False)
            if created:
                messages.success(
                    self.request, f'Successful trade for {card.name}!')
            else:
                messages.warning(
                    self.request, f'This card is currently being traded.')
        else:
            messages.error(self.request, 'You can\'t trade others\' cards')
        return super().get_redirect_url()


class OfferCreateView(CreateView):
    form_class = OfferForm
    template_name = 'offertrade.html'

    def get_success_url(self):
        return reverse_lazy('trade', kwargs={'pk': self.object.trade.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        offer = form.save(commit=False)
        offer.profile = self.request.user.profile
        offer.trade_id = self.kwargs['trade_pk']
        offer.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        trade = get_object_or_404(Trade, id=self.kwargs['trade_pk'])
        if trade.profile == self.request.user.profile:
            messages.error(
                self.request, 'You can\'t make an offer on your own trade.')
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)


class HandleOfferView(RedirectView):
    pattern_name = 'myprofile'

    def get_redirect_url(self, *args, **kwargs):
        offer = get_object_or_404(Offer, id=self.kwargs['offer_pk'])
        if self.request.user == offer.trade.profile.user:
            if self.kwargs['status'] == 'accept':
                if offer.accept():
                    messages.success(
                        self.request, 'Offer accepted successfully')
                else:
                    messages.warning(
                        self.request, 'Trade was already completed.')
            else:
                offer.reject()
                messages.success(self.request, 'Offer rejected successfully')
        else:
            messages.warning(
                self.request, 'You can\'t accept offers for other folks.')

        kwargs.clear()
        return super().get_redirect_url(*args, **kwargs)
