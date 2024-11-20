from otree.api import *
import random

class Constants(BaseConstants):
    name_in_url = 'otc_trading'
    players_per_group = 4
    num_rounds = 1
    initial_endowment = cu(100)
    max_units = 10
    min_price = cu(1)
    max_price = cu(20)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    otc_clearing_price = models.CurrencyField(initial=0)
    total_units_traded = models.IntegerField(initial=0)

    def set_clearing_price(self):
        # Set clearing price based on submitted offers
        offers = [p.offer_price for p in self.get_players() if p.offer_price is not None]
        if offers:
            self.otc_clearing_price = sum(offers) / len(offers)
        else:
            self.otc_clearing_price = Constants.min_price

    def set_total_units_traded(self):
        # Calculate total units traded by summing individual trades
        self.total_units_traded = sum([p.units_traded for p in self.get_players() if p.units_traded is not None])

    def set_earnings(self):
        for p in self.get_players():
            p.calculate_earnings()

class Player(BasePlayer):
    participant_role = models.StringField()
    info_level = models.StringField(choices=['high', 'low'], doc="Indicates whether the player has high or low information.")
    offer_price = models.CurrencyField(min=Constants.min_price, max=Constants.max_price, blank=True)
    units_traded = models.IntegerField(min=0, max=Constants.max_units, blank=True)
    earnings = models.CurrencyField()
    final_endowment = models.CurrencyField(initial=Constants.initial_endowment)

    def calculate_earnings(self):
        # Calculate the player's earnings based on the units traded and the clearing price
        if self.units_traded is not None and self.group.otc_clearing_price:
            self.earnings = self.units_traded * self.group.otc_clearing_price
            self.final_endowment = Constants.initial_endowment - (self.units_traded * self.offer_price) + self.earnings

# Page Definitions
class IntroductionPage(Page):
    template_name = 'otc_trading/IntroductionPage.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Randomly assign roles to players
        if not player.participant_role:
            player.participant_role = random.choice(['Buyer', 'Seller'])
        # Randomly assign information level
        if not player.info_level:
            player.info_level = random.choice(['high', 'low'])
            print("INFORMATION LEVEL")

class RoleAssignmentPage(Page):
    template_name = 'otc_trading/RoleAssignmentPage.html'

    @staticmethod
    def is_displayed(player: Player):
        # Always ensure this page is displayed to assign roles before proceeding
        return player.round_number == 1

class OfferPage(Page):
    template_name = 'otc_trading/OfferPage.html'
    form_model = 'player'
    form_fields = ['offer_price']

    @staticmethod
    def is_displayed(player: Player):
        # Ensure that only players who are either Buyer or Seller see this page
        return player.participant_role == 'Buyer' or player.participant_role == 'Seller'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'role': player.participant_role,
            'info_level': player.info_level,
            'endowment': Constants.initial_endowment
        }

class TradePage(Page):
    template_name = 'otc_trading/TradePage.html'
    form_model = 'player'
    form_fields = ['units_traded']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant_role == 'Buyer' or player.participant_role == 'Seller'

    @staticmethod
    def vars_for_template(player: Player):
        return {
           'available_units': Constants.max_units,
           'clearing_price': player.group.otc_clearing_price if hasattr(player.group, 'otc_clearing_price') else 'To be determined'
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Set earnings for each player based on the negotiated price and units traded
        player.calculate_earnings()

class ResultsWaitPage(WaitPage):
    template_name = 'otc_trading/ResultsWaitPage.html'

    after_all_players_arrive = 'set_group_trades'

class ResultsPage(Page):
    template_name = 'otc_trading/ResultsPage.html'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'earnings': player.earnings,
            'final_endowment': player.final_endowment,
            'total_units_traded': player.group.total_units_traded if hasattr(player.group, 'total_units_traded') else 0
        }

# functions #
def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        player.participant_role = random.choice(['Buyer', 'Seller'])
        player.info_level = random.choice(['high', 'low'])

# Page Sequence
def set_group_trades(group: Group):
    group.set_clearing_price()
    group.set_total_units_traded()
    group.set_earnings()

page_sequence = [IntroductionPage, RoleAssignmentPage, OfferPage, TradePage, ResultsWaitPage, ResultsPage]

