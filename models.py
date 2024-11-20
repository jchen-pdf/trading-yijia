from otree.api import models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer


class Constants(BaseConstants):
    name_in_url = 'trading_experiment'
    players_per_group = 4
    num_rounds = 1
    treatments = ['OTC', 'Double Auction', 'Call Market']


class Subsession(BaseSubsession):
    treatment = models.StringField()

    def creating_session(self):
        # Assign treatment to subsession based on session configuration
        if 'treatment' in self.session.config:
            self.treatment = self.session.config['treatment']
        else:
            raise ValueError("Treatment type is missing from session configuration")


class Group(BaseGroup):
    # Example of some group-level variables for the trading experiment
    total_units_traded = models.IntegerField(initial=0)
    clearing_price = models.CurrencyField(initial=0)

    def set_clearing_price(self):
        # Set clearing price logic can go here
        pass


class Player(BasePlayer):
    # Variables for each participant in the trading experiment
    endowment = models.CurrencyField(initial=100)
    units_traded = models.IntegerField(initial=0)
    earnings = models.CurrencyField()

    def role(self):
        return 'Trader'

