from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional


@unique
class AgeRating(Enum):
    UNIVERSAL = "U"
    PARENTAL_GUIDANCE = "PG"
    AGE_12 = "12"  # Including 12A
    AGE_15 = "15"
    AGE_18 = "18"  # Including R18


@dataclass
class Film:
    imdb: str
    title: str
    year: int
    imdb_rating: float
    imdb_age: Optional[AgeRating] = None
    bbfc_age: Optional[AgeRating] = None
    trailer: Optional[str] = None
    genre: Optional[str] = None
    runtime_mins: Optional[int] = None
    plot: Optional[str] = None
    poster_url: Optional[str] = None
