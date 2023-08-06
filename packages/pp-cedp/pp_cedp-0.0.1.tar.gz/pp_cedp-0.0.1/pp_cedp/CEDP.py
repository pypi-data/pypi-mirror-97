import pylcs
from pm4py.objects.log.importer.xes import factory as xes_importer_factory
from pm4py.objects.log.util import sorting
from pp_cedp.Utils import Utils
import numpy as np
import itertools
import pandas as pd
from pandas import ExcelWriter
import os
import multiprocessing as mp

class CEDP():

    def __init__(self):
        self = self


    def pylcs_len(self, A, B):
        return pylcs.lcs(A, B)

    def lcs_len(self, A, B):
        # find the length of the strings
        m = len(A)
        n = len(B)

        # declaring the array for storing the dp values
        L = [[None] * (n + 1) for i in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif A[i - 1] == B[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])
        return L[m][n]



    def lcs_str(self, A, B, m, n):
        L = [[0 for x in range(n + 1)] for x in range(m + 1)]

        # Following steps build L[m+1][n+1] in bottom up fashion. Note
        # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1]
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif A[i - 1] == B[j - 1]:
                    L[i][j] = L[i - 1][j - 1] + 1
                else:
                    L[i][j] = max(L[i - 1][j], L[i][j - 1])

                # Following code is used to print LCS
        index = L[m][n]

        # Create a character array to store the lcs string
        lcs = [""] * (index + 1)
        lcs[index] = ""

        # Start from the right-most-bottom-most corner and
        # one by one store characters in lcs[]
        i = m
        j = n
        while i > 0 and j > 0:

            # If current character in X[] and Y are same, then
            # current character is part of LCS
            if A[i - 1] == B[j - 1]:
                lcs[index - 1] = A[i - 1]
                i -= 1
                j -= 1
                index -= 1

            # If not same, then find the larger of two and
            # go in the direction of larger value
            elif L[i - 1][j] > L[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return "".join(lcs)

    def get_matching_set(self,simple_log,bk,n):
        matching_set ={}
        for key,value in simple_log.items():
            if n >= len(bk) - self.pylcs_len(bk,value['trace']):
                matching_set[key] = value
        return matching_set

    def get_matching_set_df(self,df,bk,n):
        df_matching = pd.DataFrame().reindex(columns=df.columns)
        for index, row in df.iterrows():
            if n >= len(bk) - self.pylcs_len(bk,row['trace']):
                df_matching = df_matching.append(row)
        return df_matching

    def get_matching_groups(self, matching_set_char_df, matching_set_char_df2, sensitive):
        number_groups2 = matching_set_char_df2['group'].max() + 1
        group_pairs_list = []
        for group_id in range(number_groups2):
            group_df2 = matching_set_char_df2.loc[matching_set_char_df2['group'] == group_id]
            sensitive_values = group_df2.iloc[0][sensitive]
            group_df1 = matching_set_char_df[np.logical_and.reduce(
                [matching_set_char_df[column] == value for column, value in sensitive_values.items()])]
            group_pairs = {}
            group_pairs['g1'] = group_df1  # g1
            group_pairs['g2'] = group_df2  # g2
            group_pairs_list.append(group_pairs)

        return group_pairs_list

    def calc_crack_size(self, matching_groups, sensitive, df_char, df_char2, n , map_dict_chr_act):
        for group_pairs in matching_groups:
            g1_size = group_pairs['g1'].shape[0]
            g2_size = group_pairs['g2'].shape[0]
            group_pairs['f_c'] = g1_size - min(g1_size, g2_size)  # crack size of group in g1 based on F-attack
            group_pairs['c_c'] = g2_size - min(g1_size, g2_size)  # crack size of group in g2 based on C-attack
            G1, G2 = self.get_comparable_from_R1(group_pairs['g2'], sensitive, df_char, df_char2, n, map_dict_chr_act)

            #union of g1 and G1
            uG1 = pd.concat([G1, group_pairs['g1']],sort=False)
            uG1 = uG1.drop_duplicates(subset=['case_id'])
            uG2 = pd.concat([G2, group_pairs['g2']],sort=False)
            uG2 = uG2.drop_duplicates(subset=['case_id'])
            b_c = max(0, uG1.shape[0]-(uG2.shape[0] - g2_size))
            group_pairs['b_c'] =  b_c # crack size of group in g2 based on B-attack
        return matching_groups

    #this function combines get_matching_groups and calc_crack_size
    def matching_groups_and_crack_size(self,matching_set_char_df, matching_set_char_df2, sensitive, df_char, df_char2, n , map_dict_chr_act):
        number_groups2 = matching_set_char_df2['group'].max() + 1
        group_pairs_list = []
        for group_id in range(number_groups2):
            group_df2 = matching_set_char_df2.loc[matching_set_char_df2['group'] == group_id]
            sensitive_values = group_df2.iloc[0][sensitive]
            group_df1 = matching_set_char_df[np.logical_and.reduce(
                [matching_set_char_df[column] == value for column, value in sensitive_values.items()])]
            group_pairs = {}
            group_pairs['g1'] = group_df1  # g1
            group_pairs['g2'] = group_df2  # g2
            g1_size = group_pairs['g1'].shape[0]
            g2_size = group_pairs['g2'].shape[0]


            group_pairs['f_c'] = g1_size - min(g1_size, g2_size)  # crack size of group in g1 based on F-attack
            group_pairs['c_c'] = g2_size - min(g1_size, g2_size)  # crack size of group in g2 based on C-attack
            G1, G2 = self.get_comparable_from_R1(group_pairs['g2'], sensitive_values, df_char, df_char2, n, map_dict_chr_act)
            # uG1 = pd.concat([G1, group_pairs['g1']], sort=False)
            # uG1 = uG1.drop_duplicates(subset=['case_id'])
            # uG2 = pd.concat([G2, group_pairs['g2']], sort=False)
            # uG2 = uG2.drop_duplicates(subset=['case_id'])
            # b_c = max(0, uG1.shape[0] - (uG2.shape[0] - g2_size))  # crack size of group in g2 based on B-attack
            if G1.shape[0] == 0 or G2.shape[0] == 0:
                b_c = 0
            elif G1.shape[0] > (G2.shape[0] - g2_size):
                b_c = max(0, G1.shape[0] - (G2.shape[0] - g2_size))  # crack size of group in g2 based on B-attack
            else:
                b_c = 0
            group_pairs['b_c'] = b_c
            group_pairs_list.append(group_pairs)

        return group_pairs_list

    def get_comparable_from_R1(self, g2, sensitive_values, R1, R2, n, map_dict_chr_act):
        G1 = pd.DataFrame().reindex(columns=R1.columns)
        G2 = pd.DataFrame().reindex(columns=R2.columns)
        # sensitive_values = g2.iloc[0][sensitive]
        #get all the rows matching the sensitive attributes
        R1_sensitive_match = R1[np.logical_and.reduce(
            [R1[column] == value for column, value in sensitive_values.items()])]

        if not R1_sensitive_match.empty:
            for index_R1, row_R1 in R1_sensitive_match.iterrows():
                match_result = False
                for index_g2, row_g2 in g2.iterrows():
                    utils = Utils()
                    # trace_R1 = utils.convert_char_to_act(row_R1['trace'],map_dict_chr_act)
                    # trace_G2 = utils.convert_char_to_act(row_g2['trace'],map_dict_chr_act)
                    match_result = self.check_sequence_comparability(row_R1['trace'], row_g2['trace'], n)
                    if match_result:
                        break
                if match_result:
                    G1 = G1.append(row_R1)

        if not G1.empty:
            R2_sensitive_match = R2[np.logical_and.reduce(
                [R2[column] == value for column, value in sensitive_values.items()])]
            for index_R2, row_R2 in R2_sensitive_match.iterrows():
                match_result = False
                for index_G1, row_G1 in G1.iterrows():
                    match_result = self.check_sequence_comparability(row_G1['trace'],row_R2['trace'], n)
                    if match_result:
                        break
                if match_result:
                    G2 = G2.append(row_R2)

        return G1, G2

    def check_sequence_comparability(self, seq1, seq2, n):
        result = False
        len_seq1 = len(seq1)
        len_seq2 = len(seq2)
        LCS = self.lcs_str(seq1, seq2, len_seq1, len_seq2)
        len_LCS = len(LCS)
        len_SCS = len_seq1 + len_seq2 - len_LCS
        is_prefix = seq2.startswith(LCS)
        if is_prefix:
            if n >= len_seq1 - len_LCS:
                result = True
        elif n >= len_SCS - min(len_seq1,len_seq2):
                result = True

        return result

    def calc_FCB_anonymity_per_bk(self, df_char, df_char2, bk, n, sensitive, map_dict_act_chr, map_dict_chr_act):
        bk_string = ""
        for item in bk:
            bk_string += item
        utils = Utils()
        # matching_set_char = cedp.get_matching_set(simple_log_char,bk_string,1)
        matching_set_char_df = self.get_matching_set_df(df_char, bk_string, n)
        # matching_set_char2 = cedp.get_matching_set(simple_log_char2,bk_string,1)
        matching_set_char_df2 = self.get_matching_set_df(df_char2, bk_string, n)
        matching_set_char_df['group'] = matching_set_char_df.groupby(sensitive).ngroup()
        matching_set_char_df2['group'] = matching_set_char_df2.groupby(sensitive).ngroup()
        f_crack_size = 0
        c_crack_size = 0
        b_crack_size = 0
        no_matching = False
        fa = 0
        ca = 0
        ba = 0
        R1_ka = matching_set_char_df.shape[0]
        R2_ka = matching_set_char_df2.shape[0]
        bk_act = utils.convert_char_to_act(bk_string, map_dict_chr_act)

        if matching_set_char_df.empty or matching_set_char_df2.empty:
            fa = R1_ka - f_crack_size
            ca = R2_ka - c_crack_size
            ba = R2_ka - b_crack_size
            no_matching = True
        else:
            # matching_groups = self.get_matching_groups(matching_set_char_df, matching_set_char_df2, sensitive)
            # matching_groups_with_crack_sizes = self.calc_crack_size(matching_groups, sensitive, df_char, df_char2, n,
            #                                                         map_dict_chr_act)
            matching_groups_with_crack_sizes = self.matching_groups_and_crack_size(matching_set_char_df, matching_set_char_df2, sensitive, df_char,
                                           df_char2, n, map_dict_chr_act)
            for item in matching_groups_with_crack_sizes:
                f_crack_size += item['f_c']
                c_crack_size += item['c_c']
                b_crack_size += item['b_c']
            fa = R1_ka - f_crack_size
            ca = R2_ka - c_crack_size
            ba = R2_ka - b_crack_size

        print("bk: %s, fc:%d -- cc:%d -- bc:%d" % (bk_act, f_crack_size, c_crack_size, b_crack_size))
        print("bk: %s, fa:%d -- ca:%d -- ba:%d" % (bk_act, fa, ca, ba))
        print("-------------------")

        return no_matching, bk_act, fa, ca, ba, R1_ka, R2_ka

    def calc_FCB_anonymity(self, log_name1, log_name2, event_attributes, life_cycle, all_life_cycle, sensitive, time_accuracy, n, bk_length, result_log_name, results_dir = "./Results",
                           from_time_days =0, to_time_days=0, multiprocess=True):

        log1 = xes_importer_factory.apply(log_name1)
        log2 = xes_importer_factory.apply(log_name2)
        log1 = sorting.sort_timestamp(log1)
        log2 = sorting.sort_timestamp(log2)
        utils = Utils()

        simple_log, traces, sensitive_values, df = utils.create_simple_log_adv(log1, event_attributes, life_cycle,
                                                                               all_life_cycle, sensitive,
                                                                               time_accuracy, from_time_days, to_time_days)
        # new_event_log = utils.createEventLog(log,simple_log,event_attributes,life_cycle,all_life_cycle, sensitive,time_accuracy)
        # xes_exporter.export_log(new_event_log, "EL1.xes")

        simple_log2, traces2, sensitive_values2, df2 = utils.create_simple_log_adv(log2, event_attributes, life_cycle,
                                                                                   all_life_cycle, sensitive,
                                                                                   time_accuracy, from_time_days, to_time_days)
        # new_event_log = utils.createEventLog(log,simple_log2,event_attributes,life_cycle,all_life_cycle, sensitive,time_accuracy)
        # xes_exporter.export_log(new_event_log, "EL2.xes")

        activities1 = utils.get_unique_act(traces)
        activities2 = utils.get_unique_act(traces2)

        uniq_activities = activities2.union(activities1)

        map_dict_act_chr, map_dict_chr_act, uniq_char = utils.map_act_char(uniq_activities)

        simple_log_char = utils.convert_simple_log_act_to_char(simple_log, map_dict_act_chr)
        df_char = utils.convert_lof_dataframe_act_to_char(df, map_dict_act_chr)

        simple_log_char2 = utils.convert_simple_log_act_to_char(simple_log2, map_dict_act_chr)
        df_char2 = utils.convert_lof_dataframe_act_to_char(df2, map_dict_act_chr)

        df_char.replace(np.nan, '--', inplace=True)  # this will consider nan values as a sensitive attribute!
        df_char2.replace(np.nan, '--', inplace=True)  # this will consider nan values as a sensitive attribute!

        # utils.add_fake_activities(uniq_char,map_dict_act_chr, map_dict_chr_act, bk_length)

        bk_candidate_iter = itertools.product(uniq_char, repeat=bk_length)
        bk_candidate = list(bk_candidate_iter)

        results_dir = results_dir
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        file_name = "Result_" + result_log_name + "_bk_length_" + str(bk_length) + "_n_" + str(n) + ".xlsx"
        result_file = os.path.join(results_dir, file_name)

        columns = ['bk', 'R1-K', 'R2-K', 'FA', 'CA', 'BA']
        df_result = pd.DataFrame(columns=columns)
        FA_list =[]
        BA_list =[]
        CA_list = []
        R1_KA_list =[]
        R2_KA_list =[]
        results = []

        if multiprocess:
            pool = mp.Pool()
            workers = []
            workers_number = os.cpu_count()
            data_chunks = self.chunkIt(bk_candidate, workers_number)
            for worker in range(workers_number):
                print("In worker %d out of %d" % (worker + 1, workers_number))
                workers.append(pool.apply_async(self.FCB_anonymity_worker, args=(
                data_chunks[worker], df_char, df_char2, n,sensitive, map_dict_act_chr, map_dict_chr_act)))
            for work in workers:
                results.append(work.get())
            pool.close()
            pool.join()

        else:
            result = self.FCB_anonymity(bk_candidate, df_char, df_char2, n, sensitive, map_dict_act_chr, map_dict_chr_act)
            results.append(result)

        for result in results:
            for key, value in result.items():
                if key == 'df_result':
                    df_result = pd.concat([df_result, value],sort=False)
                elif key == 'FA':
                    FA_list.append(value)
                elif key == 'CA':
                    CA_list.append(value)
                elif key == 'BA':
                    BA_list.append(value)
                elif key == 'R1_KA':
                    R1_KA_list.append(value)
                elif key == 'R2_KA':
                    R2_KA_list.append(value)
        FA = min(FA_list)
        CA = min(CA_list)
        BA = min(BA_list)
        R1_KA = min(R1_KA_list)
        R2_KA = min(R2_KA_list)

        df_result_last_row = {'bk': "Event Log", 'R1-K': R1_KA, 'R2-K': R2_KA, 'FA': FA, 'CA': CA, 'BA': BA}
        df_result = df_result.append(df_result_last_row, ignore_index=True)
        writer = ExcelWriter(result_file)
        df_result.to_excel(writer, 'bk_length_' + str(bk_length) + "-n_" + str(n))
        writer.save()

        las_line = "Result for Event Log, R1-KA:%d, R2-KA:%d, FA:%d, CA:%d, BA:%d" % (R1_KA, R2_KA, FA, CA, BA)
        print(las_line)


    def chunkIt(self, data, num):
        avg = len(data) / float(num)
        out = []
        last = 0.0
        while last < len(data):
            out.append(data[int(last):int(last + avg)])
            last += avg
        return out

    def FCB_anonymity_worker(self, data_bk, df_char, df_char2, n,sensitive, map_dict_act_chr, map_dict_chr_act):
        return self.FCB_anonymity(data_bk, df_char, df_char2, n,sensitive, map_dict_act_chr, map_dict_chr_act)

    def FCB_anonymity(self,data_bk, df_char, df_char2, n,sensitive, map_dict_act_chr, map_dict_chr_act):
        FA = 10 ** 10
        CA = 10 ** 10
        BA = 10 ** 10
        R1_KA = 10 ** 10
        R2_KA = 10 ** 10
        columns = ['bk', 'R1-K', 'R2-K', 'FA', 'CA', 'BA']
        df_result = pd.DataFrame(columns=columns)
        length_candidates = len(data_bk)
        counter = 0
        for bk in data_bk:
            counter += 1
            print("in item " + str(counter) + " of " + str(length_candidates))

            # bk = ['Leucocytes', 'Leucocytes', 'ER Triage']
            # bk = utils.convert_act_to_char(bk,map_dict_act_chr)
            no_matching, bk_act, fa, ca, ba, R1_ka, R2_ka = self.calc_FCB_anonymity_per_bk(df_char, df_char2, bk, n,
                                                                                           sensitive, map_dict_act_chr,
                                                                                           map_dict_chr_act)
            df_result_row = {'bk': bk_act, 'R1-K': R1_ka, 'R2-K': R2_ka, 'FA': fa, 'CA': ca, 'BA': ba}
            df_result = df_result.append(df_result_row, ignore_index=True)
            if fa < FA and not no_matching:
                FA = fa
            if ca < CA and not no_matching:
                CA = ca
            if ba < BA and not no_matching:
                BA = ba
            if R1_ka < R1_KA and not no_matching:
                R1_KA = R1_ka
            if R2_ka < R2_KA and not no_matching:
                R2_KA = R2_ka

        result = {'df_result':df_result, 'FA':FA, 'CA':CA, 'BA':BA, 'R1_KA':R1_KA, 'R2_KA':R2_KA}

        return result