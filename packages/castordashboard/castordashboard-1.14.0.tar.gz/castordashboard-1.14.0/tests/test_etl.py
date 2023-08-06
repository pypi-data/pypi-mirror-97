import os

from types import SimpleNamespace

from castordashboard.etl import ScriptRunner
from castordashboard.etl import DummyScript
from castordashboard.etl import RetrieveStudyListScript
from castordashboard.etl import RetrieveProcedureCountsAndComplicationsPerQuarterScript


def find_latest_log(prefix):
    log_file = None
    max_x = 0
    for f in os.listdir('.'):
        if f.startswith(prefix):
            x = int(f.split('_')[2][:-4])
            if x > max_x:
                max_x = x
                log_file = f
    print('Latest log file: {}'.format(log_file))
    return log_file


# def test_periodic_execution():
#
#     runner = ScriptRunner(interval=0, time_period=0)
#     runner.script = DummyScript(runner, {})
#     runner.execute()
#     runner.logger.close()
#
#     log_file = find_latest_log('log_etl')
#     with open(log_file, 'r') as f:
#         assert len(f.readlines()) == 6
#
#     runner = ScriptRunner(interval=1, time_period=5)
#     runner.script = DummyScript(runner, {})
#     runner.execute()
#     runner.logger.close()
#
#     log_file = find_latest_log('log_etl')
#     with open(log_file, 'r') as f:
#         assert len(f.readlines()) == 18
#
#
# def test_retrieve_study_list_every_5_secs():
#
#     runner = ScriptRunner(interval=5, time_period=10)
#     runner.script = RetrieveStudyListScript(runner, {})
#     runner.execute()
#     runner.logger.close()
#
#     log_file = find_latest_log('log_etl')
#
#     count = 0
#     with open(log_file, 'r') as f:
#         for line in f.readlines():
#             if 'study_id' in line.strip():
#                 count += 1
#     assert count > 0
#
#
# def test_retrieve_dashboard_data_liver():
#
#     params = {
#         'study_name': 'ESPRESSO_v2.0_DHBA',
#         'field_name': 'dhba_datok',
#         'output_dir': '/tmp/castordashboard',
#         'output_json': 'histogram_dhba.json',
#         'use_cache': False,
#         'verbose': True,
#     }
#
#     runner = ScriptRunner()
#     runner.script = RetrieveProcedureCountsPerQuarterScript(runner, params)
#     runner.execute()
#     runner.logger.close()
#
#     params = SimpleNamespace(**params)
#     assert os.path.isfile(os.path.join(params.output_dir, params.output_json))
#
#
# def test_retrieve_dashboard_data_pancreas():
#
#     params = {
#         'study_name': 'ESPRESSO_v2.0_DPCA',
#         'field_name': 'dpca_datok',
#         'output_dir': '/tmp/castordashboard',
#         'output_json': 'histogram_dpca.json',
#         'use_cache': False,
#         'verbose': True,
#     }
#
#     runner = ScriptRunner()
#     runner.script = RetrieveProcedureCountsPerQuarterScript(runner, params)
#     runner.execute()
#     runner.logger.close()
#
#     params = SimpleNamespace(**params)
#     assert os.path.isfile(os.path.join(params.output_dir, params.output_json))
#
#
def find_latest_dir(root_dir):
    d = None
    max_x = 0
    for f in os.listdir(root_dir):
        try:
            x = int(f)
            if x > max_x:
                max_x = x
                d = f
        except ValueError:
            pass
    print('Latest directory: {}'.format(d))
    return os.path.join(root_dir, d)


def test_main():

    import json
    import sys
    from castordashboard.etl import script_runner

    with open('params.json', 'w') as f:
        json.dump({
            'script': 'RetrieveProcedureCountsAndComplicationsPerQuarterScript',
            'study_name': 'ESPRESSO_v2.0_DPCA',
            'surgery_date_field_name': 'dpca_datok',
            'complications_field_name': 'dpca_compl',
            'output_dir': '/tmp/castordashboard',
            'output_json': 'histogram_dpca.json',
            'use_cache': True,
            'verbose': True,
        }, f)

    sys.argv = ['script_runner.py']
    script_runner.main()

    d = find_latest_dir('/tmp/castordashboard')
    with open(os.path.join(d, 'histogram_dpca.json'), 'r') as f:
        print(json.dumps(json.load(f), indent=4))
