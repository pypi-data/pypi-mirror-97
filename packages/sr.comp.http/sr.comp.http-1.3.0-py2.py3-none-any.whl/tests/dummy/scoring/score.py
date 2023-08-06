
from __future__ import absolute_import

from score_logic import score_team, tidy_slots, tidy_zones, validate_team

class Scorer:
    def __init__(self, scoresheet, arena_data_unused = None):
        self._scoresheet = scoresheet

    def calculate_scores(self):
        scores = {}
        for tla, score_data in self.isolated_scores.items():
            scores[tla] = score_team(score_data)
        return scores

    @property
    def isolated_scores(self):
        """
        The input format of the score sheet contains information about
        which team has how many tokens in a zone. We don't really care
        about this level, and really want to know _who owns_ each zone.
        Similarly, it's more useful have a list of which slots a team
        owns, rather than a map of slot to whether or not they own it.

        This method performs these tidyups and returns a new dictionary.
        In the process, we also ensure that there are no clashes.
        """

        zone_tokens = {}
        slot_bottoms = {}
        for tla, team_data in self._scoresheet.items():
            validate_team(tla, team_data)
            zone_tokens[tla] = team_data['zone_tokens']
            slot_bottoms[tla] = team_data['slot_bottoms']

        zones_owned = tidy_zones(zone_tokens)
        slots_owned = tidy_slots(slot_bottoms)

        isolated = {}
        for tla, team_data in self._scoresheet.items():
            isolated[tla] = {
                'robot_moved': team_data['robot_moved'],
                'slots_owned': slots_owned[tla],
                'upright_tokens': team_data['upright_tokens'],
                'zones_owned': zones_owned[tla],
            }

        return isolated
