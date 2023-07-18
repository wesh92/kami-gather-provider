import pathlib
from logging import info

import polars as pl

data_dir = pathlib.Path(__file__).parent.parent

files = list(data_dir.glob("*.csv"))
for file in files:
    info(f"Reading {file}")

    df_item_data = pl.read_csv(file)

    connection_uri = "postgresql://bdo_data:bdo_123456@localhost:5433/bdo_data"

    df_item_data.write_database(
        table_name="item_data",
        if_exists="replace",
        connection_uri=connection_uri,
    )
    info(f"Finished writing {file}")
