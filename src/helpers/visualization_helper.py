import os
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

def create_plot(df: pd.DataFrame):
    '''
    Creates bokeh `Figure` object using the supplied `DataFrame` and displays it. 
    '''
    column_data_source = ColumnDataSource(df)
    fig = figure(plot_width=1000)
    fig.circle(x=ColumnName.OVERALL_REGULATION.value, y=ColumnName.DEATH_RATE.value,
         source=column_data_source,
         size=5, color='red')
    fig.title.text = 'Firearm-Related Death Rate vs Overall Firearm Regulation'

    hover_tool = HoverTool()
    hover_tool.tooltips = [(column_name.value, f'@{{{column_name.value}}}') for column_name in ColumnName]
    fig.add_tools(hover_tool)

    show(fig)