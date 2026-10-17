"""Reference solutions for drills/d1_spark_to_pandas.py. Open only after you have a PASS."""

import pandas as pd


def ex1_filter(runs):
    mask = (runs["status"] == "FAILED") & (runs["duration_min"] > 30)
    return runs.loc[mask, ["run_id", "job_name", "duration_min"]].sort_values("run_id")


def ex2_group_agg(runs):
    return (
        runs.assign(is_failed=runs["status"].eq("FAILED").astype(int))
        .groupby("job_name", as_index=False)
        .agg(runs=("run_id", "count"), failures=("is_failed", "sum"), avg_duration=("duration_min", "mean"))
        .round({"avg_duration": 1})
        .sort_values("job_name")
    )


def ex3_join(runs, clusters):
    return (
        runs.merge(clusters, on="cluster_id", how="left")
        .groupby("team", dropna=False, as_index=False)
        .agg(total_cost=("cost_usd", "sum"))
        .round({"total_cost": 2})
        .sort_values("total_cost", ascending=False)
    )


def ex4_window(runs):
    df = runs.sort_values(["job_name", "run_date"]).copy()
    df["prev_duration"] = df.groupby("job_name")["duration_min"].shift(1)
    df["duration_change"] = df["duration_min"] - df["prev_duration"]
    latest = df[df.groupby("job_name").cumcount(ascending=False) == 0]
    return latest[["job_name", "run_date", "status", "duration_min", "duration_change"]].sort_values("job_name")


def ex5_pivot(runs):
    out = pd.crosstab(runs["run_date"], runs["status"])[["SUCCEEDED", "FAILED"]].reset_index()
    out.columns.name = None
    return out
