import os
import json
import datetime

from types import SimpleNamespace
from barbell2.castorclient import CastorClient


class Script:

    def __init__(self, name, runner, params):
        self.name = name
        self.runner = runner
        self.params = params
        if isinstance(self.params, dict):
            self.params = SimpleNamespace(**params)

    def save_to_json(self, data):
        os.makedirs(self.params.output_dir, exist_ok=True)
        now = datetime.datetime.now()
        timestamp = '{}'.format(now.strftime('%Y%m%d%H%M%S'))
        os.makedirs(os.path.join(self.params.output_dir, timestamp), exist_ok=True)
        output_dir = os.path.join(self.params.output_dir, timestamp)
        with open(os.path.join(output_dir, self.params.output_json), 'w') as f:
            json.dump(data, f)
        os.system('touch {}'.format(os.path.join(output_dir, 'finished.txt')))

    def execute(self):
        raise NotImplementedError()


class DummyScript(Script):

    def __init__(self, runner, params):
        super(DummyScript, self).__init__(self.__class__, runner, params)

    def execute(self):
        self.runner.logger.print(json.dumps(vars(self.params), indent=4))


class RetrieveStudyListScript(Script):

    def __init__(self, runner, params):
        super(RetrieveStudyListScript, self).__init__(self.__class__, runner, params)

    def execute(self):
        client = CastorClient()
        study_list = client.get_studies()
        for study in study_list:
            self.runner.logger.print(study)


class RetrieveProcedureCountsAndComplicationsPerQuarterScript(Script):

    def __init__(self, runner, params):
        super(RetrieveProcedureCountsAndComplicationsPerQuarterScript, self).__init__(self.__class__, runner, params)

    @staticmethod
    def get_numerical_representation(date_str):
        items = date_str.split('-')
        return int('{}{}{}'.format(items[2], items[1], items[0]))

    def get_earliest_and_latest_date(self, date_list):
        min_date = 999999999
        min_date_str = ''
        max_date = 0
        max_date_str = ''
        for d in date_list:
            x = self.get_numerical_representation(d)
            if x < min_date:
                min_date = x
                min_date_str = d
            if x > max_date:
                max_date = x
                max_date_str = d
        return min_date_str, max_date_str

    @staticmethod
    def get_year(date_str):
        return int(date_str.split('-')[2])

    @staticmethod
    def get_month(date_str):
        return int(date_str.split('-')[1])

    def get_histogram(self, year_begin, year_end, surgery_dates, complications):
        histogram = {}
        for year in range(year_begin, year_end + 1):
            histogram[year] = {
                '1_2_3': {'comp_y': 0, 'comp_n': 0},
                '4_5_6': {'comp_y': 0, 'comp_n': 0},
                '7_8_9': {'comp_y': 0, 'comp_n': 0},
                '10_11_12': {'comp_y': 0, 'comp_n': 0},
            }
        for i in range(len(surgery_dates)):
            d = surgery_dates[i]
            c = complications[i]
            y = self.get_year(d)
            m = str(self.get_month(d))
            if y in histogram.keys():
                for q in histogram[y].keys():
                    q_items = q.split('_')
                    if m in q_items:
                        if c == 1:
                            histogram[y][q]['comp_y'] += 1
                        else:
                            histogram[y][q]['comp_n'] += 1
        # for d in surgery_dates:
        #     y = self.get_year(d)
        #     m = str(self.get_month(d))
        #     if y in histogram.keys():
        #         for q in histogram[y].keys():
        #             x = q.split('_')
        #             if m in x:
        #                 histogram[y][q] += 1
        return histogram

    @staticmethod
    def get_quarter(k):
        if k == '1_2_3':
            return 'q1'
        if k == '4_5_6':
            return 'q2'
        if k == '7_8_9':
            return 'q3'
        return 'q4'

    def flatten_histogram(self, histogram):
        histogram_new = {'quarters': [], 'comp_y': [], 'comp_n': []}
        for y in histogram.keys():
            for k in histogram[y].keys():
                q = self.get_quarter(k)
                q = '{}_{}'.format(y, q)
                histogram_new['quarters'].append(q)
                histogram_new['comp_y'].append(histogram[y][k]['comp_y'])
                histogram_new['comp_n'].append(histogram[y][k]['comp_n'])
        # for y in histogram.keys():
        #     for k in histogram[y].keys():
        #         q = self.get_quarter(k)
        #         histogram_new['{}_{}'.format(y, q)] = histogram[y][k]
        return histogram_new

    def get_surgery_dates_and_complications(self):
        try:
            use_cache = self.params.use_cache
        except AttributeError:
            use_cache = True
        try:
            verbose = self.params.verbose
        except AttributeError:
            verbose = False
        client = CastorClient()
        study_id = client.get_study_id(self.params.study_name)
        fields = client.get_fields(study_id, use_cache=use_cache, verbose=verbose)
        surgery_date_field_name = self.params.surgery_date_field_name
        surgery_date_field_id = client.get_field_id(surgery_date_field_name, fields)
        complications_field_name = self.params.complications_field_name
        complications_field_id = client.get_field_id(complications_field_name, fields)
        records = client.get_records(study_id, use_cache=use_cache, verbose=verbose)
        surgery_dates, complications = [], []
        for record in records:
            surgery_date_data = client.get_field_data(study_id, record['id'], surgery_date_field_id)
            if 'value' in surgery_date_data.keys():
                complications_data = client.get_field_data(study_id, record['id'], complications_field_id)
                if 'value' in complications_data.keys():
                    d = surgery_date_data['value']
                    c = int(complications_data['value'])
                    surgery_dates.append(d)
                    complications.append(c)
                    self.runner.logger.print('{}: surgery_date = {}, complications = {}'.format(record['id'], d, c))
        return surgery_dates, complications

    def execute(self):
        surgery_dates, complications = self.get_surgery_dates_and_complications()
        earliest_date, latest_date = self.get_earliest_and_latest_date(surgery_dates)
        earliest_year, latest_year = self.get_year(earliest_date), self.get_year(latest_date)
        try:
            year_begin = self.params.year_begin
        except AttributeError:
            year_begin = earliest_year
        try:
            year_end = self.params.year_end
        except AttributeError:
            year_end = latest_year
        histogram = self.get_histogram(year_begin, year_end, surgery_dates, complications)
        histogram = self.flatten_histogram(histogram)
        self.save_to_json(histogram)
