import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
csv_path = base_dir / "Titanic-Dataset.csv"
df_csv = pd.read_csv(csv_path)

print(df_csv.head(1))
print(df_csv.tail())


## iloc : indices
#print(df_csv.iloc[0:3, 0:4])

## loc: Etiquetas
#print(df_csv.loc[0:2,["Survived","Age"]])