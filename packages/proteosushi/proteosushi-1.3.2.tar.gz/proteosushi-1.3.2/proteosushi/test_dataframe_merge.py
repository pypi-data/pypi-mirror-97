"""Quick file to make sure merge is working as I expect"""
import pandas as pd
df_region = pd.read_csv("test_region_dataframe.csv")
df_subcell = pd.read_csv("test_subcell_dataframe.csv")
df_catalytic = pd.read_csv("test_catalytic_dataframe.csv")
df_extras = pd.read_csv("test_extras_dataframe.csv")

df = df_region
df = df.merge(df_subcell, how="outer", on="entry")
df.to_csv("test_merge_1.csv")
df = df.merge(df_catalytic, how="outer", on=["entry", " position"])
df.to_csv("test_merge_2.csv")
df = df.merge(df_extras, how="outer", on=["entry", " position"])
df.to_csv("test_merge_3.csv")
#EOF