import time
import requests
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Numeric, TIMESTAMP
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
import os
from datetime import datetime


load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")


metadata = MetaData()

market_mood_log = Table(
    "market_mood_log",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("timestamp", TIMESTAMP, server_default=text("CURRENT_TIMESTAMP")),
    Column("pair", String(20)),
    Column("last_price", Numeric),
    Column("base_volume", Numeric),
    Column("change", Numeric),
    Column("mood", String(50)),
)

metadata.create_all(engine)


def get_market_mood(change, volume):
    change = float(change)
    volume = float(volume)
    if change > 5 and volume > 1000:
        return "Euphoria (Strong Bullish)"
    elif change > 1 and volume > 100:
        return "Bullish"
    elif change > 1:
        return "Weak Bullish"
    elif -1 <= change <= 1:
        return "Neutral"
    elif change < -5 and volume > 1000:
        return "Panic Selling (Strong Bearish)"
    elif change < -1 and volume > 100:
        return "Bearish"
    elif change < -1:
        return "Weak Bearish"
    else:
        return "Uncertain"


def fetch_market_data():
    """Fetch market data from the WhiteBit API."""
    try:
        response = requests.get("https://whitebit.com/api/v4/public/ticker", timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json()).T
    except (requests.RequestException, ValueError) as e:
        print(f"[ERROR] Data fetch failed: {e}")
        return pd.DataFrame()


def insert_market_mood_record(pair, last_price, volume, change, mood):
    """Insert or update a market mood record into the database."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO market_mood_log (pair, last_price, base_volume, change, mood)
                    VALUES (:pair, :last_price, :volume, :change, :mood)
                """),
                {"pair": pair, "last_price": last_price, "volume": volume, "change": change, "mood": mood}
            )
    except Exception as e:
        print(f"[ERROR] Database insert failed: {e}")


def clean_and_standardize_data(df):
    """Clean and normalize numeric data, and standardize categorical columns."""
    if df.empty:
        return df

    df = df[df.index.str.endswith("_UAH")]

    for col in ["last_price", "base_volume", "change"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=["last_price", "base_volume", "change"], inplace=True)

    scaler = MinMaxScaler()
    df[["last_price", "base_volume", "change"]] = scaler.fit_transform(df[["last_price", "base_volume", "change"]])

    df["timestamp"] = datetime.now().isoformat()

    return df


def process_market_data():
    """Main pipeline for fetching, cleaning, analyzing, and storing data."""
    df = fetch_market_data()
    df = clean_and_standardize_data(df)

    if df.empty:
        print("[WARNING] No valid market data found. Skipping iteration.")
        return

    max_row = df.loc[df["change"].idxmax()]
    pair = max_row.name
    last_price, volume, change = max_row["last_price"], max_row["base_volume"], max_row["change"]
    mood = get_market_mood(change, volume)

    print(f"{datetime.now().strftime('%H:%M:%S')} | {pair} | Mood: {mood}")

    insert_market_mood_record(pair, last_price, volume, change, mood)


if __name__ == "__main__":
    for i in range(10):
        process_market_data()
        time.sleep(1)