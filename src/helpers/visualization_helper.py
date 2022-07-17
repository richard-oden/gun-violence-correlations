import os
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, curdoc
from bokeh.models import ColumnDataSource, CustomJS, Select
from bokeh.models.tools import HoverTool
from enums.ColumnName import REGULATION_COLUMN_NAMES, ColumnName, TEXT_COLUMN_NAMES


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


def create_plot(df: pd.DataFrame, x_column_name: str, y_column_name: str) -> Figure:
    '''
    Creates bokeh `Figure` object using the supplied `DataFrame`.

    Parameters
    ---
    `df` : `DataFrame` object
    `x_column_name` : `str` representing the column to be plotted on the x-axis
    `y_column_name` : `str` representing the column to be plotted on the y-axis

    Returns
    ---
    a `Figure` object representing the `DataFrame`.
    '''

    # Drop countries where x-axis or y-axis data could not be found.
    relevant_df = df.dropna(subset=[x_column_name, y_column_name]).drop(df[(df[x_column_name] == -1) | (df[y_column_name] == -1)].index)

    # Fill cells where where data could not be found with human-friendly string for tooltips.
    relevant_df = relevant_df.fillna('No data found').replace([-1], 'No data found')

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

    return fig
    

def initialize_bokeh(df: pd.DataFrame):
    selectable_columns = [column_name.value for column_name in [
        ColumnName.DEATH_RATE, 
        ColumnName.OVERALL_REGULATION,
        *REGULATION_COLUMN_NAMES, 
        ColumnName.CIVILIAN_FIREARMS, 
        ColumnName.MILITARY_FIREARMS, 
        ColumnName.POLICE_FIREARMS]]

    x_select = Select(title='X-Axis Statistic', value=ColumnName.OVERALL_REGULATION.value, options=selectable_columns)
    y_select = Select(title='Y-Axis Statistic', value=ColumnName.DEATH_RATE.value, options=selectable_columns)

    controls = column(x_select, y_select, width=400)
    layout = row(controls, create_plot(df, x_select.value, y_select.value))

    #on_change callback functions must have the signature func(attr, old, new).
    def update(attr, old, new):
        layout.children[1] = create_plot(df, x_select.value, y_select.value)

    [select.on_change('value', update) for select in [x_select, y_select]]

    curdoc().add_root(layout)
    curdoc().title = "Gun Violence Correlations"