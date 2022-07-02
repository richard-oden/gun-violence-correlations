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
    fig = figure(plot_width=1400, x_range=list(df[ColumnName.COUNTRY.value].unique()))
    fig.circle(x=ColumnName.COUNTRY.value, y=ColumnName.DEATH_RATE.value,
         source=column_data_source,
         size=10, color='green')
    fig.title.text = 'Firearm-Related Death Rate per 100,000 Citizens by Country'
    fig.xaxis.axis_label = ColumnName.COUNTRY.value
    fig.yaxis.axis_label = ColumnName.DEATH_RATE.value
    fig.xaxis.major_label_orientation = 'vertical'

    hover_tool = HoverTool()
    hover_tool.tooltips = [
        (ColumnName.OVERALL_REGULATION.value, f'@{{{ColumnName.OVERALL_REGULATION.value}}}')
    ]
    fig.add_tools(hover_tool)

    show(fig)