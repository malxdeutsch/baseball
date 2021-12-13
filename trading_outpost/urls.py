from django.urls import path
from . import views


urlpatterns = [
    path('homepage/', views.UnacceptedOffersListView.as_view(), name='homepage'),
    path('trade/<int:pk>/', views.TradeDetailView.as_view(), name='trade'),
    path('newtrade/<int:card_pk>/',
         views.TradeCreateView.as_view(), name='newtrade'),
    path('offertrade/<int:trade_pk>/',
         views.OfferCreateView.as_view(), name='offertrade'),
    path('handleoffer/<int:offer_pk>/<str:status>/',
         views.HandleOfferView.as_view(), name='handleoffer')
]
