import helpers.data_helper as dh
import helpers.visualization_helper as vh

df = dh.get_cleaned_data()
vh.initialize_output()
vh.create_plot(df)