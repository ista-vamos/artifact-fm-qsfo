import polars as pl
import glob
import sys, os

# Get all CSV files (adjust the path/pattern as needed)
files = glob.glob(f"{sys.argv[1]}/*.csv")

def fraction_to_float(col):
    parts = col.str.split("/")
    return (
        (parts.arr.first().cast(pl.Float64) / parts.arr.last().cast(pl.Float64))
        .alias(col.meta.output_name())
    )

fraction_cols = ["intv_start", "intv_end"]



# Read and concatenate all CSVs
dfs = []
for f in files:
    print(f)
    cur = pl.read_csv(f, has_header=True, separator=",",
    dtypes=[
        pl.Utf8,  # intv_start
        pl.Utf8,  # intv_end
        pl.Float64,  # t_r
        pl.Float64   # t_m
    ]).with_columns(
        pl.lit(os.path.basename(f)).alias("filename")
    )
    dfs.append(cur)
    
df = pl.concat(dfs)

# Compute mean of (t_r + t_m)
result = df.select(
    (pl.col("t_r") + pl.col("t_m")).mean().alias("mean_sum")
)

print(result)

