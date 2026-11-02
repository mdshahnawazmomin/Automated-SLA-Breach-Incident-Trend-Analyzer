import pandas as pd
from datetime import datetime

SLA_HOURS = 2  # breach if resolution > 2 hours


def load_data(path):
    df = pd.read_csv(path)
    return df


def calculate_metrics(df):
    df["created_time"] = pd.to_datetime(df["created_time"])
    df["resolved_time"] = pd.to_datetime(df["resolved_time"])

    df["resolution_hours"] = (
        df["resolved_time"] - df["created_time"]
    ).dt.total_seconds() / 3600

    resolved_df = df[df["status"] == "Resolved"].copy()

    total_incidents = len(resolved_df)
    breaches = len(resolved_df[resolved_df["resolution_hours"] > SLA_HOURS])

    breach_percent = (breaches / total_incidents) * 100 if total_incidents else 0
    mttr = resolved_df["resolution_hours"].mean()

    return {
        "total_incidents": total_incidents,
        "breaches": breaches,
        "breach_percent": round(breach_percent, 2),
        "mttr": round(mttr, 2) if mttr else 0,
        "dataframe": df,
    }
