from itertools import chain
import copy
import datetime
import pandas as pd
from pm4py.objects.log.log import Trace, EventLog
import itertools

class Utils():

    def __init__(self):
        self = self

    def create_simple_log_adv(self, log, event_attributes, life_cycle, all_life_cycle, sensitive_attributes,
                              time_accuracy,from_time_days, to_time_days):
        time_prefix = 'time:timestamp'
        life_cycle_prefix = ['lifecycle:transition']
        logsimple = {}
        traces = []
        sensitives = {el: [] for el in sensitive_attributes}
        columns = ['case_id','trace']
        columns += sensitive_attributes
        dataframe = pd.DataFrame(columns=columns)

        start_time, end_time = self.get_start_end_time(log)
        from_time = 0
        to_time = 0
        if from_time_days != 0 and to_time_days != 0:
            from_time = start_time - datetime.timedelta(days=from_time_days)
            from_time = from_time.replace(hour=00, minute=00, second=00, microsecond=000000)
            to_time = start_time + datetime.timedelta(days=to_time_days - 1)
            to_time = to_time.replace(hour=23, minute=59, second=59, microsecond=999999)

        for case_index, case in enumerate(log):
            trace, sens = self.create_trace(case, event_attributes, life_cycle, all_life_cycle, life_cycle_prefix, time_prefix,
                                            sensitive_attributes, time_accuracy, from_time, to_time)
            if len(trace) > 0:
                df_row = {'case_id': case.attributes["concept:name"], 'trace':trace}
                logsimple[case.attributes["concept:name"]] = {"trace": tuple(trace), "sensitive": sens}
                traces.append(tuple(trace))
                for key in sens.keys():
                    sensitives[key].append(sens[key])
                    #for datafrane
                    df_row[key] = sens[key]
                dataframe = dataframe.append(df_row,ignore_index=True)

        return logsimple, traces, sensitives, dataframe

    def create_trace(self, case, event_attributes, life_cycle, all_life_cycle, life_cycle_prefix,
                     time_prefix, sensitive_attributes, time_accuracy, from_time, to_time):
        sens = {}
        trace = []
        #check sensitive attributes at case level
        sens_dict ={}
        for key, value in case.attributes.items():
            if key in sensitive_attributes:
                sens_dict[key] = value

        for event_index, event in enumerate(case):
            simple_attr_temp = []
            life_cycle_value = ''
            event_dict = {}
            time_matches = False
            for key, value in event.items():
                if key == time_prefix:
                    if from_time == 0 and to_time == 0:
                        time_matches = True
                    elif from_time < value and value <= to_time:
                        time_matches = True
                    if time_prefix in event_attributes:
                        if time_accuracy == 'original':
                            time = value
                        else:
                            if time_accuracy == "seconds":
                                time = value.replace(microsecond=0)
                            elif time_accuracy == "minutes":
                                time = value.replace(second=0, microsecond=0)
                            elif time_accuracy == "hours":
                                time = value.replace(minute=0, second=0, microsecond=0)
                            elif time_accuracy == "days":
                                time = value.replace(hour=0, minute=0, second=0, microsecond=0)
                        event_dict[key] = time

                if key in event_attributes and key != time_prefix:
                    event_dict[key] = value
                if key in sensitive_attributes:
                    sens_dict[key] = value
                if key in life_cycle_prefix:
                    life_cycle_value = value
            if (all_life_cycle or (life_cycle_value in life_cycle)) and time_matches:
                if len(event_dict) < 2:
                    simple_event = list(event_dict.values())[0]
                else:
                    for att in event_attributes:
                        if att in event_dict:
                            simple_attr_temp.append(event_dict[att])
                    simple_event = tuple(simple_attr_temp)
                trace.append(simple_event)

                #for saving the order
                for item in sensitive_attributes:
                    if item in sens_dict:
                        sens[item] = sens_dict[item]

        return trace, sens

    def createEventLog(self, original_log, simplifiedlog, event_attributes, life_cycle, all_life_cycle, sensitive_attributes, time_accuracy):
        time_prefix = 'time:timestamp'
        life_cycle_prefix = ['lifecycle:transition']
        deleteLog = []
        log = copy.deepcopy(original_log)
        for i in range(0, len(log)):
            caseId = log[i].attributes["concept:name"]
            if caseId not in simplifiedlog.keys():
                deleteLog.append(i)
                continue
            trace = simplifiedlog[caseId]["trace"]
            del_list = []
            simple_trace, sens = self.create_trace(log[i], event_attributes, life_cycle, all_life_cycle, life_cycle_prefix,
                                            time_prefix, sensitive_attributes, time_accuracy, 0, 0)
            j = 0
            while j < len(log[i]):
                if (simple_trace[j] not in trace):
                    del_list.append(log[i][j])
                j += 1
            for x in del_list:
                log[i]._list.remove(x)

        for i in sorted(deleteLog, reverse=True):
            log._list.remove(log[i])

        log2 = EventLog([trace for trace in log], classifiers = original_log.classifiers)

        return log2

    def get_start_end_time(self,log):
        start_time = log[0][0]['time:timestamp']
        end_time = log[len(log) - 1][len(log[len(log) - 1]) - 1]['time:timestamp']

        return start_time,end_time

    def get_unique_act(self, iter):
        act_list = chain.from_iterable(iter)
        return set(act_list)

    def map_act_char(self, uniq_act):

        # uniq_act = self.get_unique_act(traces)
        uniq_char = []
        map_dict_act_chr = {}
        map_dict_chr_act = {}
        for index, item in enumerate(uniq_act):
            map_dict_act_chr[item] = chr(index)
            map_dict_chr_act[chr(index)] = item
            uniq_char.append(chr(index))
        return map_dict_act_chr, map_dict_chr_act, uniq_char

    def convert_act_to_char(self, trace, map_dict_act_chr):
        trace_str = ""
        for item in trace:
            try:
                trace_str += map_dict_act_chr[item]
            except KeyError:
                map_dict_act_chr[item] = chr(len(map_dict_act_chr))
                trace_str += map_dict_act_chr[item]
        return trace_str

    def convert_char_to_act(self, trace, map_dict_chr_act):
        trace_act = []
        for item in trace:
            trace_act.append(map_dict_chr_act[item])
        return trace_act

    def convert_simple_log_act_to_char(self,simple_log,map_dict_act_chr):
        simple_log_char = copy.deepcopy(simple_log)
        for key,value in simple_log.items():
            trace_string = self.convert_act_to_char(value['trace'],map_dict_act_chr)
            simple_log_char[key]['trace'] = trace_string
        return simple_log_char

    def convert_simple_log_char_to_act(self,simple_log,map_dict_chr_act):
        simple_log_act = copy.deepcopy(simple_log)
        for key,value in simple_log.items():
            trace_act = self.convert_char_to_act(value['trace'],map_dict_chr_act)
            simple_log_act[key]['trace'] = trace_act
        return simple_log_act

    def convert_lof_dataframe_act_to_char(self,df,map_dict_act_chr):
        df_string = df
        for index, row in df.iterrows():
            trace_string = self.convert_act_to_char(row['trace'], map_dict_act_chr)
            df_string.iloc[index]['trace'] = trace_string
        return df_string

    def add_fake_activities(self, uniq_char, map_dict_act_chr, map_dict_chr_act, bk_length):
        fake_act = "::fake::"
        for fake_item in range(2):
            fake_item = fake_act + str(fake_item)
            map_dict_act_chr[fake_item] = chr(len(map_dict_act_chr))
            map_dict_chr_act[chr(len(map_dict_act_chr))] = fake_item
            uniq_char.append(chr(len(map_dict_act_chr)))

    def get_sub_sequence(self,traces, traces2, length):
        sub_seqs = []
        for item in traces2:
            indexes = [i for i in range(len(item))]
            sub_indexes = self.find_subsets(indexes, length)
            for sub_index in sub_indexes:
                list_sub_index = sorted(list(sub_index))
                sub_seq = [item[index] for index in list_sub_index]
                if sub_seq not in sub_seqs:
                    sub_seqs.append(sub_seq)
        for item in traces:
            indexes = [i for i in range(len(item))]
            sub_indexes = self.find_subsets(indexes, length)
            for sub_index in sub_indexes:
                list_sub_index = sorted(list(sub_index))
                sub_seq = [item[index] for index in list_sub_index]
                if sub_seq not in sub_seqs:
                    sub_seqs.append(sub_seq)
        return sub_seqs

    def find_subsets(self,uniq_act, k):
        return list(map(set, itertools.combinations(uniq_act, k)))