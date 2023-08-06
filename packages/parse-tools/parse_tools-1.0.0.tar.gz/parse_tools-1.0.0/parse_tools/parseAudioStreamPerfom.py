#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: parseAudioStreamPerform.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date:   2019/03/07 上午10:31
"""

import os
import shutil
import subprocess
import logging
import json
import shelve
import signal
import platform
import importlib, sys
importlib.reload(sys)

import globalVal
import db_manager
import get_scene_report
import stream_perform_parse
import manual_perform_parse
import speech_parse
import time


def abortSys(sig, stack_frame):
    """
        检测到停止信号时，删除已生成的信息，并退出
    """
    logging.error('Capture signal, exit %d, %s', sig, stack_frame)
    os.system('rm -rf ' + globalVal._WORK_DIRECTORY)
    exit(2)


class PerformanceThread():
    """
        [灌测性能统计] 端到端声学灌测性能自动统计工具
    Args:
        answer_result_file_path : [string] 输出结果列表文件
    Returns:
        output: result目录
    """

    def __init__(self, output_dir='', dci_dir='', conf_path='', script_dir=''):
        """
            输入参数解析&初始化
        """
        self._split = ':'
        globalVal._ENVIRONMENT = platform.system()
        if globalVal._ENVIRONMENT == 'Windows':
            self._split = '#'
        if output_dir != '':
            globalVal._WORK_DIRECTORY = output_dir
        # if os.path.exists(globalVal._WORK_DIRECTORY):
        #     shutil.rmtree(globalVal._WORK_DIRECTORY)
        globalVal.update_global_value(dci_dir, conf_path, script_dir)
        if len(globalVal._VERSION_LIST) == 0:
            self._version_flag = True
        else:
            self._version_flag = False

        if not os.path.exists(globalVal._WORK_DIRECTORY):
            os.mkdir(globalVal._WORK_DIRECTORY)

    def get_performance(self, answer_result_file_path):
        """
            开始性能数据统计
        """
        if not os.path.exists(answer_result_file_path):
            logging.error('请检查输入, 找不到%s', answer_result_file_path)
            globalVal.record_err(answer_result_file_path, 1101, '请检查路径, 找不到该文件', 2)
        else:
            if answer_result_file_path.endswith('.json'):
                globalVal._MANUAL_TEST_MODE = True
                globalVal._R_WAKEUP_LIST = ['唤醒音频总条数', '唤醒成功次数', '唤醒率', '误唤醒次数']
                self.processManualData(answer_result_file_path)
                globalVal.save_result()
            else:
                self.ProcessStreamData(answer_result_file_path)
                globalVal.save_result()
        # try:
        #     if not os.path.exists(answer_result_file_path):
        #         logging.error('请检查输入, 找不到%s', answer_result_file_path)
        #         globalVal.record_err(answer_result_file_path, 1101, '请检查路径, 找不到该文件', 2)
        #     else:
        #         self.ProcessStreamData(answer_result_file_path)
        #         globalVal.save_result()
        # except BaseException as e:
        #     globalVal.record_err("parseAudioStreamPerfom.py ", 4301, '捕获到特殊异常:' + str(e), 2)
        return globalVal._RESULT_FLAG

    def processManualData(self, answer_result_file_path):
        """
            [人工数据处理] 
        """
        # [0] read manual_info files
        data = open(answer_result_file_path, 'r', encoding='utf-8')
        manual_data_list = json.load(data)
        data.close()
        stream_data_list = []
        for manual_data in manual_data_list:
            stream_data_list.append(manual_data['sdk_version'] + ':' + manual_data['sample_set'])
        # [1] task assignment
        # 读入数据库
        __DATABASE = shelve.open(globalVal._DATABASE_NAME)
        for key in __DATABASE:
            globalVal._DATABASE.update({key: __DATABASE[key]})
        __DATABASE.close()
        # 增量数据统计
        globalVal._NEW_DICT, new_data_list = self.record_info_check(stream_data_list)
        curr_work_dir = os.getcwd()
        os.chdir(os.path.dirname(answer_result_file_path))
        for manual_data in manual_data_list:
            version_info = manual_data['sdk_version'] + ':' + manual_data['sample_set']
            if version_info in new_data_list:
                newpro = manual_perform_parse.ManualProcessThread(manual_data)
                newpro.parse_data()
        os.chdir(curr_work_dir)
        get_scene_report.GetStreamReport()
        # 更新数据库
        __DATABASE = shelve.open(globalVal._DATABASE_NAME)
        for key in globalVal._DATABASE:
            __DATABASE[key] = globalVal._DATABASE[key]
        __DATABASE.close()

    def ProcessStreamData(self, answer_result_file_path):
        """
            [灌测数据处理] 根据传入文件列数进行判定:DCI决策、唤醒&识别、声纹
        """
        # [0] read stream_info files
        stream_data_list = samplename_process_for_tmp(answer_result_file_path, self._split)

        # [1] task assignment
        if not len(stream_data_list):
            logging.error('%s 未检测到有效信息, 已退出!', answer_result_file_path)
            globalVal.record_err(answer_result_file_path, 1001, "未检测到有效信息, 本次统计无效", 2)
            return
        
        if len(stream_data_list[0].split(self._split)) == 2:
            round1_db = os.path.join(globalVal._DCI_AUDIO_WORK_PATH, 'stream_data')
            if os.path.exists(round1_db) or os.path.exists(round1_db + '.db'):
                # 读入DCI第一轮灌测数据库
                __DATABASE = shelve.open(round1_db)
                for key in __DATABASE:
                    globalVal._DATABASE.update({key: __DATABASE[key]})
                __DATABASE.close()
                # DCI第二轮灌测数据统计
                dci_thread = speech_parse.DciPerformanceParse()
                for line in stream_data_list:
                    item = line.split(self._split)
                    dci_thread.dciPerformance(item[0], item[1])
                dci_thread.write_dci_data()
            else:
                globalVal.record_err(globalVal._DCI_AUDIO_WORK_PATH, 1105, '请检查路径，找不到DCI第一轮灌测数据', 2)
                return
        else:
            # 读入数据库
            __DATABASE = shelve.open(globalVal._DATABASE_NAME)
            for key in __DATABASE:
                globalVal._DATABASE.update({key: __DATABASE[key]})
            __DATABASE.close()
            # 增量数据统计
            globalVal._NEW_DICT, new_data_list = self.record_info_check(stream_data_list)
            for line in new_data_list:
                item = line.split(self._split)
                if len(item) > 4:
                    newpro = stream_perform_parse.SpeechParseThread(item)
                    newpro.read_messages(item[3], item[4], item[2])
                    newpro.process_data()
            get_scene_report.GetStreamReport()
            # 更新数据库
            __DATABASE = shelve.open(globalVal._DATABASE_NAME)
            for key in globalVal._DATABASE:
                __DATABASE[key] = globalVal._DATABASE[key]
            __DATABASE.close()
            

    def record_info_check(self, stream_data_list):
        """
            [增量检查] 根据数据库中的信息，检查确认是否新增
        Args:
            stream_data_list : [list] 灌测信息结果列表
        Returns:
            info_dict : [dict] 全局增量统计信息
            new_data_list : [list] 新增集合/版本的测试列表
        """
        new_data_list = []

        # [1] 增量统计信息检查
        for line in stream_data_list:
            sdk_version, sampleset_name = line.split(self._split)[0:2]
            # 当未使用 -c 参数 指定版本时，根据灌测信息结果列表内容，记录SDK版本至globalVal._VERSION_LIST
            audio_scene = globalVal.get_scene_name(sampleset_name)[0]
            audio_type = audio_scene.split('_')[1]
            if audio_type in globalVal._SAMPLE_LIST:
                if not audio_scene in globalVal._SAMPLE_LIST[audio_type]:
                    globalVal._SAMPLE_LIST[audio_type].append(audio_scene)
            else:
                globalVal._SAMPLE_LIST.update({audio_type: [audio_scene]})
            if self._version_flag and sdk_version not in globalVal._VERSION_LIST:
                globalVal._VERSION_LIST.append(sdk_version)

            # 增量统计信息检查
            flags = db_manager.check_version_exsit(sampleset_name, sdk_version)
            if flags == 3:
                # 数据库中已存在时，直接跳过
                continue
            else:
                new_data_list.append(line)

        # [2] 更新全局增量统计信息
        info_dict = {}
        for line in new_data_list:
            sdk_version, sampleset_name = line.split(self._split)[0:2]
            scene_name, audio_name, distance, md5 = globalVal.get_scene_info(sampleset_name)
            if md5 is not None:
                sdk_version += '_' + distance
            if scene_name in info_dict:
                if audio_name in info_dict[scene_name]:
                    info_dict[scene_name][audio_name].update({sdk_version: True})
                else:
                    info_dict[scene_name].update({audio_name: {sdk_version: True}})
            else:
                info_dict.update({scene_name: {audio_name: {sdk_version: True}}})
        
        return info_dict, new_data_list


def samplename_process_for_tmp(answer_result_file_path, split_str):
    """
        测试集命名临时处理，用于新、老版本过渡
    """
    stream_data_list = []
    with open(answer_result_file_path, 'r', encoding='utf-8') as conf_file:
        for line in conf_file:
            line = line.strip()
            leng = len(line.split(split_str))
            if line.startswith('#') or not (leng == 2 or leng == 5 or leng == 6):
                continue
            ##### 测试集命名临时处理 1013
            if leng == 2:
                sample_name = line.split(split_str)[0]
            else:
                sample_name = line.split(split_str)[1]
            if not '/' in sample_name:
                if leng == 2:
                    leng = len(sample_name.split('_'))
                    if leng < 5:
                        globalVal.record_err(sample_name, 1103, '请检查测试集命名，不符合规范', 2)
                        return
                    new_name = sample_name.rsplit('_', leng - 4)[0] + '/' + sample_name.split('_', 4)[-1]
                else:
                    leng = len(sample_name.split('_'))
                    if leng < 6:
                        globalVal.record_err(sample_name, 1103, '请检查测试集命名，不符合规范', 2)
                        return
                    new_name = sample_name.rsplit('_', leng - 5)[0] + '/' + sample_name.split('_', 5)[-1]
            else:
                if len(sample_name.split('/')[0].split('_')) < 5:
                    globalVal.record_err(sample_name, 1103, '请检查测试集命名，不符合规范', 2)
                    return
                new_name = sample_name
            if 'voiceprint' in line.split(split_str)[1]:
                item = line.split(split_str)
                if len(item) < 6:
                    globalVal.record_err(item[1], 1102, '声纹性能统计，缺少vpID!', 2)
                    return
                if item[5].split('&')[0] == 'NULL' or item[5].split('&')[0] == 'null':
                    new_name = new_name.replace('voiceprint', 'voiceprint-jw')
                else:
                    new_name = new_name.replace('voiceprint', 'voiceprint-jn')
            if len(line.split(split_str)) == 2:
                new_line = new_name + split_str + line.split(split_str)[1]
            else:
                new_line = line.split(split_str)[0] + split_str + new_name + split_str + line.split(split_str, 2)[2]
            stream_data_list.append(new_line)
            ##### 
    return stream_data_list


if __name__ == '__main__':
    """性能统计工具
    input:  answer_result_file_path
    output: result目录
    """
    if len(sys.argv) < 2:
        logging.error('python ' + sys.argv[0] + ' answer_result_file_path config_path')
        globalVal._ERR_JSON_FILE_NAME = os.path.join(globalVal._WORK_DIRECTORY, 'error_info.txt')
        if not os.path.exists(globalVal._WORK_DIRECTORY):
            os.mkdir(globalVal._WORK_DIRECTORY)
        globalVal.record_err(sys.argv[0], 1003, '脚本调用方式不正确', 2)
        exit(2)
    else:
        work_path, dci_work_dir, conf_path = globalVal.parse_args(sys.argv[2:])

    signal.signal(signal.SIGINT, abortSys)
    start = time.time()
    perfThread = PerformanceThread(work_path, dci_work_dir, conf_path, sys.argv[0])
    flags = perfThread.get_performance(sys.argv[1])
    end = time.time()
    print("total Execution Time: ", end - start)
    exit(flags)
    