import numpy as np
import pandas as pd
import helpers.log_helper as lh
from bokeh.layouts import column, row
from bokeh.plotting import curdoc, figure, Figure
from bokeh.models import ColumnDataSource, Select, Div
from bokeh.models.tools import HoverTool
from enums.ColumnName import REGULATION_COLUMN_NAMES, ColumnName, TEXT_COLUMN_NAMES


def initialize_bokeh(df: pd.DataFrame):
    selectable_columns = [column_name.value for column_name in [
        ColumnName.DEATH_RATE, 
        ColumnName.OVERALL_REGULATION,
        *REGULATION_COLUMN_NAMES, 
        ColumnName.CIVILIAN_FIREARMS, 
        ColumnName.MILITARY_FIREARMS, 
        ColumnName.POLICE_FIREARMS]]

    countries = df[ColumnName.COUNTRY.value].tolist()

    description = Div(text='''
        Created by Richard Oden for Code Louisville's May 2022 Data 2 class. Data sourced from 
        <a target="_blank" href="https://smallarmssurvey.org/">Small Arms Survey</a> and 
        <a target="_blank" href="https://en.wikipedia.org/wiki/Overview_of_gun_laws_by_nation">Wikipedia</a>. 
        View the source code on <a target="_blank" href="https://github.com/richard-oden/gun-violence-correlations">Github</a>.''')
    x_select = Select(title='X-Axis Statistic', value=ColumnName.OVERALL_REGULATION.value, options=selectable_columns)
    y_select = Select(title='Y-Axis Statistic', value=ColumnName.DEATH_RATE.value, options=selectable_columns)
    highlighted_country_select = Select(title='Highlighted Country', value='United States', options=countries)

    controls = column(x_select, y_select, highlighted_country_select, description, width=400)
    layout = row(controls, create_plot(df, x_select.value, y_select.value, highlighted_country_select.value))

    #on_change callback functions must have the signature func(attr, old, new).
    def update(attr, old, new):
        lh.log_info(f'Updating plot with the following values:\n\tX: {x_select.value}, Y: {y_select.value}, HIGHLIGHTED: {highlighted_country_select.value}')
        layout.children[1] = create_plot(df, x_select.value, y_select.value, highlighted_country_select.value)

    [select.on_change('value', update) for select in [x_select, y_select, highlighted_country_select]]

    curdoc().add_root(layout)
    curdoc().title = "Gun Violence Correlations"
    

def create_plot(df: pd.DataFrame, x_column_name: str, y_column_name: str, highlighted_country_name: str) -> Figure:
    '''
    Creates bokeh `Figure` object using the supplied `DataFrame`.

    Parameters
    ---
    `df` : `DataFrame` object
    `x_column_name` : `str` representing the column to be plotted on the x-axis
    `y_column_name` : `str` representing the column to be plotted on the y-axis
    `highlighted_country_name` : `str` name of the country to be highlighted in the plot

    Returns
    ---
    a `Figure` object representing the `DataFrame`.
    '''

    # Drop countries where x-axis or y-axis data could not be found.
    relevant_df = df.dropna(subset=[x_column_name, y_column_name]).drop(df[(df[x_column_name] == -1) | (df[y_column_name] == -1)].index)

    # Fill cells where where data could not be found with human-friendly string for tooltips.
    relevant_df = relevant_df.fillna('No data found').replace([-1], 'No data found')
    highlighted_country_df = relevant_df[relevant_df[ColumnName.COUNTRY.value] == highlighted_country_name]

    column_data_source = ColumnDataSource(relevant_df.drop(highlighted_country_df.index))
    highlighted_column_data_source = ColumnDataSource(highlighted_country_df)

    fig = figure(plot_width=1000)
    fig.circle(x=x_column_name, y=y_column_name,
        source=column_data_source, size=10, color="#2F2F2F", line_color='white', alpha=0.5, hover_alpha=1, hover_color='white', name='countries')
    fig.circle(x=x_column_name, y=y_column_name,
        source=highlighted_column_data_source, size=10, color="#ca5959", name='highlighted country')

    fig.line(x=relevant_df[x_column_name], y=create_regression_line(relevant_df, x_column_name, y_column_name),
        color='#ca5959')

    fig.title.text = f'{x_column_name} vs {y_column_name}'
    fig.xaxis.axis_label = x_column_name
    fig.yaxis.axis_label = y_column_name

    tooltip_columns = [ColumnName.COUNTRY, *TEXT_COLUMN_NAMES, ColumnName.CIVILIAN_FIREARMS, ColumnName.MILITARY_FIREARMS, ColumnName.POLICE_FIREARMS]

    hover_tool = HoverTool(tooltips=[(column_name.value, f'@{{{column_name.value}}}') for column_name in tooltip_columns], names=['countries', 'highlighted country'])
    fig.add_tools(hover_tool)

    return fig
    

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