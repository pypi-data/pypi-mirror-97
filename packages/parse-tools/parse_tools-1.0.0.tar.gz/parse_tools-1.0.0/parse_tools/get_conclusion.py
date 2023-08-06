#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: get_conclusion.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date: 2021/01/21 下午20:40
"""

import os

import globalVal


_CONTENT = ""
_CONCLUSION_DESC = {
    'jike': {
        'jike-true': '极客模式',
        'jike-false': '非极客模式'
    },
    'normal_type': {
        'wp_true': '常规唤醒',
        'wp_first': '首次唤醒',
        'wp_false': '误唤醒',
        'wp_dci': 'DCI',
        'wp_location': '声源定位',
        'asr_oneshot': '单次oneshot识别',
        'asr_nooneshot': '单次非oneshot识别',
        'offlineasr_oneshot': '离线单次oneshot识别',
        'offlineasr_nooneshot': '离线单次非oneshot识别',
        'mutiplyasr_true': '多次识别',
    },
    'speech_type': {
        'wp': '唤醒',
        'voiceprint-jn': '声纹(集内)',
        'voiceprint-jw': '声纹(集外)',
        'asr': '单次识别',
        'mutiplyasr': '多次识别',
        'offlineasr': '离线识别',
        'pureasr': '纯识别',
        'roleasr': '双人交互识别',
        'semanticasr': '语义识别',
        'splitasr': '单条音频识别'
    },
    'test_type': {
        'true': '常规',
        'first': '首次',
        'false': '误报',
        'location': '声源定位',
        'whisper': '轻问轻答',
        'speed': '速度',
        'circle': '转圈',
        'nooneshot': '非oneshot'
    }
}
_SCENE_DESC = {
    'aj': '安静',
    'anjing': '安静',
    'wz': '外噪',
    'waizao': '外噪',
    'wz65db': '外噪65db',
    'wz75db': '外噪75db',
    'nz': '内噪',
    'neizao': '内噪',
    'nz70db': '内噪70db',
    'nz75db': '内噪75db',
    'nz85db': '内噪85db',
    'nzmax': '内噪最大音量',
    'wz65db+nz75db': '外噪65db+nz85db',
    'kws': '指令词'
}
_PARAM_DESC = {
    'WP_RATE': '唤醒率',
    'FALSE_WP': '误唤醒',
    'ASR_SUCCESS_RATE': '识别成功率',
    'ASR_RECALL_RATE': '召回率',
    'FALSE_ASR': '误识别',
    'ASR_WER': '字准',
    'ASR_SER': '句准',
    'VP_RIGHT_RATE': '正确判定率',
    'VP_WRONG_RATE': '错误判定率',
    'VP_UNRECG_RATE': '未识别率'
}

def col_match(curr_type):
    if curr_type in _SCENE_DESC:
        return _SCENE_DESC[curr_type]
    else:
        for key in _CONCLUSION_DESC:
            for type in _CONCLUSION_DESC[key]:
                if type == curr_type:
                    return _CONCLUSION_DESC[key][type]
        return curr_type


def type_match(key, curr_type):
    """测试类型中英文映射"""
    for type in _CONCLUSION_DESC[key]:
        if type == curr_type:
            return _CONCLUSION_DESC[key][type]
    return curr_type


def scene_mapping(scene_name):
    """测试场景中英文映射"""

    jike_mode, speech_type, test_type, scene, distance = scene_name.split('_', 5)[:5]
    # 1、如果是单次识别测试，增加极客模式类型描述
    if 'asr' == speech_type:
        new_scene = _CONCLUSION_DESC['jike'][jike_mode]
    else:
        new_scene = ''
    # 2、测试类型转换
    if speech_type + '_' + test_type in _CONCLUSION_DESC['normal_type']:
        new_scene += _CONCLUSION_DESC['normal_type'][speech_type + '_' + test_type]
    else:
        new_scene += type_match('speech_type', speech_type)
        new_scene += type_match('test_type', test_type)
    # 3、如果是单次识别测试，加上极客模式类型
    if scene in _SCENE_DESC:
        new_scene += ' ' + _SCENE_DESC[scene]
    else:
        new_scene += ' ' + scene
    if distance in _SCENE_DESC:
        new_scene += ' ' + _SCENE_DESC[distance]
    else:
        new_scene += ' ' + distance

    return new_scene


def diff_jduge(diff, param_type, param_name):
    """得出差值结论"""
    if param_type:
        if diff < globalVal._PARAM[param_name + '_RULES'][0]:
            return '变差' + str(abs(diff)) + '%'
        elif diff > globalVal._PARAM[param_name + '_RULES'][1]:
            return '变优' + str(diff) + '%'
    else:
        if diff < globalVal._PARAM[param_name + '_RULES'][0]:
            return '变优' + str(abs(diff)) + '%'
        elif diff > globalVal._PARAM[param_name + '_RULES'][1]:
            return '变差' + str(diff) + '%'
    return None


def param_type(param_name):
    """得出性能指标类型，True:正向指标，False:负向指标"""
    if 'FALSE' in param_name or 'WRONG' in param_name or 'UNRECG' in param_name or 'ERROR' in param_name:
        return False
    else:
        return True


def clear_conclusion():
    """清除历史测试结论"""
    global _CONTENT
    _CONTENT = ''


def get_conclusion(scene_name, version, param_json):
    """
       得到测试结论
    Args:
        scene_name : [string] 测试场景
        param_json : [dict] 测试版本性能差值
    Returns:
        conclusion : [string] 中文描述的测试结论
    """
    global _CONTENT
    
    curr_content = ''
    for param_name in param_json:
        if 'ASR_ERROR_CODE' == param_name:
            curr_content += '; '
            for err_code in param_json[param_name]:
                param_diff = param_json[param_name][err_code]
                if '%' in param_diff:
                    result = diff_jduge(float(param_diff.strip('%')), param_type(param_name), param_name)
                    if result is not None:
                        curr_content += err_code + '错误码' + result + '; '
        else:
            param_diff = param_json[param_name]
            if '%' in param_diff:
                result = diff_jduge(float(param_diff.strip('%')), param_type(param_name), param_name)
                if result is not None:
                    curr_content += ', ' + _PARAM_DESC[param_name] + '' + result

    if curr_content != '':
        _CONTENT += '[' + scene_mapping(scene_name) + '] ' + version + '版本:' + curr_content[1:] + '\n'
