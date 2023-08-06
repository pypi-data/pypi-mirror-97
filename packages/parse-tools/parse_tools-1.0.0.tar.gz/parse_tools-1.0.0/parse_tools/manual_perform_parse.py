#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: manual_perform_parse.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date: 2021/03/01 上午10:57
"""

import os
import copy
import shutil
import logging
from openpyxl import Workbook

import globalVal
import speech_parse
import db_manager


class ManualProcessThread():
    """
        人工测试数据汇总和分析
    """

    def __init__(self, json_data):
        """
            json数据解析&初始化
        """
        self.__initSceneName = json_data['sample_set']
        self.__audioScene, self.__audioName = self.__initSceneName.split('/')
        self.__samplesetName = self.__audioScene + '_' + self.__audioName
        self.__sdkVersion = json_data['sdk_version']
        self.__json_data = json_data['performance']
        self.__queryResultDict = {}
        self.__savePath = globalVal.get_save_path(self.__audioScene, self.__audioName)
        if not os.path.exists(self.__savePath):
            os.makedirs(self.__savePath)
        _update_Info(self.__audioScene)
        

    def parse_data(self):
        """
            唤醒、识别性能数据读取，识别准确率计算
        """ 
        # [0] 性能指标初始化
        perform_data = self.init_perform_data()
        # [1.1] 唤醒性能数据读取
        wp_status = {'summary': copy.deepcopy(globalVal._WP_DICT)}
        false_wp = {'summary': 0}
        if 'wakeup' in self.__json_data:
            for wp_words in self.__json_data['wakeup']:
                wp_data = self.__json_data['wakeup'][wp_words]
                wp_status.update({wp_words: copy.deepcopy(globalVal._WP_DICT)})
                wp_status[wp_words]['queryCount'] = wp_data['wp_query_count']
                wp_status[wp_words]['detectCount'] = wp_data['wp_triggered_count']
                wp_status[wp_words]['rightWordCount'] = wp_data['wp_triggered_count']
                if wp_data['wp_false_count'] > 0:
                    false_wp.update({wp_words: wp_data['wp_false_count']})
        # [1.2] 唤醒性能数据计算
        speech_parse.cal_wp_performance(wp_status, false_wp)
        perform_data.update({
            'wp_query_count': wp_status['summary']['queryCount'],
            'wp_count': wp_status['summary']['detectCount'],
            'false_wp_count': false_wp['summary'],
            'wp_status': wp_status,
            'wp_false': false_wp
        })
        if perform_data['wp_query_count'] > 0:
            perform_data.update({
                'wp_rate': "%.3f%%" % float(perform_data['wp_count'] * 100 / perform_data['wp_query_count'])
            })
        # [2] 识别性能数据计算
        if 'asr' in self.__json_data:
            self.__asr_answer_file_name = os.path.join(
                self.__savePath, self.__samplesetName + '_answer_result.txt')
            self.__rec_result_file_name = os.path.join(
                self.__savePath, self.__sdkVersion + '_' + self.__samplesetName + '_recognize_result.txt')
            asr_success_count = _process_answer_file(
                self.__json_data['asr']['answer_path'], self.__asr_answer_file_name,
                self.__audioScene, self.__audioName)
            self.__queryResultDict = _process_result_file(
                self.__json_data['asr']['recognize_path'], self.__samplesetName)
            query_class = speech_parse.QueryFilter(self.__initSceneName, self.__sdkVersion)
            recog_query, count_list = query_class.parse_asr_query(self.__queryResultDict)
            asr_query_count = perform_data['wp_query_count']
            asr_ready_count = asr_query_count - self.__json_data['asr']['ignore_count']
            asr_valid_count = asr_ready_count # 后续可去掉网络错误码个数
            asr_invalid_count = count_list[1]
            wer, ser, err = speech_parse.cal_asr_wer(self.__asr_answer_file_name, self.__rec_result_file_name)
            perform_data.update({
                'asr_query_count': asr_query_count,
                'asr_count': asr_ready_count,
                'valid_asr_request_count': asr_valid_count,
                'invalid_asr_request_count': asr_invalid_count,
                'success_count': asr_success_count,
                'success_rate': "%.3f%%" % float(asr_success_count * 100 / asr_valid_count),
                'asr_error_code_info': {
                    '唤醒后首次识别错误码': speech_parse.parse_asr_err(
                        self.__json_data['asr']['err_code'], perform_data['wp_query_count'])
                },
                'wer': wer,
                'ser': ser,
                'err': err
            })
            if asr_success_count != count_list[3] or asr_invalid_count != 0:
                logging.error('%s %s 识别答案和结果行数不一致！', self.__sdkVersion, self.__samplesetName)
                globalVal.record_err(self.__sdkVersion + '/' + self.__samplesetName, 3101, '识别答案和结果行数不一致！')

        db_manager.updateDataToDB(self.__initSceneName, self.__sdkVersion, 'query_result', self.__queryResultDict)
        db_manager.updateDataToDB(self.__initSceneName, self.__sdkVersion, 'recognize_result', recog_query)
        db_manager.updateDataToDB(self.__initSceneName, self.__sdkVersion, 'conclusion', perform_data)
        

    def init_perform_data(self):
        """
            性能指标默认值
        """
        query_result = {
            'wp_mode': 0,
            'wp_query_count': 0,
            'wp_count': 0,
            'wp_rate': '0.0%',
            'wp_time': 0,
            'false_wp_count': 0,
            'wp_status': {},
            'wp_false': {},
            'asr_query_count': 0,
            'asr_count': 0,
            'invalid_asr_request_count': 0,
            'valid_asr_request_count': 0,
            'success_count': 0,
            'success_rate': '0.0%',
            'recall_count': 0,
            'recall_rate': '0.0%',
            'false_asr_count': 0,
            'false_interact_count': 0,
            'first_success_count': 0,
            'ignore_asr_count': 0,
            'asr_error_code_info': {},
            'wer': '0.0%',
            'ser': '0.0%',
            'err': [],
            'partial_time': 0,
            'finish_time': 0,
            'tts_time': 0,
            'speed_query_num': 0,
            'asr_speed_list': {
                'partial_speed': [],
                'tts_speed': [],
                'finish_speed': []
            }
        }
        return query_result


def _process_answer_file(file_path, new_file, audio_scene, audio_name):
    """
        [识别标注答案文件处理] 读取音频条数；当query无编号时，需要以"音频名_编号.pcm"的格式添加编号，并记入new_file
    Args:
        file_path : [string] txt文件地址，每行以 "音频名称_编号.pcm:query内容"、或 "query内容" 格式存储
        new_file : [string] 统一处理后的txt文件存储至result目录下，用于wer进行识别率计算
        audio_scene : [string] 测试场景名称
        audio_name : [string] 测试集名称
    Returns:
        query_count : [int] 文件行数，即识别query条数
    """
    if os.path.exists(file_path):
        f = open(file_path, 'r', encoding='utf-8')
        query_list = {}
        idx = 0
        for line in f.readlines():
            idx += 1
            if '.pcm:' in line:
                item = line.strip().split(':')
                query_list.update({item[0]: {'content': item[1]}})
            else:
                query_list.update({
                    audio_scene + '_' + audio_name + '_' + str(idx) + '.pcm': {
                        'content': line.strip()
                    }
                })
        f.close()
        # record to txt
        with open(new_file, 'w') as f:
            for query_name in query_list:
                f.write(str(query_name) + ':' + str(query_list[query_name]['content']) + '\n')
        f.close()
        db_manager.updateDataToDB(audio_scene + '/' + audio_name, '', 'answer', query_list)
        return globalVal.get_row_count_of_txtfile(new_file)
    else:
        return 0


def _process_result_file(file_path, sample_set):
    """
        [识别结果文件处理] 读取 识别结果
    Args:
        file_path : [string] txt文件地址，每行以 "音频名称_编号.pcm:query内容"、或 "query内容" 格式存储
        sample_set : [string] 音频集名称
    Returns:
        query_result : [dict] 识别结果列表
    """
    query_result = {}
    if os.path.exists(file_path):
        f = open(file_path, 'r', encoding='utf-8')
        idx = 0
        for line in f.readlines():
            idx += 1
            asr_sn = None
            asr_corpus_id = None
            if len(line.strip()) == 0:
                continue
            item = line.strip().split(':')
            if len(item) == 1:
                query_name = sample_set + '_' + str(idx) + '.pcm'
                query_content = line.strip()
            elif len(item) == 4:
                query_name, query_content, asr_sn, asr_corpus_id = item
            elif len(item) >= 2:
                query_name, query_content = item
            query_result.update({
                query_name: {
                    'desc': '',
                    'recg_result': query_content,
                    'sn': asr_sn,
                    'corpus_id': asr_corpus_id,
                    'asr_role': None
                }
            })
        f.close()

    return query_result


def _update_Info(audio_scene):
    """
        [excel初始化] 按场景进行excel初始化
    Args:
        audio_scene : [string] 测试场景名称
    Returns:
        null
    """
    workbook_path = os.path.join(globalVal._WORK_DIRECTORY, audio_scene + '.xlsx')
    if not workbook_path in globalVal._WORKBOOK_DICT:
        wb = Workbook()
        wb.remove(wb['Sheet'])
        globalVal._WORKBOOK_DICT.update({workbook_path:wb})
