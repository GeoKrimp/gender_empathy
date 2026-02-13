# pages.py

from otree.api import *
from . import models as app_models
C = app_models.C
Player = app_models.Player

class Empathy(Page):

    @staticmethod
    def is_displayed(player: Player):
        # Εμφανίζεται ΜΟΝΟ αν έχουμε AI ή HUMAN empathy
        return player.empathy_condition in ['ai', 'human']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            # αν χρειαστείς κάτι έξτρα στο template
        )


class DictatorDecision(Page):
    form_model = Player
    form_fields = ['donation']
