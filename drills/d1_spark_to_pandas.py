"""
Drill 1: Spark to pandas
========================
Rewrite 5 everyday Spark transformations in pandas.

How to run (from the repo folder, in PowerShell):
    uv run python drills/d1_spark_to_pandas.py

Each exercise shows the PySpark code you already know. Replace the
`raise NotImplementedError` line with pandas code that returns the same table.
Run the script after each one. Done when all 5 print PASS.

Rules:
- Return a pandas DataFrame with exactly the columns and row order shown.
- Don't modify `runs`, `clusters` or the checker at the bottom.
- Stuck for more than 10 minutes? Read the HINT, then the pandas docs for
  that one function. Solutions are in solutions/d1_spark_to_pandas.py:
  open them only after you have a PASS, to compare approaches.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Data: 12 Databricks job runs on 4 clusters. Cluster c4 has no owner record.
# ---------------------------------------------------------------------------
runs = pd.DataFrame(
    [
        (1, "daily_sales_etl", "c1", "2026-10-01", "SUCCEEDED", 22, 4.40),
        (2, "daily_sales_etl", "c1", "2026-10-02", "FAILED", 41, 8.20),
        (3, "daily_sales_etl", "c1", "2026-10-03", "SUCCEEDED", 25, 5.00),
        (4, "customer_360", "c2", "2026-10-01", "SUCCEEDED", 55, 16.50),
        (5, "customer_360", "c2", "2026-10-02", "SUCCEEDED", 61, 18.30),
        (6, "customer_360", "c2", "2026-10-03", "FAILED", 34, 10.20),
        (7, "churn_training", "c3", "2026-10-01", "FAILED", 18, 9.00),
        (8, "churn_training", "c3", "2026-10-02", "SUCCEEDED", 47, 23.50),
        (9, "churn_training", "c3", "2026-10-03", "SUCCEEDED", 44, 22.00),
        (10, "log_ingest", "c4", "2026-10-01", "SUCCEEDED", 12, 1.20),
        (11, "log_ingest", "c4", "2026-10-02", "FAILED", 36, 3.60),
        (12, "log_ingest", "c4", "2026-10-03", "SUCCEEDED", 11, 1.10),
    ],
    columns=["run_id", "job_name", "cluster_id", "run_date", "status", "duration_min", "cost_usd"],
)
runs["run_date"] = pd.to_datetime(runs["run_date"])

clusters = pd.DataFrame(
    [("c1", "finance", "m5.xlarge"), ("c2", "marketing", "m5.2xlarge"), ("c3", "data-science", "g5.xlarge")],
    columns=["cluster_id", "team", "node_type"],
)


# ---------------------------------------------------------------------------
# Exercise 1: filter + select + orderBy
# ---------------------------------------------------------------------------
# runs.filter((F.col("status") == "FAILED") & (F.col("duration_min") > 30)) \
#     .select("run_id", "job_name", "duration_min") \
#     .orderBy("run_id")
#
# HINT: boolean masks with & (wrap each condition in brackets), then df[[cols]].
def ex1_filter(runs: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Exercise 2: groupBy + agg
# ---------------------------------------------------------------------------
# runs.groupBy("job_name").agg(
#         F.count("*").alias("runs"),
#         F.sum(F.when(F.col("status") == "FAILED", 1).otherwise(0)).alias("failures"),
#         F.round(F.avg("duration_min"), 1).alias("avg_duration"),
#     ).orderBy("job_name")
#
# HINT: groupby(...).agg(name=(column, function)) "named aggregation";
#       a helper column like is_failed = (status == "FAILED") makes the sum easy.
def ex2_group_agg(runs: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Exercise 3: left join + groupBy (watch the cluster with no team!)
# ---------------------------------------------------------------------------
# runs.join(clusters, "cluster_id", "left") \
#     .groupBy("team").agg(F.round(F.sum("cost_usd"), 2).alias("total_cost")) \
#     .orderBy(F.desc("total_cost"))
#
# Spark keeps the null team as its own group. pandas drops it by default.
# HINT: merge(..., how="left"), groupby(..., dropna=False), sort_values(ascending=False).
def ex3_join(runs: pd.DataFrame, clusters: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Exercise 4: window functions (lag + row_number) - latest run per job
# ---------------------------------------------------------------------------
# w_asc  = Window.partitionBy("job_name").orderBy("run_date")
# w_desc = Window.partitionBy("job_name").orderBy(F.desc("run_date"))
# runs.withColumn("prev_duration", F.lag("duration_min").over(w_asc)) \
#     .withColumn("duration_change", F.col("duration_min") - F.col("prev_duration")) \
#     .withColumn("rn", F.row_number().over(w_desc)) \
#     .filter("rn = 1") \
#     .select("job_name", "run_date", "status", "duration_min", "duration_change") \
#     .orderBy("job_name")
#
# HINT: sort first, then groupby(...)["duration_min"].shift(1) is lag;
#       groupby(...).cumcount(ascending=False) == 0 picks the latest row.
def ex4_window(runs: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Exercise 5: pivot
# ---------------------------------------------------------------------------
# runs.groupBy("run_date").pivot("status", ["SUCCEEDED", "FAILED"]).count() \
#     .fillna(0).orderBy("run_date")
#
# HINT: pd.crosstab or pivot_table(aggfunc="size", fill_value=0);
#       reset_index() and drop the columns' name so it's a flat table.
def ex5_pivot(runs: pd.DataFrame) -> pd.DataFrame:
    raise NotImplementedError


# ===========================================================================
# Checker: expected outputs, produced by running the Spark code above.
# Do not edit below this line.
# ===========================================================================
EXPECTED = {
    "ex1_filter": pd.DataFrame(
        {"run_id": [2, 6, 11], "job_name": ["daily_sales_etl", "customer_360", "log_ingest"],
         "duration_min": [41, 34, 36]}),
    "ex2_group_agg": pd.DataFrame(
        {"job_name": ["churn_training", "customer_360", "daily_sales_etl", "log_ingest"],
         "runs": [3, 3, 3, 3], "failures": [1, 1, 1, 1],
         "avg_duration": [36.3, 50.0, 29.3, 19.7]}),
    "ex3_join": pd.DataFrame(
        {"team": ["data-science", "marketing", "finance", None],
         "total_cost": [54.5, 45.0, 17.6, 5.9]}),
    "ex4_window": pd.DataFrame(
        {"job_name": ["churn_training", "customer_360", "daily_sales_etl", "log_ingest"],
         "run_date": pd.to_datetime(["2026-10-03"] * 4),
         "status": ["SUCCEEDED", "FAILED", "SUCCEEDED", "SUCCEEDED"],
         "duration_min": [44, 34, 25, 11], "duration_change": [-3.0, -27.0, -16.0, -25.0]}),
    "ex5_pivot": pd.DataFrame(
        {"run_date": pd.to_datetime(["2026-10-01", "2026-10-02", "2026-10-03"]),
         "SUCCEEDED": [3, 2, 3], "FAILED": [1, 2, 1]}),
}


def _check(name, fn, *args):
    try:
        got = fn(*[a.copy() for a in args])
    except NotImplementedError:
        print(f"TODO  {name}")
        return False
    except Exception as exc:  # noqa: BLE001 - show the error, keep checking the rest
        print(f"ERROR {name}: {type(exc).__name__}: {exc}")
        return False
    want = EXPECTED[name]
    try:
        assert isinstance(got, pd.DataFrame), f"expected a DataFrame, got {type(got).__name__}"
        assert list(got.columns) == list(want.columns), f"columns {list(got.columns)} != {list(want.columns)}"
        got = got.reset_index(drop=True)
        got.columns.name = None
        if name == "ex3_join":
            got["team"] = got["team"].astype(object).fillna("<null>")
            want = want.assign(team=want["team"].astype(object).fillna("<null>"))
            got["total_cost"] = got["total_cost"].round(2)
        pd.testing.assert_frame_equal(got, want, check_dtype=False, check_exact=False, atol=0.05)
    except AssertionError as exc:
        print(f"FAIL  {name}\n      {str(exc).strip().splitlines()[0]}\n      got:\n{got}\n      want:\n{want}")
        return False
    print(f"PASS  {name}")
    return True


if __name__ == "__main__":
    results = [
        _check("ex1_filter", ex1_filter, runs),
        _check("ex2_group_agg", ex2_group_agg, runs),
        _check("ex3_join", ex3_join, runs, clusters),
        _check("ex4_window", ex4_window, runs),
        _check("ex5_pivot", ex5_pivot, runs),
    ]
    print(f"\n{sum(results)}/5 passing")
    if all(results):
        print("Drill done. Commit it:  git add . ; git commit -m \"Drill 1: Spark to pandas\" ; git push")
