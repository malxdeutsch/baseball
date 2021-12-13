from django.db import models

# Create your models here.


class Card(models.Model):
    CARD_POSITIONS = [
        ('P', 'Pitcher'),
        ('C', 'Catcher'),
        ('1B', 'First Base'),
        ('2B', 'Second Base'),
        ('3B', 'Third Base'),
        ('SS', 'Short Stop'),
        ('RF', 'Right Field'),
        ('LF', 'Left Field'),
        ('CF', 'Center Field'),
    ]

    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, choices=CARD_POSITIONS)

    def rarity(self):
        if self.position == 'P':
            return 5
        else:
            return 0

    def __str__(self):
        return self.name


class Trade (models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def viable_offers(self):
        return self.offer_set.filter(is_rejected=False)


class Offer (models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    profile = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    is_rejected = models.BooleanField(default=False)

    def accept(self):
        '''The trade.card should leave the trade.profile.deck and get added to the offer.profile.deck
        offer.card should leave offer.profile.deck and get added to the trade.profile.deck
        offer.trade.is_completed should become True '''
        if not self.trade.is_completed:
            self.trade.profile.deck.remove(self.trade.card)
            self.profile.deck.add(self.trade.card)
            self.trade.profile.deck.add(self.card)
            self.profile.deck.remove(self.card)
            self.trade.is_completed = True
            self.trade.save()
            return True
        return False

    def reject(self):
        self.is_rejected = True
        self.save()
