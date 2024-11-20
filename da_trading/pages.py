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
    pass

class Player(BasePlayer):
    bid_price = models.CurrencyField(min=Constants.min_price, max=Constants.max_price, blank=True)
    ask_price = models.CurrencyField(min=Constants.min_price, max=Constants.max_price, blank=True)
    units_traded = models.IntegerField(min=0, max=Constants.max_units, blank=True)
    earnings = models.CurrencyField()

# Page Definitions
class BidPage(Page):
    form_model = 'player'
    form_fields = ['bid_price']

    @staticmethod
    def is_displayed(player: Player):
        return player.role() == 'Buyer'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'endowment': Constants.initial_endowment
        }

class AskPage(Page):
    form_model = 'player'
    form_fields = ['ask_price']

    @staticmethod
    def is_displayed(player: Player):
        return player.role() == 'Seller'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'endowment': Constants.initial_endowment
        }

class TradePage(Page):
    form_model = 'player'
    form_fields = ['units_traded']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'available_units': Constants.max_units,
            'clearing_price': player.group.clearing_price if player.group.clearing_price else 'No trades yet'
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Determine the earnings for the player based on the units traded
        if player.units_traded is not None:
            player.earnings = (player.units_traded * player.group.clearing_price) + (Constants.initial_endowment - player.units_traded * player.bid_price)

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_group_trades'

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'earnings': player.earnings,
            'total_units_traded': player.group.total_units_traded if player.group.total_units_traded else 0
        }

# Page Sequence
def set_group_trades(group: Group):
    group.set_clearing_price()
    group.set_total_units_traded()
    group.set_earnings()

page_sequence = [BidPage, AskPage, TradePage, ResultsWaitPage, Results]

