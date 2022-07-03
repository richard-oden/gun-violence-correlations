import os
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from enums.ColumnName import ColumnName, REGULATION_COLUMN_NAMES


def initialize_output() -> None:
    '''
    Defines the default output file for bokeh as `output/visualization.html`.
    '''
    if not os.path.exists('output'):
        os.makedirs('output')

    output_file(os.path.join('output', 'visualization.html'))

def create_regression_line(df: pd.DataFrame) -> list:
    '''
    Given the supplied `DataFrame`, calculates a regression line indicating the
    overall trend.

    Parameters
    ---
    `df` : `DataFrame` object

    Returns
    ---
    a `list` of y coordinate values for the regression line.
    '''
    par = np.polyfit(df[ColumnName.OVERALL_REGULATION.value], df[ColumnName.DEATH_RATE.value], 1, full=True)
    slope=par[0][0]
    intercept=par[0][1]
    return [slope*x + intercept for x in df[ColumnName.OVERALL_REGULATION.value]]

def create_plot(df: pd.DataFrame) -> None:
    '''
    Creates bokeh `Figure` object using the supplied `DataFrame` and displays it.

    Parameters
    ---
    `df` : `DataFrame` object
    '''
    column_data_source = ColumnDataSource(df)
    fig = figure(plot_width=1000)
    fig.circle(x=ColumnName.OVERALL_REGULATION.value, y=ColumnName.DEATH_RATE.value,
        source=column_data_source, size=8, color='black')
    fig.line(x=df[ColumnName.OVERALL_REGULATION.value], y=create_regression_line(df),
        color='red')

    fig.title.text = 'Firearm-Related Death Rate vs Overall Firearm Regulation'
    fig.xaxis.axis_label = ColumnName.OVERALL_REGULATION.value
    fig.yaxis.axis_label = ColumnName.DEATH_RATE.value

    hover_tool = HoverTool()
    hover_tool.tooltips = [(column_name.value, f'@{{{column_name.value}}}') for column_name in ColumnName]
    fig.add_tools(hover_tool)

    show(fig)