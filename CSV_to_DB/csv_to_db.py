import pandas as pd
from sqlalchemy import create_engine

csv_files = ["Peter_Harrington/Peter_Harrington_Data.csv", "Rare_and_Antique_Books/Rare_and_Antique_Books_Data.csv", "Temple_Rare_Books/temple_rare_books_data.csv", "World_of_Books/World_of_Books_Data.csv"]
database_file = "rare_books_database.db"
engine = create_engine(f'sqlite:///{database_file}')

frames = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    frames.append(df)
    
combined_df = pd.concat(frames, ignore_index=True)
combined_df.to_sql('combined_table', con=engine, index=False, if_exists='replace')

print(f"Combined data has been written to {database_file}.")