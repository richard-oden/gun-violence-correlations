import os
import numpy as np
import pandas as pd
from bokeh.io import show
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, CustomJS, Select
from bokeh.models.tools import HoverTool
from enums.ColumnName import ColumnName, TEXT_COLUMN_NAMES


def initialize_output() -> None:
    '''
    Defines the default output file for bokeh as `output/visualization.html`.
    '''
    if not os.path.exists('output'):
        os.makedirs('output')

    output_file(os.path.join('output', 'visualization.html'))

def create_regression_line(df: pd.DataFrame, x_column_name: str, y_column_name: str) -> list:
    '''
    Given the supplied `DataFrame`, calculates a regression line indicating the
    overall trend.

    Parameters
    ---
    `df` : `DataFrame` object
    `x_column_name` : `str` representing the column to be plotted on the x-axis
    `y_column_name` : `str` representing the column to be plotted on the y-axis

    Returns
    ---
    a `list` of y coordinate values for the regression line.
    '''
    par = np.polyfit(df[x_column_name], df[y_column_name], 1, full=True)
    slope=par[0][0]
    intercept=par[0][1]

    return [slope*x + intercept for x in df[x_column_name]]

def create_plot(df: pd.DataFrame, x_column_name: str, y_column_name: str) -> None:
    '''
    Creates bokeh `Figure` object using the supplied `DataFrame` and displays it.

    Parameters
    ---
    `df` : `DataFrame` object
    `x_column_name` : `str` representing the column to be plotted on the x-axis
    `y_column_name` : `str` representing the column to be plotted on the y-axis
    '''
    relevant_df = df.dropna(subset=[x_column_name, y_column_name]).drop(df[(df[x_column_name] == -1) | (df[y_column_name] == -1)].index)

    column_data_source = ColumnDataSource(relevant_df)
    fig = figure(plot_width=1000)
    fig.circle(x=x_column_name, y=y_column_name,
        source=column_data_source, size=8, color='black', name='countries')
    fig.line(x=relevant_df[x_column_name], y=create_regression_line(relevant_df, x_column_name, y_column_name),
        color='red')

    fig.title.text = f'{x_column_name} vs {y_column_name}'
    fig.xaxis.axis_label = x_column_name
    fig.yaxis.axis_label = y_column_name

    tooltip_columns = [ColumnName.COUNTRY, *TEXT_COLUMN_NAMES, ColumnName.CIVILIAN_FIREARMS, ColumnName.MILITARY_FIREARMS, ColumnName.POLICE_FIREARMS]

    hover_tool = HoverTool(tooltips=[(column_name.value, f'@{{{column_name.value}}}') for column_name in tooltip_columns], names=['countries'])
    fig.add_tools(hover_tool)

    show(fig)