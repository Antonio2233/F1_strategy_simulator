
import pandas as pd
import os

output_file = "tyre_warmup.csv"

df_init = pd.DataFrame(columns=["Grand Prix","tyre_warmup"])
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

    df["LapTime"] = pd.to_timedelta(df["LapTime"])

    

    mask = df["PitOutTime"].notna() | df["PitOutTime"].shift().notna() | df["PitOutTime"].shift(+2).notna() | df["PitOutTime"].shift(+3).notna() |df["PitOutTime"].shift(+4).notna()
    df = df[mask]

    df_even  = df.iloc[::2]   # Even rows # or df[df.index % 2 == 0]

    push1 = df.loc[df["TyreLife"] == 2, "LapTime"].mean()

    nextlaps = df.loc[df["TyreLife"].isin([3,4,5]), "LapTime"].mean()


    tyre_warmup = push1/nextlaps

    # print(tyre_warmup)


    new_row = pd.DataFrame({"Event": [event] ,"tyre_warmup": [tyre_warmup]})

    new_row.to_csv(output_file, mode="a", header=False, index=False)
    

    # Example:
    # Lap 20 → pit entry (PitInTime).
    # Lap 21 → out-lap (exits the pits, warms up the tyres, slower lap time). OUTLAP
    # Lap 22 → first push lap (already at race pace, but still penalized by cold tyres). OUTLAP + 1
    # Laps 23–25 → following laps, where the pace is already stable. OUTLAP + 2...
    # We calculate the average lap time of laps 23–25 and divide the push lap time by this average:
    # tyre_warmup = push1 / nextlaps
    # Example: tyre_warmup = 0.91
    # 0.91 means the first push lap was 9% faster than the following laps.