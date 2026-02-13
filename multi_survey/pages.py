from otree.api import *
from .models import C, Subsession, Group, Player

class Survey(Page):
    form_model = 'player'

    def is_displayed(self):
        # Δείξε σελίδα μόνο μέχρι τον αριθμό των διαθέσιμων CSV
        return self.round_number <= self.session.vars.get('n_surveys', 1)

    def get_form_fields(self):
        items = self.player.current_survey()['items']
        n = len(items)
        return [f"resp_{i:03d}" for i in range(1, n + 1)]

    def vars_for_template(self):
        surveys_total = self.session.vars.get('n_surveys', 1)
        survey = self.player.current_survey()
        # Ετοιμάζουμε στοιχεία για rendering
        prepared = []
        for i, it in enumerate(survey['items'], start=1):
            prepared.append(dict(
                field=f"resp_{i:03d}",
                question=it['question'],
                options=it['options'],
            ))
        progress = round(self.round_number / max(1, surveys_total) * 100)
        return dict(
            page_title=survey['title'],
            items=prepared,
            step=self.round_number,
            steps_total=surveys_total,
            progress=progress,
        )

page_sequence = [Survey]
