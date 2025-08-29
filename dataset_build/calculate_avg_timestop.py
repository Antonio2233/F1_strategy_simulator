
import pandas as pd
import os

output_file = "avg_timestop.csv"

df_init = pd.DataFrame(columns=["Grand Prix","AVG_timestop"])
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


    mask = df["PitOutTime"].notna() |  df["PitOutTime"].shift(-1).notna()
    df = df[mask]

    df_even  = df.iloc[::2]   # Even rows # or df[df.index % 2 == 0]
    df_odd  = df.iloc[1::2]  # Odd rows

    total = df_odd.reset_index(drop=True)["PitOutTime"] - df_even.reset_index(drop=True)["PitInTime"]
    total_result = total.sum()


    num_rows = len(df)

    print(total_result)
    print(num_rows)

    avg_timestop = total_result / num_rows

    new_row = pd.DataFrame({"Event": [event] ,"AVG_timestop": [avg_timestop]})
    new_row.to_csv(output_file, mode="a", header=False, index=False)
