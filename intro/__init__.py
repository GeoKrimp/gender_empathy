from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    mturk_id = models.StringField(
        label="Please enter your Mechanical Turk Worker ID"
    )


class Welcome(Page):
    pass


class MTurkID(Page):
    form_model = 'player'
    form_fields = ['mturk_id']


page_sequence = [Welcome, MTurkID]