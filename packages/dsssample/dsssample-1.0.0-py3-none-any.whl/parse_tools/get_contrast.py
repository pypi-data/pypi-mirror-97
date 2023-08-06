#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: get_contrast.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date: 2020/01/19 上午12:05
"""

import os
import subprocess
import copy
import importlib, sys
importlib.reload(sys)

import globalVal
import speech_parse


def is_new_test(sample_name, audio_name, version):
    """
        [增量统计判断] 如果是新增场景或版本，则将单个集合的答案和识别结果txt合并入场景汇总中，否则不合并
    Args:
        sample_name : [string] 测试集完整名称：测试场景/音频名称
        audio_name : [string] 音频名称
    Returns:
        flag : [bool] 是否新增场景. True:是，False:否
    """
    scene_name = sample_name.split('_' + str(audio_name))[0]
    if scene_name in globalVal._NEW_DICT:
        if audio_name in globalVal._NEW_DICT[scene_name]:
            if version != '' and (version in globalVal._NEW_DICT[scene_name][audio_name]):
                return True
            elif len(globalVal._NEW_DICT[scene_name][audio_name]) == len(globalVal._VERSION_LIST):
                return True
    return False


def update_result_file(sample_name, audio_name, in_file, version=''):
    """
        [场景识别结果汇总] 将单个音频集的测试识别结果，拼接到对应测试场景中，用于场景数据汇总
    Args:
        sample_name : [string] 测试集完整名称：测试场景/音频名称
        audio_name : [string] 音频名称
        in_file : [string] 单个音频集的识别结果
    Returns:
        out_file : [txt] 对应测试场景的识别结果
    """
    if not is_new_test(sample_name, audio_name, version):
        return
    out_file = update_file_path(in_file, audio_name)
    with open(out_file, 'a+', encoding='utf-8') as out_f:
        for line in open(in_file, 'r', encoding='utf-8'):
            out_f.writelines(line)
    out_f.close()


def update_file_path(in_file, audio_name):
    """
        [路径替换] 从单个音频集路径，得到单个测试场景的路径
    Args:
        in_file : [string] 原始路径
        audio_name : [string] 要过滤的音频集名称
    Returns:
        out_file : [string] 更新路径
    """
    out_file = in_file.split(globalVal._WORK_DIRECTORY + '/')[1]
    if '_' + audio_name in out_file:
        out_file = out_file.replace('_' + audio_name, '')
    if audio_name in out_file:
        out_file = out_file.replace(audio_name, '')
    return os.path.join(globalVal._WORK_DIRECTORY, out_file)


class VoiceprintContrast(object):
    """Contrast the voiceprint results of different versions"""
    def __init__(self, sample_set, version_array=[]):
        if len(version_array) == 0:
            self.version_list = globalVal._VERSION_LIST
        else:
            self.version_list = version_array
        self.result_data = globalVal.get_scene_data(sample_set)
        self.base_version = self.version_list[0]
        self.result_json = {}

    def get_intersect_vp(self, flag):
        if flag:
            self.get_contrast()
        else:
            self.fetch_contrast()
        return self.result_json
        
    def get_contrast(self):
        """Get contrast result"""
        intersec_dict = set(self.result_data[self.version_list[0]]['recognize_result'].keys())
        for version in self.version_list[1:]:
            tmp_dict = set(self.result_data[version]['recognize_result'].keys())
            intersec_dict = intersec_dict.intersection(tmp_dict)
        for version in self.version_list:
            version_data = self.result_data[version]['recognize_result']
            vp_right = 0
            vp_wrong = 0
            for query_name in intersec_dict:
                if '正确' in version_data[query_name]['desc']:
                    vp_right += 1
                elif '错误' in version_data[query_name]['desc']:
                    vp_wrong += 1
            self.result_json.update({version: {
                'vp_total': len(intersec_dict), 
                'vp_right': vp_right, 
                'vp_wrong': vp_wrong
            }})

    def fetch_contrast(self):
        """Fetch contrast result"""
        vp_list = ['vp_total', 'vp_right', 'vp_wrong']
        for audio_name in self.result_data:
            if audio_name in ['answer', 'excel_count', 'sample_name', 'comparison']:
                continue
            if not 'comparison' in self.result_data[audio_name]:
                continue
            compare_data = self.result_data[audio_name]['comparison']
            if self.version_list[-1] in self.result_json:
                for version in self.version_list:
                    for key in vp_list:
                        self.result_json[version][key] += compare_data[version][key]
            else:
                self.result_json.update(copy.deepcopy(compare_data))
        # [异常检查] 如果两个版本完全无交集，则初始化为0
        if not self.base_version in self.result_json:
            for version in self.version_list[version]:
                self.result_json.update({version: {}.fromkeys(vp_list, 0)})


class ContrastAccuracy(object):
    """Contrast the recognition results of different versions"""
    def __init__(self, sample_set, version_array=[]):
        """
            [多次识别query统计] 根据唤醒和首次识别的错误码情况，排除不参与统计识别率的query
        Args:
            sample_set : [string] 测试集原始名称，由"audio-scene/audio-name"组成
            version_array : [list] SDK版本集合
        Returns:
            result_json : [json] 格式为：{
                'total_count': 对齐的识别query条数,
                '版本1': [交集识别率-对比2, ..., 交集识别率-对比N],
                '版本2': 交集识别率,
                …
                '版本N': 交集识别率
            }
            其中，交集识别率的格式为：{
                'intersect_count': 识别result交集个数（包括有识别结果和识别结果为空的）,
                'intersect_success_count': 交集成功次数（交集成功率=交集成功次数/交集个数）,
                'intersect_recall_count': 交集召回次数（交集召回率=交集召回次数/交集成功次数）,
                'wer': 字准1（基于识别result、取交集）,
                'ser': 句准1（基于识别result、取交集）,
                'valid_wer': 字准2（仅统计有识别结果的result、不取交集）,
                'valid_ser': 句准2（仅统计有识别结果的result、不取交集）,
                'valid_intersect_count': 有识别结果的交集个数,
                'valid_intersect_wer': 字准3（仅统计有识别结果的result、取交集）,
                'valid_intersect_ser': 句准3（仅统计有识别结果的result、取交集）
            }
        """
        if len(version_array) == 0:
            self.version_list = globalVal._VERSION_LIST
        else:
            self.version_list = version_array
        self.version_num = len(self.version_list)
        self.base_version = self.version_list[0]
        if self.version_num == 1 or not 'mutiplyasr' in sample_set:
            self.contrast_with_all = True
        else:
            self.contrast_with_all = globalVal._PARAM['CONTRAST_WITH_ALL']
        self.audio_scene, self.audio_name = globalVal.get_scene_name(sample_set)
        if self.audio_name == '':
            self.sample_set = self.audio_scene
        else:
            self.sample_set = self.audio_scene + '_' + self.audio_name
        # result_json 初始化
        self.result_data = globalVal.get_scene_data(sample_set)
        contrast_flag = 0
        if self.contrast_with_all:
            contrast_flag = 1
        self.result_json = {
            'total_count': 0, 
            'base_version': self.base_version,
            'flag': contrast_flag
        }

        # 单次识别、多次识别的answer、result路径初始化
        self.init_result_path()

    def init_result_path(self):
        """
            [路径初始化] 识别结果路径初始化，用于wer计算识别准确率
        Args:
            null
        Returns:
            result_path : [list] 识别result
            valid_result_path : [list] 识别结果不为空的query
            intersec_result_path : [dict] 多个版本的识别result，取交集
            valid_intersec_result_path : [dict] 多个版本的识别结果不为空的query，取交集
        """
        self.total_answer_path = os.path.join(globalVal.get_save_path(self.audio_scene, self.audio_name),
            self.sample_set + '_answer_result.txt')
        self.result_path = []
        self.valid_result_path = []
        self.intersec_result_path = {}
        self.valid_intersec_result_path = {}
        if not self.contrast_with_all:
            self.intersec_result_path[self.base_version] = []
            self.valid_intersec_result_path[self.base_version] = []
            self.result_json[self.base_version] = []
        for version in range(self.version_num):
            tmp_path = os.path.join(globalVal.get_save_path(self.audio_scene, self.audio_name),
                self.version_list[version] + '_' + self.sample_set + '_recognize_result')
            self.result_path.append(tmp_path + '.txt')
            self.valid_result_path.append(tmp_path + '_valid.txt')
            if version != 0 or self.contrast_with_all:
                self.intersec_result_path[version] = tmp_path + '_intersection.txt'
                self.valid_intersec_result_path[version] = tmp_path + '_valid_intersection.txt'
            if version != 0 and not self.contrast_with_all:
                self.intersec_result_path[self.base_version].append(
                    self.result_path[0].split('.txt')[0] + '_intersection.txt' + '-' + str(version))
                self.valid_intersec_result_path[self.base_version].append(
                    self.result_path[0].split('.txt')[0] + '_valid_intersection.txt' + '-' + str(version))

    def get_file_name(self, in_file, version, intersec_version):
        """Get contrast file name"""
        if version != 0 or self.contrast_with_all:
            return in_file[version]
        else:
            return in_file[self.base_version][int(intersec_version[1]) - 1]
        
    def get_valid(self):
        """Get valid recognize result"""
        for version in range(self.version_num):
            valid_data = {}
            valid_path = self.valid_result_path[version]
            self.valid_result_path.append(valid_path)
            if os.path.exists(valid_path):
                os.remove(valid_path)
            version_result = self.result_data[self.version_list[version]]['recognize_result']
            with open(valid_path, 'a+', encoding='utf-8') as valid_result_file:
                for query_name in version_result:
                    query_result = version_result[query_name]['recg_result']
                    if query_result == '':
                        continue
                    valid_result_file.write(query_name + ':' + query_result + '\n')
                    valid_data.update({
                        query_name:{
                            'recg_result': query_result,
                            'desc': version_result[query_name]['desc']
                        }
                    })
            valid_result_file.close()
            self.result_data[self.version_list[version]].update({'valid_result': valid_data})

    def find_intersection(self, key, intersec_result_path, intersec_version):
        """Get the intersection between two version's asr result"""
        # 计算交集query
        intersec_dict = set(self.result_data[self.version_list[intersec_version[0]]][key].keys())
        for version in intersec_version[1:]:
            tmp_dict = set(self.result_data[self.version_list[version]][key].keys())
            intersec_dict = intersec_dict.intersection(tmp_dict)
        for version in intersec_version:
            total_count = 0
            success_count = 0
            recall_count = 0
            # 交集识别结果写入txt文件
            intersec_result_file_path = self.get_file_name(intersec_result_path, version, intersec_version)
            if os.path.exists(intersec_result_file_path):
                os.remove(intersec_result_file_path)
            rec_result = self.result_data[self.version_list[version]][key]
            with open(intersec_result_file_path, 'a+', encoding='utf-8') as intersec_result_file:
                for query_num in intersec_dict:
                    total_count += 1
                    if rec_result[query_num]['recg_result'] != '':
                        success_count += 1
                        if not 'asr reject' in rec_result[query_num]['desc']:
                            recall_count += 1
                    intersec_result_file.write(query_num + ':' + rec_result[query_num]['recg_result'] + '\n')
            intersec_result_file.close()
            # 更新交集个数
            if key == 'recognize_result':
                intersect_data = {
                    'intersect_count': total_count, 
                    'intersect_success_count': success_count, 
                    'intersect_recall_count': recall_count
                }
                if total_count > 0:
                    intersect_data.update({
                        'intersect_success_rate': "%.3f%%" % float(success_count * 100 / total_count),
                        'intersect_recall_rate': "%.3f%%" % float(recall_count * 100 / total_count)
                    })
                else:
                    intersect_data.update({
                        'intersect_success_rate': '0.0%',
                        'intersect_recall_rate': '0.0%'
                    })
                if version != 0 or self.contrast_with_all:
                    self.result_json[self.version_list[version]] = intersect_data
                else:
                    self.result_json[self.base_version].append(intersect_data)
                self.result_json['total_count'] = total_count
            else:
                intersect_data = {
                    'valid_intersect_count': total_count, 
                    'valid_intersect_success_count': success_count, 
                    'valid_intersect_recall_count': recall_count
                }
                if version != 0 or self.contrast_with_all:
                    self.result_json[self.version_list[version]].update(intersect_data)
                else:
                    self.result_json[self.base_version][version - 1].update(intersect_data)

    def get_contrast(self):
        """Get the intersection result"""
        if self.contrast_with_all:
            intersec_version = range(self.version_num)
            self.find_intersection('recognize_result', self.intersec_result_path, intersec_version)
            self.find_intersection('valid_result', self.valid_intersec_result_path, intersec_version)
        else:
            for version in range(1, self.version_num):
                intersec_version = [0, version]
                self.find_intersection('recognize_result', self.intersec_result_path, intersec_version)
                self.find_intersection('valid_result', self.valid_intersec_result_path, intersec_version)
        # 如果当前是单人音频，则拷贝测试结果和答案到具体场景下，用于数据汇总
        if len(self.sample_set.split('_')) > 5:
            update_result_file(self.sample_set, self.audio_name, self.total_answer_path)
            for version_inx in range(self.version_num):
                if self.contrast_with_all:
                    intersec_version = [version_inx]
                else:
                    if version_inx == 0:
                        continue
                    else:
                        intersec_version = [0, version_inx]
                for version in intersec_version:
                    vers = self.version_list[version]
                    update_result_file(self.sample_set, self.audio_name, self.result_path[version], vers)
                    update_result_file(self.sample_set, self.audio_name, self.valid_result_path[version], vers)
                    update_result_file(self.sample_set, self.audio_name, 
                        self.get_file_name(self.intersec_result_path, version, intersec_version), vers)
                    update_result_file(self.sample_set, self.audio_name, 
                        self.get_file_name(self.valid_intersec_result_path, version, intersec_version), vers)
        
    def fetch_contrast(self):
        """Fetch contrast comparison"""
        intersect_list = ['intersect_count', 'intersect_success_count', 'intersect_recall_count', 
            'valid_intersect_count', 'valid_intersect_success_count', 'valid_intersect_recall_count']
        for audio_name in self.result_data:
            if audio_name in ['answer', 'excel_count', 'sample_name', 'comparison']:
                continue
            if not 'comparison' in self.result_data[audio_name]:
                continue
            compare_data = self.result_data[audio_name]['comparison']
            if self.version_list[-1] in self.result_json:
                self.result_json['total_count'] += compare_data['total_count']
                for version in range(self.version_num):
                    curr_version = self.version_list[version]
                    for key in intersect_list:
                        if version != 0 or self.contrast_with_all:
                            self.result_json[curr_version][key] += \
                                compare_data[curr_version][key]
                        else:
                            self.result_json[curr_version][version - 1][key] += \
                                compare_data[curr_version][version - 1][key]
            else:
                self.result_json = copy.deepcopy(compare_data)
        for version in range(self.version_num):
            if version != 0 or self.contrast_with_all:
                curr_data = self.result_json[self.version_list[version]]
            else:
                curr_data = self.result_json[self.version_list[version]][version - 1]
            intersect_count = curr_data['intersect_count']
            if intersect_count > 0:
                curr_data.update({
                    'intersect_success_rate': "%.3f%%" % \
                        float(curr_data['intersect_success_count'] * 100 / intersect_count),
                    'intersect_recall_rate': "%.3f%%" % \
                        float(curr_data['intersect_recall_count'] * 100 / intersect_count)
                })
            else:
                curr_data.update({
                    'intersect_success_rate': '0.0%',
                    'intersect_recall_rate': '0.0%'
                })
        # [异常检查] 如果两个版本完全无交集，则初始化为0
        if not self.base_version in self.result_json:
            for version in self.version_list:
                self.result_json.update({version: {}.fromkeys(intersect_list, 0)})

    def get_contrast_result(self, flag):
        """Get contrast result"""
        if flag:
            # 单个测试集数据统计，取交集
            self.get_valid()
            self.get_contrast()
        else:
            # 单个测试场景数据汇总 - 从单测试集的comparsion里获取数据并汇总
            self.fetch_contrast()
        
    def get_contrast_accuracy(self, flag=True):
        """Get contrast accuracy"""
        self.get_contrast_result(flag)
        for version_inx in range(self.version_num):
            if self.contrast_with_all:
                intersec_version = [version_inx]
            else:
                if version_inx == 0:
                    continue
                else:
                    intersec_version = [0, version_inx]
            for version in intersec_version:
                if 'semanticasr' in self.sample_set:
                    total_count = self.result_json['total_count']
                else:
                    total_count = -1
                valid_charACU, valid_sentenseACU, err = speech_parse.cal_asr_wer(
                    self.total_answer_path, 
                    self.valid_result_path[version], 
                    total_count
                )
                intersec_charACU, intersec_sentenseACU, err = speech_parse.cal_asr_wer(
                    self.total_answer_path, 
                    self.get_file_name(self.intersec_result_path, version, intersec_version), 
                    total_count
                )
                valid_intersec_charACU, valid_intersec_sentenseACU, err = speech_parse.cal_asr_wer(
                    self.total_answer_path, 
                    self.get_file_name(self.valid_intersec_result_path, version, intersec_version), 
                    total_count
                )
                wer_list = {
                    'wer': intersec_charACU, 
                    'ser': intersec_sentenseACU, 
                    'valid_wer': valid_charACU, 
                    'valid_ser': valid_sentenseACU, 
                    'intersect_wer': valid_intersec_charACU, 
                    'intersect_ser': valid_intersec_sentenseACU
                }
                if version != 0 or self.contrast_with_all:
                    self.result_json[self.version_list[version]].update(wer_list)
                else:
                    self.result_json[self.base_version][version - 1].update(wer_list)

        return self.result_json
