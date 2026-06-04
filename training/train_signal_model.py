import os
import glob
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split


DATA_DIR = "data\\ml_data"
MODEL_DIR = "models"
MODEL_PATH = "models\\signal_model.pkl"


def load_all_stock_data():
    """
    Load all CSV files from data/ml_data.
    """

    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found inside data/ml_data")

    dataframes = []

    for file_path in csv_files:
        file_name = os.path.basename(file_path).replace(".csv", "")

        if file_name.lower() == "stock_metadata":
            print("Skipping metadata file:", file_path)
            continue
        df = pd.read_csv(file_path)

        df["symbol"] = file_name.upper()

        dataframes.append(df)

    final_df = pd.concat(dataframes, ignore_index=True)

    return final_df


def prepare_dataset(df):
    """
    Prepare ML features and labels.

    Label logic:
    future_return > 1%  -> BUY
    future_return < -1% -> SELL
    otherwise           -> HOLD
    """

    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    required_columns = ["date", "open", "high", "low", "close", "volume", "symbol"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column missing: {col}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["symbol", "date"])

    df["daily_return"] = df.groupby("symbol")["close"].pct_change()
    df["price_range"] = (df["high"] - df["low"]) / df["close"]
    df["close_open_diff"] = (df["close"] - df["open"]) / df["open"]

    df["ma_3"] = df.groupby("symbol")["close"].transform(
        lambda x: x.rolling(window=3).mean()
    )

    df["ma_5"] = df.groupby("symbol")["close"].transform(
        lambda x: x.rolling(window=5).mean()
    )

    df["volume_ma_5"] = df.groupby("symbol")["volume"].transform(
        lambda x: x.rolling(window=5).mean()
    )

    df["price_vs_ma_5"] = (df["close"] - df["ma_5"]) / df["ma_5"]
    df["volume_vs_ma_5"] = (df["volume"] - df["volume_ma_5"]) / df["volume_ma_5"]

    df["future_close"] = df.groupby("symbol")["close"].shift(-1)
    df["future_return"] = (df["future_close"] - df["close"]) / df["close"]

    def create_label(future_return):
        if future_return > 0.01:
            return "BUY"
        elif future_return < -0.01:
            return "SELL"
        else:
            return "HOLD"

    df["target"] = df["future_return"].apply(create_label)

    feature_columns = [
        "daily_return",
        "price_range",
        "close_open_diff",
        "price_vs_ma_5",
        "volume_vs_ma_5",
    ]

    df = df.dropna(subset=feature_columns + ["target"])

    x = df[feature_columns]
    y = df["target"]

    return x, y, feature_columns


def train_model():
    """
    Train ML signal model and save it.
    """

    os.makedirs(MODEL_DIR, exist_ok=True)

    df = load_all_stock_data()
    x, y, feature_columns = prepare_dataset(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
    )

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("Model training completed")
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    model_package = {
        "model": model,
        "feature_columns": feature_columns,
    }

    joblib.dump(model_package, MODEL_PATH)

    print(f"Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()