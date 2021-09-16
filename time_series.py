from pathlib import Path

import pandas as pd

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/iris-hep/analysis-community-summary/gh-pages/summary_time_series.csv"
    update_df = pd.read_csv(url)
    current_df = pd.read_csv(Path().cwd().joinpath("summary.csv"))

    if current_df.date.isin(update_df.date)[0]:
        # Overwrite dataframe with current values
        selection = update_df["date"] == current_df["date"][0]
        update_df[selection] = current_df
    else:
        # Append current values
        update_df = pd.concat([update_df, current_df])

    update_df.to_csv("summary-time-series.csv", index=False)
