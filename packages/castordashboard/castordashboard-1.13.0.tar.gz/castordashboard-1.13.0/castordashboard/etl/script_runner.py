import time
import json
import argparse
import importlib

from types import SimpleNamespace
from barbell2.utils import Logger, current_time_secs, elapsed_secs


class ScriptRunner:

    def __init__(self):
        self.script = None
        self.logger = Logger(prefix='log_etl')

    def execute(self):
        if self.script is None:
            self.logger.print('Nothing to execute')
            return
        self.logger.print('Starting script {}'.format(self.script.name))
        self.script.execute()
        self.logger.print('Script finished')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--params',
                        help='Full path to JSON parameter file (default: params.json)',
                        default='params.json')
    args = parser.parse_args()
    with open(args.params, 'r') as f:
        params = json.load(f)
    params = SimpleNamespace(**params)
    try:
        script_module = params.script_module
    except AttributeError:
        script_module = 'castordashboard.etl.scripts'
    script = getattr(importlib.import_module(script_module), params.script)
    runner = ScriptRunner()
    runner.script = script(runner, params)
    runner.execute()


if __name__ == '__main__':
    main()
