#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: read_message.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date: 2020/12/09 下午15:50
"""
import os
import chardet
import copy
import logging
import importlib, sys
importlib.reload(sys)

import globalVal
import db_manager


def _is_right_encoding(file_path, encoding):
    """
        判断文件编码格式是否符合预期
    Args:
        file_path : [string] 文件路径
        encoding : [string] 预期的编码格式
    Returns:
        bool : 是否符合预期
    """
    r_file = open(file_path, 'rb')
    try:
        file_encode = chardet.detect(r_file.read())['encoding']
        if file_encode is not None and file_encode != encoding:
            logging.error('%s 编码格式是 %s, 不是%s', r_file, file_encode, encoding)
            globalVal.record_err(file_path, 1202, file_path + '编码格式错误,实际是' + file_encode)
            return False
    except:
        logging.error('%s 获取编码信息失败', r_file)
        globalVal.record_err(file_path, 1202, file_path + '编码格式获取失败')
        return False
    return True


def _validation_check(file_path):
    """
        检查文件是否异常（路径存在、是utf-8格式）
    Args:
        file_path : [string] 文件路径
    Returns:
        bool : 是否符合预期
    """
    if not os.path.exists(file_path):
        logging.error('找不到 %s , 请检查路径是否正确', file_path)
        globalVal.record_err(file_path, 1201, '请检查路径, 找不到该文件')
        return False
    elif not _is_right_encoding(file_path, 'utf-8'):
        return False
    return True


def _get_param_from_line(line, key, key_type='string'):
    """
    从line中，按照key_type读取对应key的值 
    """
    if key in line:
        try:
            value = line.strip().split(key + ':')[1].split('\t')[0]
            if '_qc' in value and key == 'asr_sn':
                value = value.split('_qc')[0]
            if key_type == 'int':
                return int(value)
            else:
                if len(value):
                    return value
                else:
                    return None
        except (TypeError, ValueError, IndexError) as e:
            logging.error(e)
            logging.error('获取' + key + '时出现异常，请检查回调格式:' + line)
    return None


class AnswerParseThread():
    """
        根据人工标注，将读到的唤醒和识别答案进行配对，一一组合成 “唤醒” 或 “唤醒+识别” 的形式
    Args:
        sample_name : [string] 测试音频集名称
        save_path : [string] 当前音频集答案存储路径
        wp_answer_path : [string] 唤醒人工标注答案文件路径
        asr_answer_path : [string] 识别人工标注答案文件路径
    Returns:
        __AnswerList : [list] 唤醒、识别组合成一一对应关系的list
        __wpStatusDict : [dict] 唤醒词、标注条数
        __asrQueryCount : [int] 识别query标注个数
        __wpLocationAnswerList : [list] 声源定位location标注答案list(仅声源定位集合)
    """

    def __init__(self, sample_name, save_path, wp_answer_path, asr_answer_path):
        """参数初始化
        """
        self.__AnswerList = []
        self.__asrQueryCount = 0
        self.init_name = sample_name
        audio_scene, audio_name = globalVal.get_scene_name(sample_name)
        self.sampleset_name = audio_scene + '_' + audio_name
        self.wp_answer_path = wp_answer_path
        self.asr_answer_path = asr_answer_path
        self.answer_result_dict = {}
        self.speech_type = globalVal.get_speech_type(self.sampleset_name)
        self.asr_answer_name = os.path.join(save_path, self.sampleset_name + '_answer_result.txt')
        self.record_answer_flag = True
        if self.speech_type == globalVal.SpeechType.WHISPER:
            self.__wpStatusDict = {'summary': copy.deepcopy(globalVal._WHISPER_DICT)}
        else:
            self.__wpStatusDict = {'summary': copy.deepcopy(globalVal._WP_DICT)}
        if os.path.exists(self.asr_answer_name):
            self.record_answer_flag = False

    def readAnswerMessages(self):
        """答案读取和拼接,用于生成__AnswerList
        """
        #【1】读取answer文件
        if self.speech_type in globalVal.SPEECH_MODE['wp']:        # 仅唤醒(普通唤醒、声源定位、dci)
            if _validation_check(self.wp_answer_path):
                self.__AnswerList = self.parse_answer(self.wp_answer_path, 'wp')
        elif self.speech_type in globalVal.SPEECH_MODE['asr']:     # 仅识别(纯识别)
            if _validation_check(self.asr_answer_path):
                self.__AnswerList = self.parse_answer(self.asr_answer_path, 'asr')
                self.__asrQueryCount = len(self.__AnswerList)
        elif self.speech_type in globalVal.SPEECH_MODE['wp+asr']:  # 唤醒+识别(单次识别、多次识别、语义识别、声纹)
            if _validation_check(self.wp_answer_path) and \
                (self.speech_type == globalVal.SpeechType.WHISPER or _validation_check(self.asr_answer_path)):
                self.__AnswerList = self.makeup_query(
                    self.parse_answer(self.wp_answer_path, 'wp'), 
                    self.parse_answer(self.asr_answer_path, 'asr')
                )
        #【2】写好的answer文件，按照json格式读入，然后记录入db
        if self.record_answer_flag:
            self.recordRecAnswerForWer()
        if globalVal._DEBUG_MODE:
            for list in self.__AnswerList:
                print(list)

        return self.__AnswerList, self.__wpStatusDict, self.__asrQueryCount

    def parse_answer(self, file_path, parse_type):
        """读取&解析 唤醒、识别场景的标注答案
        """
        if self.speech_type == globalVal.SpeechType.SPLIT_ASR:
            return self.read_split_answer(file_path, parse_type)
        else:
            asr_answer = self.read_normal_answer(file_path, parse_type)
            if self.speech_type == globalVal.SpeechType.ROLE_ASR:
                return self.merge_query_for_same_role(asr_answer)
            else:
                return asr_answer
        
    def read_normal_answer(self, file_path, parse_type):
        """读取&解析 整轨形式的标注答案，如"query内容&query起点时刻&query尾点时刻"
        """
        answer_list = []
        if not os.path.exists(file_path):
            return answer_list
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = line.strip().split('\r')[0].split('&')
                if len(item) < 3 or line.startswith('#'):
                    continue
                try:
                    if parse_type == 'asr':
                        answer = {'asr_query': item[0], 'asr_begin': int(item[1]), 'asr_end': int(item[2])}
                        if len(item) == 4:
                            if self.speech_type == globalVal.SpeechType.ROLE_ASR:
                                answer.update({'asr_role': item[3]})
                            else:
                                answer.update({'asr_pcm_name': item[3]})
                    elif parse_type == 'wp':
                        if not item[0] in self.__wpStatusDict:
                            if self.speech_type == globalVal.SpeechType.WHISPER:
                                self.__wpStatusDict.update({item[0]: copy.deepcopy(globalVal._WHISPER_DICT)})
                            else:
                                self.__wpStatusDict.update({item[0]: copy.deepcopy(globalVal._WP_DICT)})
                        self.__wpStatusDict[item[0]]['queryCount'] += 1
                        answer = {'wp_words': item[0], 'wp_begin': int(item[1]), 
                            'wp_end': int(item[2]), 'wp_index': None, 'wp_whisper': None}
                        if len(item) == 4:
                            if self.speech_type == globalVal.SpeechType.WP_LOCATION:
                                answer.update({'wp_location': item[3]})
                            elif self.speech_type == globalVal.SpeechType.WHISPER:
                                wp_whisper = int(item[3])
                                answer.update({'wp_whisper': wp_whisper})
                                if not wp_whisper in self.__wpStatusDict[item[0]]['whisperInfo']:
                                    self.__wpStatusDict[item[0]]['whisperInfo'].update({
                                        wp_whisper: copy.deepcopy(globalVal._BASE_WHISPER)
                                    })
                                self.__wpStatusDict[item[0]]['whisperInfo'][wp_whisper]['queryCount'] += 1
                            else:
                                answer.update({'wp_index': int(item[3])})
                        elif self.speech_type == globalVal.SpeechType.WHISPER:
                            logging.error(file_path + ', 未标注轻问轻答类型，请检查: ' + line)
                            globalVal.record_err(file_path, 1203, '未标注轻问轻答类型，请检查: ' + line)
                            return []
                    else:
                        return {}
                except TypeError:
                    logging.error(file_path + ', 标注答案格式异常，请检查: ' + line)
                    globalVal.record_err(file_path, 1203, '标注答案格式异常，请检查: ' + line)
                answer_list.append(answer)
        return answer_list

    def read_split_answer(self, file_path, parse_type):
        """读取&解析 单条形式的标注答案，目前仅适用于codriver
        """
        answer_list = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split('\r')[0]
                if ':' in line:
                    item = line.split(':')
                    if len(item) < 2:
                        continue
                    answer_list.append({'file_name': item[0], 'asr_query': item[1]})
                if ',' in line:
                    item = line.split(',').strip()
                    if len(item) < 2:
                        continue
                    if len(answer_list) > 0:
                        answer_list[-1]['asr_begin'] = item[0]
                        answer_list[-1]['asr_end'] = item[1]
        return answer_list

    def makeup_query(self, wp_answer, asr_answer):
        """将唤醒、识别答案，组合成"唤醒+识别"的query形式
        """
        answer_list = []
        tmp_list = {}
        for query in self.sort_list(wp_answer, asr_answer):
            if 'wp_words' in query:
                if len(tmp_list):
                    answer_list.append(tmp_list)
                tmp_list = query
            else:
                if 'asr_query' in tmp_list:
                    if self.speech_type == globalVal.SpeechType.MULTI_ASR:
                        answer_list.append(tmp_list)
                        tmp_list = query
                        self.__asrQueryCount += 1
                    else:
                        logging.error(self.asr_answer_path + ', 单次识别:标注答案出现连续识别:' + str(query))
                        globalVal.record_err(self.asr_answer_path, 1205, '单次识别:标注答案出现连续识别:' + str(query))
                elif 'wp_words' in tmp_list:
                    if self.speech_type != globalVal.SpeechType.MULTI_ASR:
                        self.__asrQueryCount += 1
                    tmp_list.update(query)
                else:
                    logging.error(self.asr_answer_path + ', 单次识别:缺少唤醒标注:' + str(query))
                    globalVal.record_err(self.asr_answer_path, 1205, '单次识别:缺少唤醒标注:' + str(query))
        if len(tmp_list):
            answer_list.append(tmp_list)
        return answer_list

    def merge_query_for_same_role(self, asr_answer):
        """双人交互，按角色进行答案合并
        """
        merged_answer_list = []
        last_role = ''
        for query in asr_answer:
            curr_role = query['asr_role']
            if last_role != curr_role:
                merged_answer_list.append(query)
            else:
                merged_answer_list[-1]['asr_end'] = query['asr_end']
                merged_answer_list[-1]['asr_query'] +=  query['asr_query']
            last_role = curr_role
        return merged_answer_list

    def sort_list(self, wp_answer, asr_answer):
        """将答案list按照起点时刻进行排序
        """
        tmp_list = {}
        for answer in wp_answer:
            tmp_list.update({answer['wp_begin']: answer})
        for answer in asr_answer:
            tmp_list.update({answer['asr_begin']: answer})
        sort_list = dict(sorted(tmp_list.items(), key=lambda x: x[0]))
        return sort_list.values()
  
    def recordRecAnswerForWer(self):
        """把标注的识别query写入txt文件，用于wer计算准确率
        """
        if not self.speech_type in globalVal.SPEECH_MODE['wp']:
            if self.speech_type == globalVal.SpeechType.MULTI_ASR:
                sufix = '_first.pcm'
            else:
                sufix = '.pcm'
            pcm_index = 0
            asr_index = 0
            answer_f = open(self.asr_answer_name, 'w', encoding='utf-8')
            for query in self.__AnswerList:
                if 'asr_query' in query:
                    if 'asr_pcm_name' in query:
                        pcm_name = query['asr_pcm_name'] + '.pcm'
                    elif 'file_name' in query:
                        pcm_name = self.sampleset_name + '_' + query['file_name']
                    elif 'wp_words' in query:
                        pcm_index += 1
                        pcm_name = self.sampleset_name + '_' + str(pcm_index) + sufix
                    else:
                        asr_index += 1
                        pcm_name = self.sampleset_name + '_' + str(asr_index) + '.pcm'
                    if not '_first.pcm' in pcm_name:
                        answer_f.write(pcm_name + ':' + query['asr_query'] + '\n')
                    self.answer_result_dict.update({pcm_name: {'content': query['asr_query']}})
                    if self.speech_type == globalVal.SpeechType.ROLE_ASR:
                        self.answer_result_dict[pcm_name].update({'asr_role': query['asr_role']})
                else:
                    pcm_index += 1
            answer_f.close()
            db_manager.updateDataToDB(self.init_name, '', 'answer', self.answer_result_dict)

    def getLocationAnswerList(self):
        """计算声源定位的answer list
        """
        wp_location_answer = {}
        for wp_item in self.__AnswerList:
            scene = wp_item['wp_location'].rsplit('_', 1)[0]
            location = wp_item['wp_location'].rsplit('_', 1)[1]
            if scene in wp_location_answer:
                if location in wp_location_answer[scene]:
                    wp_location_answer[scene][location]['total'] += 1
                else:
                    wp_location_answer[scene].update({location: {'total': 1, 'wpCount': 0}})
            else:
                wp_location_answer.update({scene: {location: {'total': 1, 'wpCount': 0}}})
        return wp_location_answer


class LogParseThread():
    """将读到的各种回调信息根据sn进行配对，组合成一次完整的语音请求
    Args:
        log_path : [string] 灌测回调打点文件路径
        audio_scene : [string] 测试音频场景
    Returns:
        __logResultList : [list] 
        __totalWpCount : [int] 
    """

    def __init__(self, log_path, audio_scene):
        """参数初始化
        """
        self.__totalWpCount = 0
        self.__asrFirstRequestCount = 0
        self.__asrMultiRequestCount = 0
        self.__wp_mode = 0
        self.__use_vad = False
        self.__logResultList = []
        self.__asrMultiError = []
        self.__asrFirstError = []
        self.log_path = log_path
        self.audio_scene = audio_scene
        self.speech_type = globalVal.get_speech_type(audio_scene)

    def readLogMessages(self):
        """log关键信息筛选,用于生成__logResultList
        """
        if os.path.exists(self.log_path):
            if self.speech_type == globalVal.SpeechType.SPLIT_ASR:
                self.parse_codriver_log()
            else:
                self.parse_stream_log()
        else:
            logging.error('找不到 %s, 请检查路径是否正确', self.log_path)
            globalVal.record_err(self.log_path, 1201, '请检查路径, 找不到该文件')

        if globalVal._DEBUG_MODE:
            for list in self.__logResultList:
                print(list)
        
        if self.speech_type == globalVal.SpeechType.WHISPER:
            self.__wp_mode = 3
        list_info = [self.__logResultList, self.__asrFirstError, self.__asrMultiError]
        count_info = [self.__totalWpCount, self.__asrFirstRequestCount, self.__asrMultiRequestCount]
        return list_info, count_info, [self.__use_vad, self.__wp_mode]

    def parse_codriver_log(self):
        """解析codriver、单条识别模式 的识别结果
        """
        with open(self.log_path, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                line = line.strip()
                if not len(line) or 'File_Name' in line or '当前测试集' in line:
                    continue
                if 'SUMMARY' in line:
                    break
                item = line.split('\t')
                tmpList = {}.fromkeys(['file_name', 'asr_result', 'asr_sn', 'errCode'])
                tmpList['file_name'] = item[0]
                tmpList['asr_result'] = item[1]
                tmpList['asr_sn'] = item[21]
                tmpList['asr_corpus_id'] = item[22]
                if len(tmpList) > 26:
                    tmpList['errCode'] = item[26]
                else:
                    tmpList['errCode'] = -1
                try:
                    self.__logResultList.append(tmpList)
                except UnboundLocalError:
                    logging.debug("no wp & rec result")

    def parse_stream_log(self):
        """根据灌测打点日志，进行关键回调信息解析
        """
        wak_list = []
        asr_list = []
        cancel_list = []
        # 读取sdk日志打点文件，并按照audio_time存入list
        with open(self.log_path, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                line = line.strip()
                if not len(line) or line.startswith('#'):
                    continue
                if 'AUTOTEST_TIME' in line and 'tagName' in line and 'audio_time' in line:
                    if 'DOT_WP_' in line or 'DOT_DCI_DATA' in line:
                        if 'wpIndex' in line:
                            self.__wp_mode = 1
                        elif 'wp_sn' in line:
                            self.__wp_mode = 2
                        wak_list.append(line)
                    elif 'DOT_ASR_CANCEL' in line:
                        cancel_list.append({'asrCancel': _get_param_from_line(line, 'audio_time', 'int')})
                        self.__asrFirstError.append('cancel')
                    elif 'DOT_ASR_' in line:
                        if 'DOT_ASR_VAD_BEGIN' in line:
                            self.__use_vad = True
                        asr_list.append(line)
                    else:
                        logging.error('未知回调名称:' + line + ', 请检查日志:' + self.log_path)
                
        # 唤醒、识别 回调解析&query组合
        self.makeup_query(self.parse_wp_log(wak_list), self.parse_asr_log(asr_list), cancel_list)
        if self.speech_type == globalVal.SpeechType.ROLE_ASR:
            self.merge_query_for_same_role()

    def merge_query_for_same_role(self):
        """双人交互，按角色进行识别结果合并
        """
        merged_log_list = []
        last_role = ''
        for query in self.__logResultList:
            curr_role = query['asr_role']
            if last_role != curr_role:
                merged_log_list.append(query)
            else:
                merged_log_list[-1]['vadEnd'] = query['vadEnd']
                merged_log_list[-1]['asrFinalResult'] = query['asrFinalResult']
                merged_log_list[-1]['asr_sn'] += '+ws_' + query['asr_sn'].split('_ws_')[1]
                if query['asr_result'] is not None:
                    if merged_log_list[-1]['asr_result'] is None:
                        merged_log_list[-1]['asr_result'] = query['asr_result']
                    else:
                        merged_log_list[-1]['asr_result'] += '。' + query['asr_result']
            last_role = curr_role
        self.__logResultList = merged_log_list

    def makeup_query(self, wak_list, asr_list, cancel_list):
        """将唤醒、识别结果，组合成"唤醒+识别"的query形式
        """
        tmp_list = {}
        for content in self.sort_list(wak_list, asr_list, cancel_list):
            if content['audio_time'] == 0:
                continue
            query = content['content']
            if 'wpWords' in query:
                if len(tmp_list):
                    self.__logResultList.append(tmp_list)
                tmp_list = query
            elif 'asrCancel' in query:
                for i in range(len(self.__logResultList) - 1, -1, -1):
                    if 'asrReady' in self.__logResultList[i] and self.__logResultList[i]['asrReady'] is not None:
                        self.__logResultList[i].update(query)
                        break
            else:
                query.update({'asrCancel': None})
                if self.speech_type in [globalVal.SpeechType.PUER_ASR, globalVal.SpeechType.ROLE_ASR]:
                    # 纯识别
                    if len(tmp_list):
                        self.__logResultList.append(tmp_list)
                    tmp_list = query
                else:
                    # 极客模式的2~N次识别
                    if globalVal.is_jikemode_sn(query['match_sn']):
                        if self.speech_type == globalVal.SpeechType.MULTI_ASR:
                            self.__logResultList.append(tmp_list)
                            tmp_list = query
                    # 唤醒后首次识别
                    else:
                        tmp_list.update(query)
        self.__logResultList.append(tmp_list)

    def sort_list(self, wak_list, asr_list, cancel_list):
        """将结果list按照起点时刻进行排序
        """
        sort_list = []
        for content in wak_list:
            if self.__wp_mode == 2 and content['wpIndex'] is not None:
                time = int(content['wpIndex'].split('_')[1])
            else:
                time = content['wpTriggered']
            sort_list.append({'audio_time': time, 'content': content})
        if self.speech_type == globalVal.SpeechType.ROLE_ASR:
            for content in asr_list:
                if content['errCode'] is None:
                    sort_list.append({'audio_time': content['asrFinalResult'], 'content': content})
        else:
            for content in asr_list:
                time = -1
                for key in ['asrRunning', 'asrIgnore', 'asrReady', 'vadBegin', 
                    'asrFirstPartial', 'asrFinalResult', 'asrError']:
                    if content[key] is not None:
                        time = int(content[key])
                        break
                sort_list.append({'audio_time': time, 'content': content})
        for content in cancel_list:
            sort_list.append({'audio_time': content['asrCancel'], 'content': content})
        sort_list.sort(key=lambda x: x['audio_time'])
        return sort_list
        
    def parse_wp_log(self, log_list):
        """唤醒回调解析、组合
        """
        wp_query_list = []
        tmpList = {}
        for line in log_list:
            if 'DOT_WP_SUCCESS' in line:
                if len(tmpList):
                    wp_query_list.append(tmpList)
                if 'wpWords' in line:
                    wpWords = _get_param_from_line(line, 'wpWords')
                elif 'wpWord' in line:
                    wpWords = _get_param_from_line(line, 'wpWord')
                else:
                    wpWords = '小度小度'
                tmpList = {
                    'wpWords': wpWords,
                    'wpTriggered': _get_param_from_line(line, 'audio_time', 'int'),
                    'wpIndex': _get_param_from_line(line, 'wpIndex', 'int'),
                    'wpWhisper': _get_param_from_line(line, 'is_whisper', 'int'),
                    'wpSN': _get_param_from_line(line, 'wp_sn'),
                    'soundLocation': None,
                    'locationAccuracy': None,
                    'dci_data': None
                }
            elif 'DOT_WP_SOUND_LOCATION' in line:
                if len(tmpList):
                    tmpList['soundLocation'] = _get_param_from_line(line, 'sound_location')
            elif 'DOT_DCI_DATA' in line:
                if len(tmpList):
                    dci_data = _get_param_from_line(line, 'dci_data')
                    if dci_data.endswith(','):
                        dci_data = dci_data.rsplit(',', 1)[0]
                    dci_float_data = dci_data.split(',')
                    dci_float_data_length = len(dci_float_data)
                    if dci_float_data_length > 300:
                        dci_data = \
                            dci_data.split(',', dci_float_data_length - 300)[dci_float_data_length - 300]
                    dci_data = dci_data.replace(',', ' ')
                    tmpList['dci_data'] = dci_data
            else:
                logging.error('未知回调名称:' + line)
        if len(tmpList):
            wp_query_list.append(tmpList)

        if self.__wp_mode == 2:
            return self.process_same_wake(wp_query_list)
        else:
            self.__totalWpCount = len(wp_query_list)
            return wp_query_list

    def process_same_wake(self, wp_query_list):
        """小度+指令词，筛选真正的唤醒响应
        """
        last_wp_words = ''
        last_wp_sn = ''
        wp_list = []
        for query in wp_query_list:
            if query['wpSN'] == last_wp_sn:
                if last_wp_words == '小度' and query['wpWords'] != '小度':
                    wp_list[-1]['wpIndex']  = '小度_' + str(wp_list[-1]['wpTriggered'])
                    wp_list[-1]['wpWords'] = query['wpWords']
                    wp_list[-1]['wpTriggered'] = query['wpTriggered']
                    wp_list[-1]['soundLocation'] = query['soundLocation']
                    wp_list[-1]['dci_data'] = query['dci_data']
                else:
                    logging.error('出现异常唤醒回调,请检查:' + query['wpSN'])
            else:
                wp_list.append(query)
            last_wp_words = query['wpWords']
            last_wp_sn = query['wpSN']

        self.__totalWpCount = len(wp_list)
        return wp_list

    def parse_asr_log(self, log_list):
        """识别回调解析、组合
        """
        asr_query_list = []
        tmpList = {}
        for line in log_list:
            # 基础信息解析
            asr_sn = _get_param_from_line(line, 'asr_sn')
            audio_time = _get_param_from_line(line, 'audio_time', 'int')
            match_sn = asr_sn
            if 'moke_sn' in line:
                match_sn = _get_param_from_line(line, 'moke_sn')
            # 回调判断&组合
            if 'DOT_ASR_WORK_READY' in line:                                    # 无屏，有屏/codriver的非极客模式、极客的首次
                if len(tmpList):
                    asr_query_list.append(tmpList)
                tmpList = copy.deepcopy(globalVal._ASR_REQUEST)
                tmpList.update({
                    'asrReady': audio_time,
                })
                if match_sn is not None:
                    tmpList.update({'match_sn': match_sn})
                self.__asrFirstRequestCount += 1
            elif 'DOT_ASR_VAD_BEGIN' in line:
                if len(tmpList) == 0:                                           # 纯识别 第一次识别
                    tmpList = copy.deepcopy(globalVal._ASR_REQUEST)
                    tmpList.update({
                        'vadBegin': audio_time,
                        'match_sn': match_sn
                    })
                elif match_sn == tmpList['match_sn']:
                    tmpList.update({'vadBegin': audio_time})
                elif tmpList['vadBegin'] is None and not globalVal.is_jikemode_sn(asr_sn):  # 有屏/codriver 首次识别
                    self.match_correct_asr_round(asr_query_list, match_sn, {'vadBegin': audio_time})
                else:                                                           # 有屏/codriver 极客模式的2~N次识别
                    asr_query_list.append(tmpList)
                    tmpList = copy.deepcopy(globalVal._ASR_REQUEST)
                    tmpList.update({
                        'vadBegin': audio_time,
                        'match_sn': match_sn
                    })
            elif 'DOT_ASR_FINAL_RESULT' in line or 'DOT_ASR_ERROR' in line:
                errCode = str(_get_param_from_line(line, 'asr_error_code'))
                if str(errCode) == '0':
                    errCode = None
                if 'DOT_ASR_FINAL_RESULT' in line:
                    result = {
                        'asrFinalResult': audio_time,
                        'asr_result': _get_param_from_line(line, 'asr_result'),
                        'asr_corpus_id': _get_param_from_line(line, 'asr_corpus_id'),
                        'errCode': errCode,
                        'semantics_index': _get_param_from_line(line, 'semantics_index'),
                        'asr_reject': _get_param_from_line(line, 'asr_reject'),
                        'reject_type': _get_param_from_line(line, 'reject_type'),
                        'state': _get_param_from_line(line, 'state'),
                        'direction_invalid': _get_param_from_line(line, 'direction_invalid')
                    }
                    if self.speech_type == globalVal.SpeechType.ROLE_ASR:
                        result.update({
                            'asr_role': asr_sn.split('role_')[1].split('_')[0]
                        })
                else:
                    if errCode is None:
                        result = {
                            'asrError': None,
                            'errCode': None
                        }
                    else:
                        if len(errCode) == 1:
                            errCode += '_' + str(_get_param_from_line(line, 'asr_error_domain'))
                        result = {
                            'asrError': audio_time,
                            'errCode': errCode
                        }
                if asr_sn is not None:
                    result.update({'asr_sn': asr_sn})
                if len(tmpList):
                    if match_sn == tmpList['match_sn']:
                        tmpList.update(result)
                    elif not self.match_correct_asr_round(asr_query_list, match_sn, result):
                        if tmpList['asrReady'] is not None and tmpList['match_sn'] is None:
                            tmpList.update(result)
                        elif tmpList['vadBegin'] is None:                           # RTOS 非第一次识别
                            asr_query_list.append(tmpList)
                            tmpList = copy.deepcopy(globalVal._ASR_REQUEST)
                            tmpList.update(result)
                        else:
                            logging.error(str(result) + ' 未找到匹配结果')
                else:                                                           # RTOS 第一次识别
                    tmpList = copy.deepcopy(globalVal._ASR_REQUEST)
                    tmpList.update(result)
                if result['errCode'] is not None and str(result['errCode']) != '0':
                    if asr_sn and globalVal.is_jikemode_sn(asr_sn):
                        self.__asrMultiError.append(result['errCode'])
                    else:
                        self.__asrFirstError.append(result['errCode'])
            elif 'DOT_ASR_IGNORE_XD' in line:  # 小度+指令词 已经在识别响应中，当前不再发起识别请求
                ignoreList = copy.deepcopy(globalVal._ASR_REQUEST)
                result = {
                    'asrIgnore': audio_time,
                    'asr_sn': _get_param_from_line(line, 'tagName')
                }
                ignoreList.update(result)
                asr_query_list.append(ignoreList)
            else:   # 其他普通回调
                result = {}
                if 'DOT_ASR_FIRST_PARTIAL' in line:
                    key = 'asrFirstPartial'
                elif 'DOT_ASR_FIRST_THIRD_DATA' in line:
                    key = 'asrFirstThirdData'
                elif 'DOT_ASR_FIRST_TTS' in line:
                    key = 'asrFirstTTS'
                    if 'voiceprint' in self.audio_scene:
                        result = {'vpResult': _get_param_from_line(line, 'tts_text')}
                elif 'DOT_ASR_RUNNING' in line:
                    key = 'asrRunning'
                elif 'DOT_ASR_VAD_END' in line:
                    key = 'vadEnd'
                    if globalVal.is_jikemode_sn(asr_sn):
                        self.__asrMultiRequestCount += 1
                elif 'DOT_ASR_END' in line:
                    key = 'recEnd'
                else:
                    logging.debug('未知回调名称:' + line)
                    continue
                result.update({key: audio_time})
                if match_sn is not None:
                    result.update({'match_sn': match_sn})
                if len(tmpList) == 0:
                    tmpList = copy.deepcopy(globalVal._ASR_REQUEST)
                    tmpList.update(result)
                elif match_sn is None or match_sn == tmpList['match_sn']:
                    tmpList.update(result)
                elif not self.match_correct_asr_round(asr_query_list, match_sn, result):
                    if tmpList['asrReady'] is not None and tmpList['match_sn'] is None:
                        tmpList.update(result)
                    else:
                        logging.error(str(result) + ' 未找到匹配结果')
        if len(tmpList):
            asr_query_list.append(tmpList)

        return asr_query_list

    def match_correct_asr_round(self, asr_query_list, match_sn, result_list):
        """从asr_query_list里，根据match_sn寻找匹配的query，并把result_list里的值更新进去
        """
        find_flag = False
        for query in asr_query_list:
            if match_sn == query['match_sn']:
                find_flag = True
                query.update(result_list)
                break
        if find_flag:
            return True
        return False
