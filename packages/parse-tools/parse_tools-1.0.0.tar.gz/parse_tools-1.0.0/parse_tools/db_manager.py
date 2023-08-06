#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: db_manager.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date:   20/09/02 上午10:14
"""
import os
import shelve
import copy
import globalVal


class AutoVivification(dict):
    """Inplememtation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def get_split_scene_item(sampleset_name):
    """
        [场景转换] 将测试集名称转化为scene_list格式，用于按场景汇总测试数据
    Args:
        sampleset_name : [string] 测试集名称
    Returns:
        scene_list : [list] 测试类型, 场景信息1, 场景信息2, .., 场景信息X
        audio_name : [string] 测试音频名称
    """
    scene_name, audio_name = globalVal.get_scene_name(sampleset_name)
    scene_list = globalVal.get_scene_list(scene_name)
    return scene_list, audio_name
    

def get_sampleset_list(sampleset_name):
    """
        [场景转换] 将测试集名称转化为scene_list格式，用于按场景汇总测试数据
    Args:
        sampleset_name : [string] 测试集名称
    Returns:
        sampleset_list : [list] 测试类型, 场景信息1, 场景信息2, .., 场景信息X, 测试音频名称
    """
    scene_list, audio_name = get_split_scene_item(sampleset_name)
    if audio_name == '':
        return scene_list
    else:
        return scene_list + [audio_name]


def check_version_exsit(sampleset_name, sdk_version):
    """
        [查询db] 查询db中是否已存在版本信息
    Args:
        sampleset_name : [string] 测试集名称
        sdk_version : [string] SDK版本
    Returns:
        int : 0 测试场景不存在
              1 测试场景存在、但audio_name不存在
              2 audio_name存在、但sdk_version不存在
              3 都存在
    """
    scene_list, audio_name = get_split_scene_item(sampleset_name)
    tmp_data = globalVal._DATABASE
    for scene_item in scene_list:
        if not scene_item in tmp_data:
            return 0
        else:
            tmp_data = tmp_data[scene_item]
    if audio_name in tmp_data:
        if sdk_version in tmp_data[audio_name]:
            return 3
        else:
            return 2
    else:
        return 1
    

def fetch_db(sampleset_name, sdk_version):
    """
        [测试信息读取] 按照测试集名称、SDK版本读取详细测试信息
    Args:
        sampleset_name : [string] 测试集名称
        sdk_version : [string] SDK版本
        request_info : [dict] 格式详见globalVal._DB_REQUEST
    Returns:
        bool : 正常执行/发生错误
    """
    sampleset_list = get_sampleset_list(sampleset_name)
    result_json = globalVal._DATABASE
    for scene_item in sampleset_list:
        result_json = result_json[scene_item]
    return result_json[sdk_version]


def updateDataToDB(sampleset_name, sdk_version, key, result_dict):
    """
        [测试结果记录] 按照测试集名称、SDK版本，把识别query答案和结果写入db
    Args:
        sampleset_name : [string] 测试集名称
        sdk_version : [string] SDK版本
        key : [string] 传入文件类型，answer或recognize_result
        result_dict : [dict] 识别query的标注答案、或识别结果dict
    Returns:
        bool : 正常执行/发生错误
    """
    sampleset_list = get_sampleset_list(sampleset_name)
    new_data = {key:result_dict}

    if not sampleset_list[0] in globalVal._DATABASE:
        globalVal._DATABASE[sampleset_list[0]] = AutoVivification()

    json_data = globalVal._DATABASE[sampleset_list[0]]
    for scene_item in sampleset_list[1:-1]:
        json_data = json_data[scene_item]
    if sdk_version == '':
        json_data[sampleset_list[-1]].update(new_data)
    else:
        json_data[sampleset_list[-1]][sdk_version].update(new_data)
