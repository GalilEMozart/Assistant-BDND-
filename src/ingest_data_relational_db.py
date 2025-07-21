#ingest data from csv to sqlitedatabase
import pandas as pd
from sqlalchemy import create_engine
import os


class Ingest_csv_to_sqlite():

    def __init__(self, CSV_DIR, name_db="bdnb"):
        
        self.name_db = name_db
        self.CSV_DIR = CSV_DIR
        self.engine = create_engine(f"sqlite:///db/{name_db}.sqlite3")


    def ingest(self) -> None:

        for csv_file in os.listdir(self.CSV_DIR):
            if csv_file.endswith(".csv"):
                table_name = os.path.splitext(csv_file)[0].lower()
                df = pd.read_csv(os.path.join(self.CSV_DIR, csv_file), sep=',', low_memory=False)
                df.to_sql(table_name, self.engine, if_exists="replace", index=False)
                print(f"Table `{table_name}` insérée avec {len(df)} lignes")



def main() -> None:

    ingestor = Ingest_csv_to_sqlite("data/etl_input")
    ingestor.ingest()
    
if __name__ == "__main__":
    main()
