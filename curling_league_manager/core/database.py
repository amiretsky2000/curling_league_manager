# curling_league_manager/core/database.py
import json
from pathlib import Path
from .models import League, Team, Member
from typing import List

class LeagueDatabase:
    def __init__(self):
        self.leagues: List[League] = []

    def load(self, filepath: str):
        raw = json.loads(Path(filepath).read_text())
        self.leagues = []
        for ld in raw:
            # Create the League, preserving id if present
            league = League(
                name=ld["name"],
                teams=[],
                id=ld.get("id")
            )
            # Rebuild each team
            for td in ld.get("teams", []):
                team = Team(
                    name=td["name"],
                    members=[],
                    id=td.get("id")
                )
                # Rebuild each member
                for md in td.get("members", []):
                    member = Member(
                        name=md["name"],
                        email=md["email"],
                        id=md.get("id")
                    )
                    team.members.append(member)
                league.teams.append(team)

            self.leagues.append(league)

    def save(self, filepath: str):
        data = [dataclass_to_dict(l) for l in self.leagues]
        Path(filepath).write_text(json.dumps(data, indent=2))

    def add_league(self, name: str):
        self.leagues.append(League(name=name))

    def remove_league(self, league_id: str):
        self.leagues = [l for l in self.leagues if l.id != league_id]

# Helper to convert nested dataclasses to dicts:
def dataclass_to_dict(obj):
    if hasattr(obj, "__dataclass_fields__"):
        result = {}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            if isinstance(value, list):
                result[field] = [dataclass_to_dict(v) for v in value]
            else:
                result[field] = value
        return result
    else:
        return obj
