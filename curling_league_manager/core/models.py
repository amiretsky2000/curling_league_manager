# curling_league_manager/core/models.py
from dataclasses import dataclass, field
from typing import List
import uuid

@dataclass
class Member:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str

@dataclass
class Team:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    members: List[Member] = field(default_factory=list)

@dataclass
class League:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    teams: List[Team] = field(default_factory=list)
