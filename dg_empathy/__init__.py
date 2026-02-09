from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'dg_empathy'
    players_per_group = None
    num_rounds = 1

    endowment = 20

    treatments = [
        ('no', 'none'),
        ('no', 'woman'),
        ('no', 'man'),
        ('ai', 'none'),
        ('ai', 'woman'),
        ('ai', 'man'),
        ('human', 'none'),
        ('human', 'woman'),
        ('human', 'man'),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    empathy_condition = models.StringField()
    receiver_gender = models.StringField()

    donation = models.IntegerField(
        min=0,
        max=Constants.endowment,
        label=""
    )


def creating_session(subsession: Subsession):
    for i, player in enumerate(subsession.get_players()):
        empathy, gender = Constants.treatments[i % len(Constants.treatments)]
        player.empathy_condition = empathy
        player.receiver_gender = gender


class Instructions(Page):
    pass


class Empathy(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.empathy_condition in ['ai', 'human']


class DictatorDecision(Page):
    form_model = 'player'
    form_fields = ['donation']


class Results(Page):
    pass


page_sequence = [
    Instructions,
    Empathy,
    DictatorDecision,
    Results,
]
