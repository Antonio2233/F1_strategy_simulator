
import pandas as pd
import os

output_file = "base_laptime.csv"

df_init = pd.DataFrame(columns=["Grand Prix","base_laptime"])
df_init.to_csv(output_file, index=False)

year=2024

events = [
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



for event in events:
    filename = str(year) + "/" + str(year) + "_" + event + "_race" + ".csv"
    df = pd.read_csv(filename)

    df['LapNumber'] = df['LapNumber'].astype(int)

    df['LapTime'] = pd.to_timedelta(df['LapTime'])
    df['Sector1Time'] = pd.to_timedelta(df['Sector1Time'])
    df['Sector2Time'] = pd.to_timedelta(df['Sector2Time'])
    df['Sector3Time'] = pd.to_timedelta(df['Sector3Time'])


    min_lap = df['LapTime'].min()
    min_sector1 = df['Sector1Time'].min()
    min_sector2 = df['Sector2Time'].min()
    min_sector3 = df['Sector3Time'].min()

    # 3SectorMinSum
    totalSector = min_sector1+min_sector2+min_sector3


    new_row = pd.DataFrame({"Event": [event] ,"base_laptime": [totalSector]})

    new_row.to_csv(output_file, mode="a", header=False, index=False)


