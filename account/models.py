from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField()
    points = models.IntegerField(default=0)
    deck = models.ManyToManyField('trading_outpost.Card')

    def deal_cards(self):
        cards = self.__class__.deck.field.related_model.objects.all()
        random_cards = random.sample(list(cards), 10)
        self.deck.add(*random_cards)



