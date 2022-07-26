import helpers.data_helper as dh
import helpers.log_helper as lh
import helpers.visualization_helper as vh
from enums.ColumnName import ColumnName

lh.configure_logging()
lh.log_info('Starting data import and cleaning.')
df = dh.get_cleaned_data()
lh.log_info('Data import and cleaning completed.')
lh.log_info('Starting visualization.')
vh.initialize_bokeh(df)
lh.log_info('Visualization started.')