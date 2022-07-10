import helpers.data_helper as dh
import helpers.visualization_helper as vh
from enums.ColumnName import ColumnName

df = dh.get_cleaned_data()
vh.initialize_bokeh(df)