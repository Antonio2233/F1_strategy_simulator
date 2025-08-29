from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import math
import numpy as np

# ---------------------------- Base Models -----------------------------
@dataclass
class Track:
    name: str
    laps: int
    base_lap_time: float  # seconds under ideal conditions with reference tyre (Medium, lap 1, no fuel)
    pit_loss: float       # total loss for pit stop (entry + change + exit)
    fuel_effect: float    # penalty per 10 kg of fuel (s/10kg)
    tyre_warmup: float = 0.35  # seconds gained per lap during warmup window

@dataclass
class Compound:
    name: str              # "S", "M", "H" / Soft Hard Medium
    perf_delta: float      # delta vs reference tyre (negative = faster)
    deg_per_lap: float      # base linear degradation (s/lap)
    cliff_lap: Optional[int] = None  # from this lap onwards, a cliff is added (None = unused)
    cliff_penalty: float = 0.0       # extra s/lap after cliff
    warmup_laps: int = 1             # laps needed for warmup

@dataclass
class Car:
    start_fuel_kg: float   # starting fuel for race distance
    min_stop_lap: int = 1  # not allowed to pit before (lap 1 = after completing 1st lap)

@dataclass
class Stint:
    compound: Compound
    laps: int

@dataclass
class Strategy:
    name: str
    stints: List[Stint]

@dataclass
class Event:
    kind: str  # 'SC' o 'VSC' / Safety Car or Virtual Safety Car
    start_lap: int
    duration_laps: int
    pit_loss_factor: float  # pit loss multiplier during the event
    lap_time_factor: float  # lap time multiplier during the event