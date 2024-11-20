from otree.api import *
import random

class Constants(BaseConstants):
    name_in_url = 'cm_trading'
    players_per_group = 4
    num_rounds = 1
    initial_endowment = cu(100)
    max_units = 10
    min_price = cu(1)
    max_price = cu(20)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    bid_price = models.CurrencyField(min=Constants.min_price, max=Constants.max_price, blank=True)
    ask_price = models.CurrencyField(min=Constants.min_price, max=Constants.max_price, blank=True)
    units_traded = models.IntegerField(min=0, max=Constants.max_units, blank=True)

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid_price', 'units_traded']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            endowment=Constants.initial_endowment
        )

class AskPage(Page):
    form_model = 'player'
    form_fields = ['ask_price', 'units_traded']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            endowment=Constants.initial_endowment
        )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_clearing_price_and_earnings'

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            clearing_price=group.clearing_price,
            earnings=player.earnings
        )

page_sequence = [Introduction, BidPage, AskPage, ResultsWaitPage, Results]

# FUNCTIONS
def set_clearing_price_and_earnings(group: Group):
    group.set_clearing_price()
    group.set_total_units_traded()
    group.set_earnings()

