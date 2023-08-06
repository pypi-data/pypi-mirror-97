"""Defines all functions within plot part of exergi package."""

from pandas import DataFrame
from plotly import express
import plotly.graph_objects as go


def lineplot(
    df_: DataFrame, x: str, y: list, title="No title", width=1200, height=500
):
    """Create a lineplot of columns in specified dataframe using plotly.

    Arguments:
        df_         - Dataframe with data to plot. All data must be in the
                      same DataFrame.
        x           - String with name of column for x-axis, can't be index
        y           - List of string with name of columns for y-axis.
        title       - Title for plot.
        width       - Width of plot in pixels.
        height      - Height of plot in pixels.


    Returns:
        - Plotly lineplot with legend.

    """
    # Define position of legend
    legend_dict = dict(
        orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0
    )

    # Create figure
    fig = express.line(df_, x=x, y=y, title=title, width=width, height=height)
    fig.update_layout(legend=legend_dict)
    fig.show()


def histogram(
    df_: DataFrame, x: list, title="No title", width=1000, height=500
):
    """Create a histogram of columns in specified dataframe using plotly.

    Arguments:
        df_         - Dataframe with data to plot. All data must be in the
                      same DataFrame.
        x           - List of string with name of columns.
        title       - Title for plot.
        width       - Width of plot in pixels.
        height      - Height of plot in pixels.

    Returns:
        - Plotly histogram
    """
    fig = go.Figure()

    for col in x:
        fig.add_trace(go.Histogram(x=df_[col], name=col))

    # Overlay both histograms
    fig.update_layout(
        barmode="overlay", title=title, width=width, height=height
    )

    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.6)
    fig.show()


def scatterplot(
    df_: DataFrame, x: str, y: list, width=1200, height=500, **kwargs
):
    """Create a scatter of columns in specified dataframe using plotly.

    Arguments:
        df_         - Dataframe with data to plot. All data must be in the
                      same DataFrame.
        x           - String with name of column for x-axis, can't be index
        y           - List of string with name of columns for y-axis.
        title       - Title for plot.
        width       - Width of plot in pixels.
        height      - Height of plot in pixels.

    Keyword Arguments:
        **kwargs    - Additional keyword arguments for plotly express

    Returns:
        - Plotly lineplot with legend.
    """
    # Define position of legend
    legend_dict = dict(
        orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0
    )

    # Create figure
    fig = express.scatter(df_, x=x, y=y, width=width, height=height, **kwargs)
    fig.update_layout(legend=legend_dict)
    fig.show()
