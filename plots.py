import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def project_timeseries(df, value, **kwargs):
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
    fig.savefig(f"time_series_{value}.png", facecolor="white")


def write_markdown_section(df):

    dates = df["date"]

    with open("time_series.md", "w") as write_file:
        file_str = "\n## Time Series Plots\n"
        file_str = f"\nCovering dates from **{dates.min()}** to **{dates.max()}**\n"

        plots = ["stars", "forks", "watchers"]
        base_url = "https://raw.githubusercontent.com/iris-hep/analysis-community-summary/gh-pages"
        for plot in plots:
            file_str += f"\n### {plot.capitalize()}\n\n"
            file_str += f"![{plot}]({base_url}/img/time_series_{plot}.png)\n"

        file_str += "\n"

        write_file.write(file_str)


if __name__ == "__main__":
    time_series_df = pd.read_csv("summary-time-series.csv", parse_dates=True)

    exclude_list = [
        "All IRIS-HEP Analysis Systems",
        "root-project/root",
        "alexander-held/cabinetry",
    ]
    project_timeseries(time_series_df, "stars", exclude=exclude_list)
    project_timeseries(time_series_df, "forks", exclude=exclude_list)
    project_timeseries(time_series_df, "watchers", exclude=exclude_list)

    write_markdown_section(time_series_df)