from otree.api import *
from pathlib import Path
import csv

_DATA_DIR = Path(__file__).resolve().parent / 'data'
_SURVEY_FILES = sorted(_DATA_DIR.glob('questionnaire*.csv')) if _DATA_DIR.exists() else []

def _max_items_across_csv(files):
    max_items = 1
    for p in files:
        try:
            with open(p, 'r', encoding='utf-8-sig', newline='') as f:
                r = csv.DictReader(f)
                count = 0
                for row in r:
                    q = (row.get('Question') or '').strip()
                    if q:
                        count += 1
                max_items = max(max_items, count)
        except Exception:
            pass
    return max_items

_MAX_ITEMS = _max_items_across_csv(_SURVEY_FILES)

class C(BaseConstants):
    NAME_IN_URL = 'multi_survey'
    PLAYERS_PER_GROUP = None

    # ΔΕΝ αναφερόμαστε στην C εδώ μέσα — υπολογίζουμε απευθείας τα paths.
    _DATA_DIR = Path(__file__).resolve().parent / 'data'
    DATA_DIR = _DATA_DIR
    SURVEY_FILES = sorted(_DATA_DIR.glob('questionnaire*.csv')) if _DATA_DIR.exists() else []

    # Όσες σελίδες (=όσα CSV). Αν δεν βρεθεί κανένα, κρατάμε 1 για να μην σκάει.
    NUM_ROUNDS = max(1, len(SURVEY_FILES))

    # Μέγιστος αριθμός ερωτήσεων ανά σελίδα (εύκολα αλλάζει).
    MAX_ITEMS_PER_PAGE = _MAX_ITEMS


class Subsession(BaseSubsession):
    def creating_session(self):
        surveys = []

        for i, path in enumerate(C.SURVEY_FILES, start=1):
            items = []
            # utf-8-sig για σωστό άνοιγμα σε αρχεία που ήρθαν από Excel/Windows
            with open(path, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    q = (row.get('Question') or '').strip()
                    if not q:
                        continue
                    # μάζεψε όλες τις Option N στήλες που έχουν περιεχόμενο
                    opts = []
                    k = 1
                    while True:
                        key = f'Option {k}'
                        if key in row and (row[key] or '').strip():
                            opts.append(row[key].strip())
                            k += 1
                        else:
                            break
                    items.append(dict(question=q, options=opts))

            surveys.append(dict(
                title=f'Questionnaire {i}',
                items=items[:C.MAX_ITEMS_PER_PAGE],
            ))

        if not surveys:
            # placeholder αν δεν υπάρχουν CSV
            surveys = [dict(title='Questionnaire 1 (no CSV found)', items=[])]

        self.session.vars['surveys'] = surveys
        self.session.vars['n_surveys'] = len(surveys)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Δημιουργούμε πεδία για μέχρι MAX_ITEMS_PER_PAGE απαντήσεις (επαναχρησιμοποιούνται ανά γύρο)
    for i in range(1, C.MAX_ITEMS_PER_PAGE + 1):
        locals()[f"resp_{i:03d}"] = models.StringField(blank=True)
    del i

    def current_survey(self):
        """Επιστρέφει το survey του τρέχοντος γύρου (1-based)."""
        surveys = self.session.vars.get('surveys', [])
        idx = min(self.round_number - 1, len(surveys) - 1)
        return surveys[idx] if surveys else dict(title='(empty)', items=[])
