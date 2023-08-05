import os
import json

from types import SimpleNamespace

from bokeh.server.server import Server
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


def load_params(file_path='params.json'):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None


params = load_params()
if params is None:
    params = {
        'script': 'RetrieveProcedureCountsAndComplicationsPerQuarterScript',
        'study_name': 'ESPRESSO_v2.0_DPCA',
        'surgery_date_field_name': 'dpca_datok',
        'complications_field_name': 'dpca_compl',
        'output_dir': '/tmp/castordashboard',
        'output_json': 'histogram_dpca.json',
        'use_cache': True,
        'verbose': True,
        'port_nr': 5006
    }
    print('Could not find params.json. Using defaults...')
    print(json.dumps(params, indent=4))
params = SimpleNamespace(**params)


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


def make_document(doc):

    latest_dir = find_latest_finished_dir(params.output_dir)

    histogram = load_json(os.path.join(latest_dir, params.output_json))

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

    doc.title = 'Dashboard HPB'
    doc.add_root(column(p))


def main():
    p = params.port_nr
    print('Running server at port {}...'.format(p))
    server = Server({'/': make_document}, port=p)
    server.start()
    server.io_loop.add_callback(server.show, '/')
    server.io_loop.start()


if __name__ == '__main__':
    main()
