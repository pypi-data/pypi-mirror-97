#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: speech_parse.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date: 2020/12/09 上午11:55
"""
import os
from openpyxl import Workbook
from itertools import product
import numpy as np
from collections import Counter
import linecache
import logging
import subprocess
import copy
import re

import xls
import globalVal
from wer_client import wer


def cal_asr_wer(answer_result, recognize_result, total_count=-1):
    """
        [识别准确率] 使用wer工具，计算识别字准、句准
    Args:
        answer_result : [string] 标注答案的txt文件地址，每行以"音频名称.pcm:query内容"格式存储
        recognize_result : [string] 识别结果的txt文件地址，每行以"音频名称.pcm:query内容"格式存储
        total_count : [int] 总识别query条数，仅"语义识别"模式下传入，其他模式下默认值-1
    Returns:
        charACU : [string] 识别字准，保留3位有效数字
        sentenseACU : [string] 识别句准，保留3位有效数字
    """
    if total_count != -1:
        return _semantics_accuracy(answer_result, recognize_result, total_count)
    answer_result = os.path.abspath(answer_result)
    recognize_result = os.path.abspath(recognize_result)
    acu_result = str(recognize_result) + '-c'
    if os.path.exists(recognize_result) and os.path.getsize(recognize_result):
        if not os.path.exists(acu_result):
            retry_count = 3
            while retry_count:
                wer_info = str(recognize_result) + '.err.' + str(retry_count)
                retry_count -= 1
                if globalVal._ENVIRONMENT == 'windows':
                    flag, command_result = wer(answer_result, recognize_result, acu_result, wer_info)
                else:
                    if globalVal._ENVIRONMENT == 'linux':
                        command_line = r'cd %s && %s %s %s %s >%s 2>&1' \
                            % (globalVal._TOOL_ACUCALC[globalVal._ENVIRONMENT]['dir'], \
                            globalVal._TOOL_ACUCALC[globalVal._ENVIRONMENT]['bin'], answer_result, \
                            recognize_result, acu_result, wer_info)
                    else:
                        command_line = r'cd %s && %s %s %s %s %s >%s 2>&1' \
                            % (globalVal._TOOL_ACUCALC[globalVal._ENVIRONMENT]['dir'], \
                            globalVal._TOOL_ACUCALC[globalVal._ENVIRONMENT]['bin'], \
                            answer_result, recognize_result, acu_result, \
                            globalVal._TOOL_ACUCALC[globalVal._ENVIRONMENT]['conf'], wer_info)
                    flag, command_result = subprocess.getstatusoutput(command_line)
                if os.path.exists(acu_result):
                    break
    else:
        wer_info = recognize_result
        command_result = '该文件不存在或为空，导致wer计算失败'
    errInfo = []
    if os.path.exists(acu_result):
        charACU = _get_wer_from_file(acu_result, 'CHARACTOR_ACU')
        sentenseACU = _get_wer_from_file(acu_result, 'UTTERANCE_ACU')
        err = _get_wer_from_file(acu_result, 'TOTAL_ERR')
        errInfo = list(filter(_not_empty, re.split(r'[: \]]', err)))[1::2]
    else:
        charACU = 'Nan'
        sentenseACU = 'Nan'
        globalVal.record_err(wer_info, 3001, command_result)
    return charACU, sentenseACU, errInfo


def cal_speed_performance(speed_list):
    """
        [速度性能统计] 计算速度中位数、90分位数、标准差、最小值、最大值
    Args:
        speed_list : [list] 速度列表
    Returns:
        perform_list : [list] [中位数, 90分位数, 标准差, 最小值, 最大值]
    """
    return [np.median(speed_list), np.percentile(speed_list, 90), np.std(speed_list), 
        np.min(speed_list), np.max(speed_list)]


def cal_wp_status(wp_dict):
    """唤醒性能数据更新
    """
    if 'whisperCount' in wp_dict:
        rightRate = '0.0%'
        wpRate = '0.0%'
        queryCount = wp_dict['queryCount']
        if queryCount:
            if wp_dict['detectCount']:
                wp_dict['wpAvgTime'] = float(wp_dict['totalTime'] / wp_dict['detectCount'])
                rightRate = "%.3f%%" % float(wp_dict['rightCount'] * 100 / wp_dict['detectCount'])
                wpRate = "%.3f%%" % float(wp_dict['detectCount'] * 100 / queryCount)
        wp_dict.update({
            'rightRate': rightRate,
            'wpRate': wpRate
        })
    else:
        rightRate = '0.0%'
        rightWordRate = '0.0%'
        wrongWordRate = '0.0%'
        wrongWordCount = 0
        wrongIndexCount = 0
        wrongIndexRate = '0.0%'
        queryCount = wp_dict['queryCount']
        if queryCount:
            if wp_dict['detectCount']:
                wp_dict['wpAvgTime'] = float(wp_dict['totalTime']) / float(wp_dict['detectCount'])
            wrongWordCount = wp_dict['detectCount'] - wp_dict['rightWordCount']
            wrongIndexCount = wp_dict['detectCount'] - wp_dict['rightIndexCount']
            rightRate = "%.3f%%" % float(wp_dict['rightCount'] * 100 / queryCount)
            rightWordRate = "%.3f%%" % float(wp_dict['rightWordCount'] * 100 / queryCount)
            wrongWordRate = "%.3f%%" % float(wrongWordCount * 100 / queryCount)
            wrongIndexRate = "%.3f%%" % float(wrongIndexCount * 100 / queryCount)
        wp_dict.update({
            'rightRate': rightRate, 
            'rightWordRate': rightWordRate, 
            'wrongWordCount': wrongWordCount, 
            'wrongWordRate': wrongWordRate, 
            'wrongIndexCount': wrongIndexCount, 
            'wrongIndexRate': wrongIndexRate
        })

    if 'whisperInfo' in wp_dict:
        for whisper in wp_dict['whisperInfo']:
            cal_wp_status(wp_dict['whisperInfo'][whisper])


def update_whisper_info(wp_status, add_status):
    """whisper性能统计
    """
    for whisper_status in add_status:
        if whisper_status not in wp_status:
            wp_status.update({whisper_status: copy.deepcopy(add_status[whisper_status])})
        else:
            for key in wp_status[whisper_status]:
                if key not in ['wpAvgTime', 'wpMaxTime']:
                    wp_status[whisper_status][key] += add_status[whisper_status][key]
            if wp_status[whisper_status]['wpMaxTime'] < add_status[whisper_status]['wpMaxTime']:
                wp_status[whisper_status]['wpMaxTime'] = add_status[whisper_status]['wpMaxTime']


def cal_wp_performance(wp_status, false_wp):
    """唤醒性能数据统计
    """
    if 'whisperInfo' in wp_status['summary']:
        key_list = globalVal._WHISPER_DICT
    else:
        key_list = globalVal._WP_DICT
    for wpWords in wp_status:
        if wpWords == 'summary':
            continue
        # [1] 更新常规key到summary
        curr_result = wp_status[wpWords]
        for key in key_list:
            if key not in ['wpAvgTime', 'wpMaxTime', 'whisperInfo']:
                wp_status['summary'][key] += curr_result[key]
        if 'whisperInfo' in wp_status['summary']:
            update_whisper_info(wp_status['summary']['whisperInfo'], curr_result['whisperInfo'])
        if wp_status['summary']['wpMaxTime'] < curr_result['wpMaxTime']:
            wp_status['summary']['wpMaxTime'] = curr_result['wpMaxTime']
        # [2] 计算唤醒速度、唤醒词误串、音区误串率等指标
        cal_wp_status(wp_status[wpWords])
    cal_wp_status(wp_status['summary'])
    # [3] 计算总的唤醒误报次数
    total_false = 0
    for wpWords in false_wp:
        total_false += false_wp[wpWords]
    false_wp.update({'summary': total_false})


def cal_wp_location_diff(location_a, location_b):
    """
        [唤醒声源定位] 获取定位准确度、定位偏差
    Args:
        location_a : [int] 标注答案的角度
        location_b : [int] 信号/唤醒算法，计算得到的角度
    Returns:
        is_right_location : [int] 定位准确度，1:定位正确, 2:相邻灯位正确, 0:错误
        location_diff : [int] 定位角度差，location_a与location_b的差值
    """
    # [1] 计算角度差
    if location_a >= location_b:
        if location_a - location_b > 180:
            location_diff = location_b - location_a + 360
        else:
            location_diff = location_b - location_a
    else:
        if location_b - location_a > 180:
            location_diff = location_b - location_a - 360
        else:
            location_diff = location_b - location_a
    # [2] 判断定位是否正确，即在 标记位置±15° 或 标记位置±45° 范围内
    is_right_location = 0
    if cal_location_accuracy(location_a, location_b, globalVal._PARAM['WP_LOCATION_RIGHT_RANGE']):
        is_right_location = 1
    elif cal_location_accuracy(location_a, location_b, globalVal._PARAM['WP_LOCATION_IN_RANGE']):
        is_right_location = 2

    return is_right_location, location_diff


def cal_location_accuracy(location_a, location_b, location_range):
    """
        [唤醒声源定位] 计算定位准确度
    Args:
        location_a : [int] 标注答案的角度
        location_b : [int] 信号/唤醒算法，计算得到的角度
        location_range : [list] 角度差值允许范围，参考globalVal._PARAM['WP_LOCATION_RIGHT_RANGE']定义
    Returns:
        bool : True:正确，False:错误
    """
    location_begin = _location_unify(location_a + location_range[0])
    location_end = _location_unify(location_a + location_range[1])
    if location_end - location_begin == location_range[1] - location_range[0]:
        if location_b >= location_begin and location_b <= location_end:
            return True
        else:
            return False
    else:
        if location_b >= location_begin and location_b <= 360:
            return True
        elif location_b >= 0 and location_b <= location_end:
            return True
        else:
            return False


def record_wp_location_accuracy(location_answer, location_list, sdk_version, audio_scene):
    """
        [唤醒声源定位] 测试结果记录入文件
    """
    with open(globalVal._LOCATION_RECORD_FILE_NAME, 'a+', encoding='utf-8') as location_file:
        location_file.write('[' + str(sdk_version) + '] ' + str(audio_scene) + '\n')
        for scene in location_answer:
            for location in location_answer[scene]: 
                wp_count = int(location_answer[scene][location]['wpCount'])
                total_count = int(location_answer[scene][location]['total'])
                false_count = 0
                right_count = 0
                in_count = 0
                if scene in location_list and location in location_list[scene]:
                    result = np.array(sorted(location_list[scene][location].values(), key=(lambda _:_[0])))
                    result = Counter(result[:, 0]).most_common()
                    for value in result:
                        if value[0] == 1:
                            right_count = int(value[1])
                        elif value[0] == 2:
                            in_count = int(value[1])
                        else:
                            false_count = int(value[1])
                    if false_count + in_count + right_count != wp_count:
                        print(sdk_version + ':' + audio_scene + ':' + str(scene) + ':' + str(location) \
                            + ':' + str(right_count) + ',' + str(in_count) + ',' + str(false_count) + ',' \
                            + str(wp_count) + ',' + str(total_count) + '\n')
                    else:
                        location_file.write(sdk_version + ':' + audio_scene + ':' + str(scene) + ':' + str(location) \
                            + ':' + str(right_count) + ',' + str(in_count) \
                            + ',' + str(wp_count) + ',' + str(total_count) + '\n')
                else:
                    location_file.write(sdk_version + ':' + audio_scene + ':' + str(scene) + ':' + str(location) \
                        + ':' + str(right_count) + ',' + str(in_count) \
                        + ',' + str(wp_count) + ',' + str(total_count) + '\n')

    location_file.close()


def parse_asr_err(err_list, denominator):
    """
        [识别错误码] 记录每个错误类型的次数
    Args:
        err_list : [list] 错误列表
        denominator : [int] 分母（总请求次数）
    Returns:
        err_info : [dict] 每个错误类型的次数
    """
    err_info = {'info': {}, 'diff': {}, 'denominator': denominator}
    for item in set(err_list):
        if item != '':
            err_info['info'].update({str(item): err_list.count(item)})
    return err_info
    

class QueryFilter(object):
    """Get valid asr query"""
    def __init__(self, sampleset_name, sdk_version):
        """
            [识别query统计] 根据唤醒和识别的错误码情况，排除不参与统计识别的query
        Args:
            sampleset_name : [string] 测试集名称，由"audio-scene_audio-name"组成
            sdk_version : [string] SDK版本
        Returns:
            null
        """
        self.sdk_version = sdk_version
        audio_scene, audio_name = globalVal.get_scene_name(sampleset_name)
        self.speech_type = globalVal.get_speech_type(sampleset_name)
        self.save_path = globalVal.get_save_path(audio_scene, audio_name)
        self.sampleset_name = audio_scene + '_' + audio_name
        self.result_path = os.path.join(
            self.save_path, 
            self.sdk_version + '_' + self.sampleset_name + '_recognize_result.txt'
        )

        self.recg_query = {}                # 参与识别统计的query
        self.ready_request_count = 0        # [识别指标]识别请求次数（单次:正常唤醒且有识别标注，多次:supported的query）
        self.invalid_request_count = 0      # [识别指标]无效识别请求次数（对齐且因为网络原因引起的失败）
        self.valid_request_count = 0        # [识别指标]有效识别请求次数（识别成功率的分母）
        self.asr_success_count = 0          # [识别指标]识别成功次数（对齐且有识别结果、不区分是否拒识）
        self.asr_recall_count = 0           # [识别指标]多次召回次数、纯识别准召次数
        self.first_success_count = 0        # [识别指标]多次识别首次请求成功次数

    def parse_asr_query(self, asr_query):
        """
            [识别结果过滤] 根据对应场景下每条query的识别详情，统计识别成功次数、召回次数等指标
        Args:
            asr_query : [dict] 每条query的识别详情
        Returns:
            recg_query : [dict] 参与识别统计的query
            count_list : [list] 有效、无效识别请求次数，识别成功次数，召回次数，首次请求成功次数等指标
        """
        if self.speech_type == globalVal.SpeechType.MULTI_ASR:
            self.parse_rule_2(asr_query)
        elif self.speech_type == globalVal.SpeechType.VOICE_PRINT:
            self.parse_rule_4(asr_query)
        elif self.speech_type in globalVal.SPEECH_MODE['asr']:
            self.parse_rule_3(asr_query)
        elif self.speech_type in [globalVal.SpeechType.ASR, globalVal.SpeechType.SEMANTIC_ASR, 
            globalVal.SpeechType.OFFLINE_ASR]:
            self.parse_rule_1(asr_query)
        elif 'asr' in self.sampleset_name and self.speech_type == globalVal.SpeechType.WHISPER:
            self.parse_rule_1(asr_query)

        return self.recg_query, [self.ready_request_count, self.invalid_request_count, self.valid_request_count, \
            self.asr_success_count, self.asr_recall_count, self.first_success_count]

    def parse_rule_1(self, asr_query):
        """
            [规则1:单次识别] 排除掉未唤醒和网络错误码的情况
        """
        #【单次识别】dict描述（1、2、3参与识别率统计，4、5不参与）
        # {'pcm_name': 'jike-false_asr_speed_aj_1m_luqi', 'desc': '识别相关标签', 'recg_result': '识别结果'}
        # 1:唤醒、有识别结果，desc为''
        # 2:唤醒、无识别结果，非网络错误，desc为'err:错误码'，recg_result为''
        # 3:唤醒、未对齐，desc为'no asr'，recg_result为''
        # 4:唤醒、无识别结果，网络错误，desc为'net_err:错误码'，recg_result为''
        # 5:没唤醒，desc为'no wakeup'，recg_result为''
        with open(self.result_path, 'w', encoding='utf-8') as result_file:
            for query_name in asr_query:
                query = asr_query[query_name]
                if not 'no wakeup' in query['desc']:
                    self.ready_request_count += 1
                    if 'net_err' in query['desc'] or 'ignore' in query['desc']:
                        self.invalid_request_count += 1
                    else:
                        self.valid_request_count += 1
                        self.recg_query.update({query_name: query})
                        result_file.write(query_name + ':' + query['recg_result'] + '\n')
                        if query['recg_result'] != '':
                            self.asr_success_count += 1
        result_file.close()

    def parse_rule_2(self, asr_query):
        """
            [规则2:一次唤醒多次识别] 排除掉未唤醒、误唤醒、首次识别无结果或回调网络错误码的情况
        """
        #【多次识别】（1、2、3参与识别率统计，4、5、6、7、8、9不参与）
        # {'pcm_name': 'jike-false_asr_speed_aj_1m_luqi', 'desc': '识别相关标签', 'recg_result': '识别结果'}
        # 1:supported、2～N次识别、有识别结果，asr_reject为0，desc为''
        # 2:supported、2～N次识别、有识别结果，asr_reject为1，desc为'asr reject'
        # 3:supported、2～N次识别、无识别结果，非网络错误，desc为'err:错误码'，recg_result为''
        # 4:supported、2～N次识别、无识别结果，网络错误，desc为'net_err:错误码'，recg_result为''
        # 5:unsupported、2～N次识别、有识别结果，asr_reject为0，
        # 6:unsupported、2～N次识别、有识别结果，asr_reject为1
        # 7:unsupported、2～N次识别、无识别结果，非网络错误
        # 8:unsupported、2～N次识别、无识别结果，网络错误
        # 9:首次识别
        with open(self.result_path, 'w', encoding='utf-8') as result_file:
            for query_name in asr_query:
                query = asr_query[query_name]
                if not 'unsupported' in query['desc']:
                    if 'first asr' in query['desc']:
                        self.first_success_count += 1
                    else:
                        self.ready_request_count += 1
                        if 'net_err' in query['desc']:
                            self.invalid_request_count += 1
                        else:
                            self.valid_request_count += 1
                            self.recg_query.update({query_name: query})
                            result_file.write(query_name + ':' + query['recg_result'] + '\n')
                            if query['recg_result'] != '':
                                self.asr_success_count += 1
                                if not 'asr reject' in query['desc']:
                                    self.asr_recall_count += 1
        result_file.close()

    def parse_rule_3(self, asr_query):
        """
            [规则3:纯识别] 排除掉网络错误码的情况
        """
        with open(self.result_path, 'w', encoding='utf-8') as result_file:
            for query_name in asr_query:
                query = asr_query[query_name]
                self.ready_request_count += 1
                if 'net_err' in query['desc']:
                    self.invalid_request_count += 1
                else:
                    self.valid_request_count += 1
                    self.recg_query.update({query_name: query})
                    result_file.write(query_name + ':' + query['recg_result'] + '\n')
                    if query['recg_result'] != '':
                        self.asr_success_count += 1
                        if not 'asr reject' in query['desc']:
                            self.asr_recall_count += 1
        result_file.close()

    def parse_rule_4(self, asr_query):
        """
            [规则4:声纹] 排除掉未唤醒、识别结果不是"我是谁"和没有tts的情况
        """
        #【声纹】dict描述（1参与判定准确率统计，2、3不参与）
        # {'pcm_name': 'jike-false_asr_speed_aj_1m_luqi', 'desc': 'tts回调内容', 'recg_result': '识别结果'}
        # 1:识别结果为'我是谁'，desc为非空
        # 2:识别结果不是'我是谁'
        # 3:desc为None
        for query_name in asr_query:
            query = asr_query[query_name]
            if not 'no wakeup' in query['desc']:
                self.ready_request_count += 1
                if 'net_err' in query['desc']:
                    self.invalid_request_count += 1
                else:
                    self.valid_request_count += 1
                    if query['recg_result']:
                        self.asr_success_count += 1
                        if query['recg_result'] == '我是谁' and \
                            ('集内:' in query['desc'] or '集外:' in query['desc']):
                            self.recg_query.update({query_name: query})


class InteractAccuracy(object):
    """Interact accuracy"""
    def __init__(self, test_info, recognize_result):
        """
            [双人交互识别率统计] 根据角色和识别query，统计角色准确率、识别率等指标
        Args:
            test_info : [list] 包含测试场景、测试集名称、测试版本信息
            recognize_result : [list] 识别结果详情
        Returns:
        """
        self.audio_scene, self.audio_name, self.sdk_version = test_info
        self.answer_dict = globalVal.get_scene_data(self.audio_scene + '/' + self.audio_name, 'answer')
        self.recognize_dict = recognize_result
        self.add_flag = '。'

    def get_interact_accuracy(self):
        """
            [性能统计] 计算角色准确率、识别率等指标
        Args:
            null
        Returns:
            result_json : [json]
        """
        total_role_recognize = {}
        right_role_answer = {}
        right_role_recognize = {}

        role_info, total_role_answer = self.get_interact_round()
        for query in self.answer_dict:
            ans = self.answer_dict[query]
            curr_role = str(ans['asr_role'])
            right_role = False
            tmp_answer = self.add_flag + ans['content']
            tmp_recognize = ''
            if query in self.recognize_dict:
                tmp_recognize = self.add_flag + self.recognize_dict[query]['recg_result']
                if curr_role == self.recognize_dict[query]['asr_role']:
                    right_role = True
            if curr_role in total_role_recognize:
                total_role_recognize[curr_role] += tmp_recognize
            else:
                if len(tmp_recognize) == 0:
                    total_role_recognize.update({curr_role: ''})
                else:
                    total_role_recognize.update({curr_role: tmp_recognize.split(self.add_flag, 1)[1]})
            if right_role:
                role_info[curr_role]['right_round'] += 1
                if curr_role in right_role_answer:
                    right_role_answer[curr_role] += tmp_answer
                    right_role_recognize[curr_role] += tmp_recognize
                else:
                    if len(tmp_recognize) == 0:
                        right_role_answer.update({curr_role: ''})
                        right_role_recognize.update({curr_role: ''})
                    else:
                        right_role_answer.update({curr_role: tmp_answer.split(self.add_flag, 1)[1]})
                        right_role_recognize.update({curr_role: tmp_recognize.split(self.add_flag, 1)[1]})

        acu_info, sum_wer = self.get_wer_result(
            total_role_answer, total_role_recognize, right_role_answer, right_role_recognize
        )
        return self.get_role_accuracy(role_info, acu_info, sum_wer)

    def get_interact_round(self):
        """
            [交互query合并] 将某个角色连续说的几句话合并成一句，构成形如A、B、A、B、A、B...的双人交互模式
        Args:
            answer_dict : [dict] 原始识别query标注答案，包含query内容、角色信息
        Returns:
            role : [int] 参与交互的人数(兼容不是双人交互的情况)
            total_role_answer : [string] 按A、B角色拆分后、拼接到一起的识别标注答案，用于wer计算字准
        """
        role = {}
        total_role_answer = {}

        for query in self.answer_dict:
            ans = self.answer_dict[query]
            curr_role = str(ans['asr_role'])
            if curr_role in total_role_answer:
                total_role_answer[curr_role] += self.add_flag + ans['content']
            else:
                total_role_answer.update({curr_role: ans['content']})
            if not curr_role in role:
                role.update({curr_role: {'total_round': 0, 'right_round': 0}})
            role[curr_role]['total_round'] += 1

        return role, total_role_answer

    def get_wer_result(self, total_role_answer, total_role_recognize, right_role_answer, right_role_recognize):
        """
            [结果记录] 将对齐前后的答案和结果记录入txt，用于wer计算识别准确率
        Args:
            total_role_answer : [list] 原始识别query标注答案，按A、B角色拆分
            total_role_recognize : [list] 云端返回的识别结果，按A、B角色拆分（不关注云端角色判断是否正确）
            total_answer : [list] 根据所有角色的total_role_answer得到，用于汇总整体的字准情况（不关注云端角色判断是否正确）
            total_recognize : [list] 根据所有角色的total_role_recognize得到
            right_role_answer : [list] 云端返回的识别结果，按A、B角色拆分（仅记录角色判断正确的回合）
            right_role_recognize : [list] 与right_role_result对应回合的标注答案
            right_answer : [list] 根据所有角色的right_role_answer得到，用于汇总角色判定正确的情况下、整体的字准情况
            right_recognize : [list] 根据所有角色的right_role_recognize得到
        Returns:
            acu_info : [list] 识别字准（按角色区分）
            sum_wer : [list] 识别字准（汇总情况，不区分角色）
        """
        acu_info = {}

        sample_set, txt_path = _init_txt_path(self.audio_scene, self.audio_name, self.sdk_version, total_role_answer)
        # [1] 不关注云端角色判断是否正确，记录query答案和识别结果（区分A、B角色）
        total_answer = txt_path['total_path']['sum']['answer']
        total_recognize = txt_path['total_path']['sum']['result']
        for role in total_role_answer:
            answer = txt_path['total_path'][role]['answer']
            recognize = txt_path['total_path'][role]['result']
            pcm_name = sample_set + '_role-' + str(role) + '.pcm:'
            _write_role_file(answer, pcm_name + total_role_answer[role])
            _write_role_file(recognize, pcm_name + total_role_recognize[role]) 
            _write_role_file(total_answer, pcm_name + total_role_answer[role])
            _write_role_file(total_recognize, pcm_name + total_role_recognize[role])
            acu_info.update({role: {'total_wer': cal_asr_wer(answer, recognize)[0]}})
        # [2] 将标注答案与云端结果一一对比后，记录角色判定正确的query答案和识别结果（区分A、B角色）
        right_answer = txt_path['right_path']['sum']['answer']
        right_recognize = txt_path['right_path']['sum']['result']
        for role in right_role_answer:
            answer = txt_path['right_path'][role]['answer']
            recognize = txt_path['right_path'][role]['result']
            pcm_name = sample_set + '_role-' + str(role) + '.pcm:'
            _write_role_file(answer, pcm_name + right_role_answer[role])
            _write_role_file(recognize, pcm_name + right_role_recognize[role]) 
            _write_role_file(right_answer, pcm_name + right_role_answer[role])
            _write_role_file(right_recognize, pcm_name + right_role_recognize[role])
            acu_info[role].update({'role_wer': cal_asr_wer(answer, recognize)[0]})
        # [3] 汇总整体的字准情况（total_wer：不区分角色， role_wer：区分A、B角色）
        sum_wer = {
            'role_wer': cal_asr_wer(right_answer, right_recognize)[0],
            'total_wer': cal_asr_wer(total_answer, total_recognize)[0]
        }

        return acu_info, sum_wer

    def get_role_accuracy(self, role_info, acu_info, sum_wer):
        """
            [准确率计算] 汇总角色判定准确率、识别率信息
        """
        sum_info = {'total_round': 0, 'right_round': 0}
        for role in role_info:
            for key in role_info[role]:
                sum_info[key] += role_info[role][key]
            role_info[role].update(_get_right_role_rate(role_info[role]))
            role_info[role].update(acu_info[role])
        sum_info.update(_get_right_role_rate(sum_info))
        sum_info.update(sum_wer)
        return {'sum_info': sum_info, 'role_info': role_info}


class WpDCIdataExtract(object):
    """
        [DCI第一轮灌测] DCI特征提取、多台设备组网
        Args:
            sampleset_name : [string] 测试集名称
            version_array : [dict] 测试版本_米数
        Returns:
            dci_json : [json] 格式为：{
                'DCI组合设备1': 组合结果1,
                'DCI组合设备2': 组合结果2,
                …
                'DCI组合设备N': 组合结果N
            }
            其中，
            DCI组合设备N 的格式为：测试版本1_1m+测试版本2_3m+测试版本3_5m
            组合结果N 的格式为：{
                'wp_query_count': 人工标注的唤醒总条数,
                'all_response_count': 全应答次数（同源场景下，1、3、5m设备全部被唤醒的次数）,
                'dci_group_count': DCI组网成功次数（在all response的基础上，1、3、5m设备的响应间隔在500ms以内，命中度秘组网成功策略的次数）
            }
    """
    def __init__(self, sampleset_name, version_array=[]):
        self.scene_name, self.audio_name = globalVal.get_scene_name(sampleset_name)
        self.dci_json = {}
        if len(version_array) < 2:
            logging.error('DCI组合设备数量小于2,请检查场景: %s, %s', self.scene_name, self.audio_name)
            globalVal.record_err(str(self.scene_name) + '/' + str(self.audio_name), 3201, 'DCI组合设备数量小于2')
            return
        else:
            # 得到版本组合判断
            self.dci_group = self.get_dci_group(version_array)
        for version_list in self.dci_group:
            group_info = ''
            for vers in version_list:
                group_info += '+' + vers
            self.version_num = len(version_list)
            self.save_path = globalVal.get_save_path(self.scene_name, self.audio_name)
            self.dci_data_intersect_path = os.path.join(
                self.save_path.split(self.audio_name)[0], self.audio_name + '_' + group_info[1:] + "_dci_data.txt")
            self.dci_data_path = []
            for version in version_list:
                sdk_v, distance = version.rsplit('_', 1)
                self.dci_data_path.append(os.path.join(self.save_path,
                    sdk_v + "_" + self.scene_name + '_' + self.audio_name + '_' + distance + "_wp_dci.txt"))
            self.dci_json.update({group_info[1:]: self.find_intersec_wakeup(self.scene_name + '_' + self.audio_name)})

    def get_result_json(self):
        """Return dci_json"""
        return self.dci_json

    def get_dci_group(self, version_array):
        """Compute responce device from distance"""
        group = {}
        dci_group = []
        for version in version_array:
            sdk_v, dis = version.rsplit('_', 1)
            if dis in group:
                group[dis].append(sdk_v)
            else:
                group.update({dis: [sdk_v]})
        for gp in product(*group.values()):
            idx = 0
            tmp = []
            for dis in group:
                tmp.append(gp[idx] + '_' + dis)
                idx += 1
            dci_group.append(tmp)
        return dci_group

    def get_answer_from_distance(self, result_dict):
        """Compute responce device from distance"""
        distance = 999
        answer = 0
        for version in range(self.version_num):
            ver_dis = int(list(filter(str.isdigit, result_dict[version]['device_distance']))[0])
            if 'nz' in self.scene_name:
                if str(ver_dis) in self.scene_name.split('_')[3].split('nz')[0]:
                    answer = version
                    return answer
            else:
                if ver_dis < distance:
                    distance = ver_dis
                    answer = version
        return answer

    def is_in_dci_range(self, response_time):
        """Check if satisfy the restrict of DCI_TIME_RESTRICT"""
        if abs(response_time[0] - response_time[-1]) < globalVal._PARAM['DCI_TIME_RESTRICT']:
            return True
        else:
            return False

    def find_intersec_wakeup(self, dci_audio):
        """Find supported intersection result for all sdk verion"""
        result_dict = {}
        total_wp_count = []
        result_json = {'wp_query_count': 0, 'all_response_count': 0, 'dci_group_count': 0}
        # 分别读取唤醒的标注答案和对齐结果
        for version in range(self.version_num):
            if os.path.exists(self.dci_data_intersect_path):
                os.remove(self.dci_data_intersect_path)
            result_dict[version] = {}
            if os.path.exists(self.dci_data_path[version]):
                with open(self.dci_data_path[version], 'r', encoding='utf-8') as result_file:
                    for line in result_file:
                        if 'total_wakeup_count' in line:
                            total_wp_count.append(line.split('\t')[0].split(':')[1])
                            result_dict[version]['device_distance'] = line.split('\t')[1].split(':')[1]
                            result_dict[version]['device_md5'] = line.split('\t')[2].split(':')[1].strip()
                            continue
                        query_index = line.split(':')[0]
                        result_dict[version][query_index + '_wpTime'] = int(line.split(':')[1])
                        result_dict[version][query_index] = line.split(':')[2].strip()
        # 根据场景，计算应该响应的设备
        response_device = self.get_answer_from_distance(result_dict)
        # 检查多台设备的唤醒query条数是否一致
        if len(set(total_wp_count)) != 1:
            logging.error('多台设备的唤醒条数不一致，请检查场景: %s, %s', self.scene_name, self.audio_name)
            globalVal.record_err(str(self.scene_name) + '/' + str(self.audio_name), 3202, '多台设备的唤醒条数不一致')
            return
        result_json['wp_query_count'] = total_wp_count[0]
        # 多台设备唤醒全应答，则汇总dci特征进行判定
        for query_num in range(int(total_wp_count[0])):
            query_index = str(dci_audio) + "_" + str(query_num) + ".pcm"
            response_time = []
            for version in range(self.version_num):
                if query_index in result_dict[version]:
                    response_time.append(result_dict[version][query_index + '_wpTime'])
            # 多台设备全应答、且满足DCI_TIME_RESTRICT时，进行dci特征汇总
            if len(response_time) == self.version_num:
                result_json['all_response_count'] += 1
                if not self.is_in_dci_range(sorted(response_time)):
                    logging.error('DCI组网失败，多台设备的唤醒速度差异过大，请检查场景: %s, %s', 
                        self.scene_name, self.audio_name)
                    globalVal.record_err(str(self.scene_name) + '/' + str(self.audio_name) + '/' + query_index, 
                        3203, 'DCI组网失败，多台设备的唤醒速度差异过大，' + str(response_time))
                result_json['dci_group_count'] += 1
                with open(self.dci_data_intersect_path, "a+", encoding='utf-8') as intersec_file:
                    intersec_file.write( \
                        "time:[" + str(response_device) + "]" + "\twakeup_index:" + str(query_num + 1) + "\n")
                    for version in range(self.version_num):
                        intersec_file.write( \
                            result_dict[version]['device_md5'] + ":" + result_dict[version][query_index] + "\n")
                    intersec_file.close()
        return result_json


class DciPerformanceParse():
    """
        DCI test round 2
        Get dci judge performance
    """

    def __init__(self):
        """
        参数初始化
        """
        self.dci_perform_array = {}

    def getDciJudgeResult(self, audioScene, log_path):
        """
        获取DCI判定准确率
        """
        success_count = 0
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as log_file:
                for line in log_file:
                    line = line.strip()
                    if line == "":
                        continue
                    answer = ""
                    result = ""
                    item = line.split('\t')
                    for content in item:
                        if 'dci_answer' in content:
                            answer = content.split(':')[1].strip()
                        if 'dci_result' in content:
                            result = content.split(':')[1].strip()
                    if answer == result:
                        success_count += 1
        else:
            logging.error("%s 文件不存在!", log_path)
        return success_count

    def dciPerformance(self, sampleset_name, log_path):
        """
        DCI性能统计函数
        """
        enviroment, audio_name, dci_group = globalVal.get_dci_info(sampleset_name)
        round1_data = globalVal.get_scene_data(os.path.join('jike-false_wp_dci_' + enviroment, audio_name))
        wp_query_count = 0
        all_response_count = 0
        dci_group_count = 0
        success_count = 0
        dci_success_rate = '0.0%'
        dci_accuracy_rate = '0.0%'
        if round1_data['dciinfo'][dci_group] is not None:
            wp_query_count = round1_data['dciinfo'][dci_group]['wp_query_count']
            all_response_count = round1_data['dciinfo'][dci_group]['all_response_count']
            dci_group_count = round1_data['dciinfo'][dci_group]['dci_group_count']
            success_count = self.getDciJudgeResult(sampleset_name, log_path)
        if wp_query_count > 0:
            dci_success_rate = str(round(float(success_count * 100) / float(wp_query_count), 3)) + "%"
        if dci_group_count > 0:
            dci_accuracy_rate = str(round(float(success_count * 100) / float(dci_group_count), 3)) + "%"
        result_summary = {
            '唤醒音频总条数': wp_query_count, 
            '唤醒全应答次数': all_response_count,
            'DCI组网成功次数': dci_group_count, 
            'DCI判决正确次数': success_count, 
            'DCI成功率': dci_success_rate,
            'DCI准确率': dci_accuracy_rate
        }
        if dci_group in self.dci_perform_array:
            if enviroment in self.dci_perform_array[dci_group]:
                self.dci_perform_array[dci_group][enviroment].update({audio_name: result_summary})
            else:
                self.dci_perform_array[dci_group].update({enviroment: {audio_name: result_summary}})
        else:
            self.dci_perform_array.update({dci_group: {enviroment: {audio_name: result_summary}}})

    def write_dci_data(self):
        """
        DCI数据表格
        """
        result_workbook = Workbook()
        result_workbook.remove(result_workbook['Sheet']) 
        result_worksheet = result_workbook.create_sheet('声学测试结论')
        row_count_list = [1]
        perform_feature = ['唤醒音频总条数', '唤醒全应答次数', 'DCI组网成功次数', 
            'DCI判决正确次数', 'DCI成功率', 'DCI准确率']
        for dci_group in self.dci_perform_array:
            col_count = 1
            start_row_count = max(row_count_list)
            row_count_list = []
            for enviroment in self.dci_perform_array[dci_group]:
                row_count = start_row_count + 2
                xls.write_content(result_worksheet, [start_row_count, start_row_count + 1],
                    col_count, enviroment, 9)
                xls.write_content(result_worksheet, [start_row_count, start_row_count],
                    [col_count + 1, col_count + 6], dci_group, 1)
                for index in range(len(perform_feature)):
                    xls.write_content(result_worksheet, start_row_count + 1, col_count + index + 1, 
                        perform_feature[index], 3)
                total_query = 0
                total_response = 0
                total_dci = 0
                total_success = 0
                for audio_name in self.dci_perform_array[dci_group][enviroment]:
                    xls.write_content(result_worksheet, row_count, col_count, audio_name, 3)
                    index = -0
                    features = self.dci_perform_array[dci_group][enviroment][audio_name]
                    total_query += int(features['唤醒音频总条数'])
                    total_response += int(features['唤醒全应答次数'])
                    total_dci += int(features['DCI组网成功次数'])
                    total_success += int(features['DCI判决正确次数'])
                    for feature in perform_feature:
                        index += 1
                        xls.write_content(result_worksheet, row_count, col_count + index, features[feature])
                    row_count += 1
                xls.write_content(result_worksheet, row_count, col_count, '汇总', 1)
                xls.write_content(result_worksheet, row_count, col_count + 1, total_query)
                xls.write_content(result_worksheet, row_count, col_count + 2, total_response)
                xls.write_content(result_worksheet, row_count, col_count + 3, total_dci)
                xls.write_content(result_worksheet, row_count, col_count + 4, total_success)
                if total_query > 0:
                    xls.write_content(result_worksheet, row_count, col_count + 5, 
                        str(round(float(total_success * 100) / float(total_query), 3)) + "%")
                if total_response > 0:
                    xls.write_content(result_worksheet, row_count, col_count + 6, 
                        str(round(float(total_success * 100) / float(total_response), 3)) + "%")
                col_count += len(perform_feature) + 2
                row_count_list.append(row_count + 3)
        result_workbook.save(os.path.join(globalVal._WORK_DIRECTORY, 'dci_perform.xlsx'))


# Private function

def _semantics_accuracy(answer_result, recognize_result, total_count):
    """
    计算语义准确率
    """
    answer = _read_file_content(answer_result, ':')
    recognize = _read_file_content(recognize_result, ':')
    intersec_query = set(answer.keys()).intersection(set(recognize.keys()))
    right_count = 0
    for query_name in intersec_query:
        if answer[query_name].split('#')[1] == recognize[query_name].split('#')[0]:
            right_count += 1
    accuracy = "%.3f%%" % float(right_count  * 100 / total_count)
    return accuracy, str(total_count - right_count)


def _get_wer_from_file(path, key):
    """
    指定path路径下，寻找名称中包含 key 的值
    """
    f = open(path, 'r', encoding='utf-8')
    content = f.readlines()
    for line in content[len(content)-10:]:
        if key in line:
            if 'ACU' in key:
                return '%.3f%%' % float(line.strip().split(' ')[1].split('%')[0])
            elif 'ERR' in key:
                return line
            else:
                return None 


def _location_unify(location):
    """唤醒声源定位:角度归一化
    """
    if location > 360:
        return location - 360
    elif location < 0:
        return location + 360
    else:
        return location


def _write_role_file(file_path, content):
    """
        [txt写入] 识别结果和答案写入txt文件
    """
    if '_role-' in file_path:
        with open(file_path, 'a+') as f:
            f.write(content + '\n')
        f.close()
    else:
        with open(file_path, 'w') as f:
            f.write(content + '\n')
        f.close()


def _update_role_count(curr_info, new_info):
    """
        [性能汇总]叠加right_round、total_round
    """
    curr_info['right_count'] += new_info['right_count']
    curr_info['total_count'] += new_info['total_count']


def _init_txt_path(audio_scene, audio_name, sdk_version, role_info):
    """
        [路径初始化] 用于wer计算的answer和result路径
    """
    if '/' in audio_scene:
        audio_scene = audio_scene.split('/')[0]
    if audio_name == '':
        sample_set = audio_scene
    else:
        sample_set = audio_scene + '_' + audio_name
    dir = globalVal.get_save_path(audio_scene, audio_name)
    prefix = sdk_version + '_' + sample_set + '_'
    suffix = '.txt'

    txt_path = {
        'total_path' : {
            'sum': {
                'answer': os.path.join(dir, prefix + 'total_answer' + suffix),
                'result': os.path.join(dir, prefix + 'total_recognize' + suffix)
            }
        }, 
        'right_path': {
            'sum': {
                'answer': os.path.join(dir, prefix + 'right_answer' + suffix),
                'result': os.path.join(dir, prefix + 'right_recognize' + suffix)
            }
        }
    }
    for role in role_info:
        txt_path['total_path'].update({
            str(role): {
                'answer': os.path.join(dir, prefix + 'total_answer_role-' + str(role) + suffix),
                'result': os.path.join(dir, prefix + 'total_recognize_role-' + str(role) + suffix)
            }
        })
        txt_path['right_path'].update({
            str(role): {
                'answer': os.path.join(dir, prefix + 'right_answer_role-' + str(role) + suffix),
                'result': os.path.join(dir, prefix + 'right_recognize_role-' + str(role) + suffix)
            }
        })

    return sample_set, txt_path


def _get_right_role_rate(role_info):
    """
        [角色准确率计算]
    Args:
        role_info : [dict] 角色信息，包含对话轮数、角色正确轮数、对话query条数、角色正确query条数
    Returns:
        round_rate : [string] 角色判定准确率(基于双人交互轮数)，用于准出（单位%）
        query_rate : [string] 角色判定准确率(基于query条数)，该指标受标注人员因素影响、仅供参考（单位%）
    """
    round_rate = '0.0%'
    if role_info['total_round'] > 0:
        round_rate = "%.3f%%" % \
            (float(role_info['right_round']) / float(role_info['total_round']) * 100)
    return {'round_rate': round_rate}
        

# Public function

def _update_role_perf(audio_scene, sdk_version, curr_info):
    """
        [性能计算] 重新计算角色准确率、字准
    """
    sample_set, txt_path = _init_txt_path(audio_scene, '', sdk_version, curr_info['role_info'])
    for role in list(curr_info['role_info'].keys()) + ['sum']:
        if role == 'sum':
            role_info = curr_info['sum_info']
        else:
            role_info = curr_info['role_info'][role]
        role_info.update(_get_right_role_rate(role_info))
        answer = txt_path['right_path'][role]['answer']
        recognize = txt_path['right_path'][role]['result']
        role_info.update(({'role_wer': cal_asr_wer(answer, recognize)[0]}))
        answer = txt_path['total_path'][role]['answer']
        recognize = txt_path['total_path'][role]['result']
        role_info.update(({'total_wer': cal_asr_wer(answer, recognize)[0]}))


def _update_role_info(audio_scene, audio_name, sdk_version, curr_info, new_info):
    """
        [性能汇总]
    """
    # [1] 叠加right_round、total_round
    if 'role_info' in new_info:
        for role in new_info['role_info']:
            if not role in new_info['role_info']:
                continue
            if role in curr_info['role_info']:
                curr_info['role_info'].update({'role': copy.deepcopy(new_info['role_info'][role])})
            else:
                _update_role_count(curr_info['role_info'][role], new_info['role_info'][role])
        _update_role_count(curr_info['sum_info'], new_info['sum_info'])
    # [2] 单集合的答案和识别结果、拷贝到对应场景下
    sample_set, txt_path = _init_txt_path(audio_scene, audio_name, sdk_version, curr_info['role_info'])
    for role in list(curr_info['role_info'].keys()) + ['sum']:
        _merge_txt_file_for_wer(txt_path['total_path'][role]['answer'], audio_name)
        _merge_txt_file_for_wer(txt_path['total_path'][role]['result'], audio_name)
        _merge_txt_file_for_wer(txt_path['right_path'][role]['answer'], audio_name)
        _merge_txt_file_for_wer(txt_path['right_path'][role]['result'], audio_name)


def _merge_txt_file_for_wer(in_file, audio_name):
    """
        [性能汇总]answer.txt/result.txt按场景叠加
    """
    out_file = _update_file_path(in_file, audio_name)
    with open(out_file, 'a+', encoding='utf-8') as out_f:
        for line in open(in_file, 'r', encoding='utf-8'):
            out_f.writelines(line)
    out_f.close()
    

def _file_search(path, key, suffix):
    """
    指定path路径下，寻找名称中包含 key 和 suffix 的特征值文件
    """
    for root, dirs, files in os.walk(path):
        for filename in files:
            if suffix in filename and key in filename:
                root = str(root)
                file_name = os.path.join(root, filename)
                if os.path.exists(file_name):
                    return file_name
    return -1


def _read_file_content(file_name, split_str):
    """
    读取txt，每一行按split_str分割成key和value，并保存入dict
    """
    f = open(file_name, encoding='utf-8')
    result = {}
    for line in f.read().split('\n'):
        item = line.split(split_str)
        if len(item) == 2:
            result.update({item[0]: item[1]})
    return result


def _update_file_path(in_file, audio_name):
    """
        [路径替换] 从单个音频集路径，得到单个测试场景的路径
    Args:
        in_file : [string] 原始路径
        audio_name : [string] 要过滤的音频集名称
    Returns:
        out_file : [string] 更新路径
    """
    out_file = in_file
    if audio_name != '':
        if '_' + audio_name in out_file:
            out_file = out_file.replace('_' + audio_name, '')
        if audio_name in out_file:
            out_file = out_file.replace(audio_name, '')
    return out_file


def _get_mean(list_data):
    """得到列表均值"""
    if len(list_data):
        return np.mean(list_data)
    else:
        return 0


def _not_empty(s):
    """去掉列表的空元素"""
    return s and s.strip()
