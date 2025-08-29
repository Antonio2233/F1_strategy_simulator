

import fastf1


###############################################################################
# Load the race session.


events = [
    "Pre-Season Testing",
    "Australian Grand Prix",
    'Chinese Grand Prix',
    'Japanese Grand Prix',
    'Bahrain Grand Prix',
    'Saudi Arabian Grand Prix',
    'Miami Grand Prix',
    "Emilia Romagna Grand Prix",
    'Monaco Grand Prix',
    'Spanish Grand Prix',
    'Canadian Grand Prix',
    'Austrian Grand Prix',
    'British Grand Prix',
    'Belgian Grand Prix',
    'Hungarian Grand Prix',
    'Dutch Grand Prix',
    'Italian Grand Prix',
    'Azerbaijan Grand Prix',
    'Singapore Grand Prix',
    'United States Grand Prix',
    'Mexico City Grand Prix',
    'São Paulo Grand Prix',
    'Las Vegas Grand Prix',
    'Qatar Grand Prix',
    'Abu Dhabi Grand Prix',
]

sesions = "R"
year = 2024

for event in events:
    race = fastf1.get_session(year, event, 'R')
    race.load()

    filename = str(year) + "_" + event + "_race" + ".csv"

    race.laps.to_csv(filename,index=False,encoding="utf-8")

