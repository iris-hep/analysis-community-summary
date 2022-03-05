from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def project_timeseries(df, value, **kwargs):
    if value not in df.keys():
        print(
            f"WARNING: {value} is not a column of the DataFrame. Valid columns are: {', '.join(time_series_df.keys())}"
        )
        return 1

    scale_factor = 2.5
    fig, (ax, legend_ax) = plt.subplots(
        ncols=2,
        figsize=(6 * scale_factor, 4 * scale_factor),
        gridspec_kw={"width_ratios": [4, 1]},
    )

    time_fmt = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(time_fmt)

    projects = time_series_df.sort_values(value, ascending=False)[
        "repositories"
    ].unique()
    if exclude_list := kwargs.pop("exclude", None):
        for project in exclude_list:
            projects = np.delete(projects, np.where(projects == project))

    plot_style = kwargs.pop("plot_style", "line")
    for idx, project in enumerate(projects):
        selection = df["repositories"] == project
        plot_kwargs = {"color": None if idx < 15 else "black"}

        if plot_style == "scatter":
            ax.scatter(
                df[selection]["date"],
                df[selection][value],
                label=project,
                **plot_kwargs,
            )
        else:
            plot_kwargs["linewidth"] = kwargs.get("linewidth", 3)
            ax.plot(
                df[selection]["date"],
                df[selection][value],
                label=project,
                **plot_kwargs,
            )

    handles, labels = ax.get_legend_handles_labels()
    legend_ax.legend(handles, labels, borderaxespad=0)
    legend_ax.axis("off")

    xlabel = kwargs.pop("xlabel", "Date")
    ax.set_xlabel(xlabel, size=14)
    ylabel = kwargs.pop("ylabel", f"Number of {value}")
    ax.set_ylabel(ylabel, size=14)

    fig.tight_layout()

    # Ensure img directory exists
    Path.cwd().joinpath("img").mkdir(parents=True, exist_ok=True)

    file_types = ["png", "pdf", "svg"]
    for extension in file_types:
        fig.savefig(f"img/time_series_{value}.{extension}", facecolor="white")


def write_markdown_section(df, plots):

    dates = df["date"]

    with open("time_series.md", "w") as write_file:
        file_str = "\n## Time Series Plots\n"
        file_str += f"\nCovering dates from **{dates.min()}** to **{dates.max()}**\n"

        base_url = "https://raw.githubusercontent.com/iris-hep/analysis-community-summary/gh-pages"
        for plot in plots:
            if plot not in df.keys():
                print(
                    f"WARNING: {plot} is not a column of the DataFrame. Valid columns are: {', '.join(time_series_df.keys())}"
                )
            else:
                file_str += f"\n### {plot.capitalize()}\n\n"
                file_str += f"![{plot}]({base_url}/img/time_series_{plot}.svg)\n"

        file_str += "\n"

        write_file.write(file_str)


if __name__ == "__main__":
    time_series_df = pd.read_csv("summary-time-series.csv", parse_dates=True)

    exclude_list = [
        "All IRIS-HEP Analysis Systems",
        "root-project/root",
        "alexander-held/cabinetry",
    ]

    plots = ["stars", "watchers", "contributors", "forks", "tags", "releases"]
    for plot in plots:
        project_timeseries(time_series_df, plot, exclude=exclude_list)

    write_markdown_section(time_series_df, plots)
