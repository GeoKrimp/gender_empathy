from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'dg_empathy'
    players_per_group = None
    num_rounds = 1

    endowment_cents = 20
    belief_bonus_cents = 20  # 0.20$

    treatments = [
        ('no', 'none'),
        ('no', 'man'),
        ('no', 'woman'),
        ('ai', 'none'),
        ('ai', 'man'),
        ('ai', 'woman'),
        ('human', 'none'),
        ('human', 'man'),
        ('human', 'woman'),
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # store session-wide average donation (computed after everyone decided)
    avg_donation = models.FloatField(initial=0)


class Player(BasePlayer):

    empathy_condition = models.StringField()
    receiver_gender = models.StringField()

    failed_comprehension = models.BooleanField(initial=False)

    # comprehension checks
    comp_self = models.FloatField(
        label="How much should you transfer to the other participant to maximize your income?",
        min=0, max=Constants.endowment_cents
    )
    comp_other = models.FloatField(
        label="How much should you transfer to maximize the other participant’s income?",
        min=0, max=Constants.endowment_cents
    )

    # DG decision (needs FloatField for 0.5 steps)
    donation = models.FloatField(min=0, max=Constants.endowment_cents)

    # belief elicitation
    belief_avg = models.FloatField(
        label="What do you think is the average amount that Person A will transfer to Person B in the same situation you just participated in, across all other pairs of participants in the study?",
        min=0, max=Constants.endowment_cents
    )

    belief_bonus = models.CurrencyField(initial=0)


def creating_session(subsession: Subsession):
    # Round-robin balanced assignment μέσα στο session
    for i, p in enumerate(subsession.get_players()):
        empathy, gender = Constants.treatments[i % len(Constants.treatments)]
        p.empathy_condition = empathy
        p.receiver_gender = gender


# ---------------- PAGES ----------------

class Instructions(Page):
    pass


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comp_self', 'comp_other']

    @staticmethod
    def error_message(player: Player, values):
        a = float(values['comp_self'])
        b = float(values['comp_other'])

        ok = (abs(a - 0.0) < 1e-9) and (abs(b - Constants.endowment_cents) < 1e-9)
        player.failed_comprehension = not ok

        if not ok:
            return "One or more answers are incorrect."

class Failed(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_comprehension


class Treatment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.failed_comprehension


class DictatorDecision(Page):
    form_model = 'player'
    form_fields = ['donation']

    @staticmethod
    def is_displayed(player: Player):
        return not player.failed_comprehension


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_avg']

    @staticmethod
    def is_displayed(player: Player):
        return not player.failed_comprehension


class End(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.failed_comprehension


page_sequence = [
    Instructions,
    Comprehension,
    Failed,
    Treatment,
    DictatorDecision,
    Belief,
    End,
]