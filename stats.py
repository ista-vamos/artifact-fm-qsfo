import polars as pl
import glob
import sys
import os


def fraction_to_float(col):
    parts = col.str.split("/")
    return (
        parts.arr.first().cast(pl.Float64) / parts.arr.last().cast(pl.Float64)
    ).alias(col.meta.output_name())


# fraction_cols = ["intv_start", "intv_end"]


def process_csvs(files):
    if not files:
        return None

    # Read and concatenate all CSVs
    dfs = []
    for f in files:
        try:
            cur = pl.read_csv(
                f,
                has_header=True,
                separator=",",
                ignore_errors=True,
                dtypes=[
                    pl.Utf8,  # intv_start
                    pl.Utf8,  # intv_end
                    pl.Float64,  # t_r
                    pl.Float64,  # t_m
                ],
            ).with_columns(pl.lit(os.path.basename(f)).alias("filename"))
        except pl.exceptions.NoDataError:
            continue
        dfs.append(cur)

    df = pl.concat(dfs)

    # Compute mean of (t_r + t_m)
    result = df.select((pl.col("t_r") + pl.col("t_m")).mean().alias("mean_sum"))

    return result[0, 0]


if __name__ == "__main__":
    if len(sys.argv) != 2 or (not os.path.isdir(sys.argv[1])):
        print("Usage: stats.py <results-dir>", file=sys.stderr)
        exit(1)

    results_dir = os.path.abspath(sys.argv[1])
    print(f"... looking for results in `{results_dir}`")
    for sd in os.listdir(results_dir):
        fullpath = f"{results_dir}/{sd}"
        if not os.path.isdir(fullpath) or (sd not in ("avoidance", "f16")):
            print(
                f"WARNING: skipping `{fullpath}` which I did not expect in results directory"
            )
            continue
        for pdir in os.listdir(fullpath):
            fullpath2 = f"{fullpath}/{pdir}"
            if not os.path.isdir(fullpath2) or not pdir.startswith("prp"):
                print(
                    f"WARNING: skipping `{fullpath2}` which I did not expect in results directory"
                )
                continue
            files = glob.glob(f"{fullpath2}/*.csv")
            if files:
                print(f"{sd: <12}{pdir: <6} {process_csvs(files): <8.4f}")
