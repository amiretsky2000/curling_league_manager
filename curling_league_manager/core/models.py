# curling_league_manager/core/models.py
# curling_league_manager/core/models.py
from dataclasses import dataclass, field
from typing import List
import uuid

@dataclass
class Member:
    name: str
    email: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class Team:
    name: str
    members: List[Member] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class League:
    name: str
    teams: List[Team] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
