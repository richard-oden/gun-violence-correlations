import os
from bokeh.plotting import figure, output_file, show

if not os.path.exists('output'):
    os.makedirs('output')

output_file(os.path.join('output', 'visualization.html'))

x = [1, 3, 5, 7]
y = [2, 4, 6, 8]

p = figure()

p.circle(x, y, size=10, color='red', legend='circle')
p.line(x, y, color='blue', legend='line')
p.triangle(y, x, color='gold', size=10, legend='triangle')

p.legend.click_policy='hide'

show(p)