import asyncio

import altair as alt
import streamlit as st
import pandas as pd

from utils.surreal_engine import connect_to_db


# Connect to the database
async def get_data_from_db():
    db = await connect_to_db()
    await db.use("bdo", "market_data")
    return await db.select("world_market_list")

print("Connecting to database...")
data = asyncio.run(get_data_from_db())
df = pd.DataFrame()
for item in data:
    df = df.append(item, ignore_index=True)

st.write(df)

st.bar_chart(df[['item_id', 'base_price', 'current_stock', 'total_trades']].set_index('item_id'))
