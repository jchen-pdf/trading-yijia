from otree.api import *
import random

class Constants(BaseConstants):
    name_in_url = 'da_trading'
    players_per_group = 4
    num_rounds = 1
    initial_endowment = cu(100)
    max_units = 10
    min_price = cu(1)
    max_price = cu(20)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    clearing_price = models.CurrencyField()
    total_units_traded = models.IntegerField()

    def set_clearing_price(self):
        # For simplicity, set clearing price as the average of all offers
        offers = [p.offer_price for p in self.get_players() if p.offer_price is not None]
        if offers:
            self.clearing_price = sum(offers) / len(offers)
        else:
            self.clearing_price = Constants.min_price

    def set_total_units_traded(self):
        self.total_units_traded = sum(p.units_traded for p in self.get_players())

    def set_earnings(self):
        for p in self.get_players():
            p.earnings = (p.units_traded * self.clearing_price) + (Constants.initial_endowment - p.units_traded * p.offer_price)

class Player(BasePlayer):
    offer_price = models.CurrencyField(min=Constants.min_price, max=Constants.max_price, blank=True)
    units_traded = models.IntegerField(min=0, max=Constants.max_units, blank=True)
    earnings = models.CurrencyField()

    def role(self):
        return 'Trader'

