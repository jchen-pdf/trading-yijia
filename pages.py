from otree.api import Page, WaitPage


class Introduction(Page):
    def is_displayed(self):
        # Show this page only in the first round
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'treatment': self.subsession.treatment,
            'endowment': self.player.endowment,
        }


class Trading(Page):
    form_model = 'player'
    form_fields = ['units_traded']

    def vars_for_template(self):
        return {
            'current_endowment': self.player.endowment,
            'total_units_traded': self.group.total_units_traded,
        }

    def before_next_page(self):
        # Logic to handle units traded by the player
        self.player.endowment -= self.player.units_traded * 10  # Assume each unit costs 10
        self.group.total_units_traded += self.player.units_traded


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        # Set clearing price after all players are done trading
        self.group.set_clearing_price()


class Results(Page):
    def vars_for_template(self):
        return {
            'units_traded': self.player.units_traded,
            'earnings': self.player.earnings,
            'clearing_price': self.group.clearing_price,
        }


page_sequence = [Introduction, Trading, ResultsWaitPage, Results]

