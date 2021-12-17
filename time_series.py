import argparse

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update the time series CSV.")
    parser.add_argument(
        "in_csv",
        metavar="IN_CSV",
        type=str,
        help="Path of input CSV",
    )
    parser.add_argument(
        "--join-csv",
        dest="join_csv",
        type=str,
        default="summary.csv",
        help="Path of CSV to join or update IN_CSV",
    )
    parser.add_argument(
        "--out-csv",
        dest="out_csv",
        type=str,
        default="summary-time-series.csv",
        help="Path of output CSV",
    )
    args = parser.parse_args()

    update_df = pd.read_csv(args.in_csv)
    current_df = pd.read_csv(args.join_csv)

    if current_df.date.isin(update_df.date)[0]:
        # Overwrite dataframe with current values
        selection = update_df["date"] == current_df["date"][0]
        update_df.loc[selection, update_df.keys()] = current_df[update_df.keys()].values
    else:
        # Append current values
        update_df = pd.concat([update_df, current_df])

    update_df.to_csv(args.out_csv, index=False)
