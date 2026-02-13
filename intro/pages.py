from otree.api import *
from .models import C, Subsession, Group, Player

class Welcome(Page):
    """
    Απλά welcome / instructions πριν ξεκινήσει οτιδήποτε άλλο.
    """


    def vars_for_template(self):
        return dict(
            # αν θες να αλλάξεις duration / πληρωμή, άλλαξέ τα εδώ
            estimated_minutes=30,
            show_up_fee=self.session.config.get('participation_fee', 0),
        )


page_sequence = [Welcome]
