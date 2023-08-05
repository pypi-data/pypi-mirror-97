import os
import json
import sys

from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure


NR_YEARS = 5

NR_QUARTERS = 4 * NR_YEARS


def load_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


def find_latest_finished_dir(root_dir):
    ld = None
    max_x = 0
    for d in os.listdir(root_dir):
        try:
            x = int(d)
            d = os.path.join(root_dir, d)
            if os.path.isfile(os.path.join(d, 'finished.txt')) and x > max_x:
                ld = d
                max_x = x
        except ValueError:
            pass
    print('Latest (finished) directory: {}'.format(ld))
    return ld


latest_dir = find_latest_finished_dir('/tmp/castordashboard')

histogram = load_json(os.path.join(latest_dir, 'histogram_dpca.json'))

quarters = histogram['quarters']
comp_y = histogram['comp_y']
comp_n = histogram['comp_n']

colors = ['#718dbf', '#e84d60']

source = ColumnDataSource(data={
    'quarters': quarters,
    'comp_y': comp_y,
    'comp_n': comp_n,
})

p = figure(
    x_range=quarters,
    plot_width=1000, plot_height=500,
    title='Pancreatic procedure counts and complications per quarter',
)

p.vbar_stack(
    stackers=['comp_y', 'comp_n'],
    x='quarters',
    width=0.9,
    color=colors,
    source=source,
    legend_label=['Complications YES', 'Complications NO'])

p.xaxis.major_label_orientation = 'vertical'
p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"


def main():
    curdoc().add_root(column(p))


main()
