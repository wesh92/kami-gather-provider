import pathlib

import pandas as pd
import streamlit as st
import toml
from pymongo import MongoClient

# Set the path to the current script
current_file = pathlib.Path(__file__).resolve()

# Construct the path to the .secrets.toml file
secrets_path = current_file.parents[2] / "src" / "v1" / "config" / ".secrets.toml"

# Load the .toml file
with open(secrets_path) as f:
    secrets = toml.load(f)


# Define a function to fetch data
def fetch_data(item_id) -> list:
    # Replace the following lines with your existing connection string and filter
    connection_string = f"mongodb://{secrets['DB_USER']}:{secrets['DB_PASS']}@localhost:27017/?authMechanism=DEFAULT&tls=false"  # noqa: E501
    db_name = "bdo"
    report_name = "report__absolute_trade_differences"

    client = MongoClient(connection_string)
    filter = {"_id.item_id": item_id} if item_id is not None else {}
    result = client[db_name][report_name].find(filter=filter)

    data = []
    for document in result:
        data.append(document)

    return data


# Define a function to convert data to DataFrame
def to_dataframe(data) -> pd.DataFrame:
    formatted_data = []
    for doc in data:
        formatted_data.append(
            {
                "region": doc["_id"]["region"],
                "item_id": doc["_id"]["item_id"],
                "base_price": doc["current_details"]["base_price"],
                "stock": doc["current_details"]["stock"],
                "trades": doc["current_details"]["trades"],
                "at_time": doc["current_details"]["at_time"],
                "total_trade_difference": doc["total_trade_difference"],
            }
        )

    return pd.DataFrame(formatted_data)


def main() -> None:
    st.title("Market Data")

    state = st.session_state.get(item_id=None, stock_filter=0)

    # Input for item ID
    item_id_input = st.text_input("Enter Item ID (leave empty for None)", state.item_id)
    if item_id_input == "":
        state.item_id = None
    else:
        try:
            state.item_id = int(item_id_input)
        except ValueError:
            st.error("Invalid input. Please enter a number or leave empty for None.")
            st.stop()

    # Slider to filter stock
    state.stock_filter = st.slider("Filter stock", 0, 1000000, state.stock_filter)

    # Fetch and process data
    data = fetch_data(state.item_id)
    data_df = to_dataframe(data)
    filtered_df = data_df[data_df["stock"] <= state.stock_filter]

    # Display data
    st.write("Base Price by Region and Time")
    st.table(filtered_df[["region", "at_time", "base_price"]])

    st.write("Stock by Region and Time")
    st.table(filtered_df[["region", "at_time", "stock"]])

    st.write("Trades by Region and Time")
    st.table(filtered_df[["region", "at_time", "trades"]])

    st.write("Total Trade Difference by Region and Time")
    st.table(filtered_df[["region", "at_time", "total_trade_difference"]])


def page_selector() -> str:
    st.sidebar.title("Navigation")
    return st.sidebar.selectbox("Choose a page", ["Home", "Market Data"])
