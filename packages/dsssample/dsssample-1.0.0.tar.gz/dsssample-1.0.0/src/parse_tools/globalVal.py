#!/usr/bin/ python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
########################################################################

"""
    File: globalVal.py
    Author: dushuangshuang(dushuangshuang@baidu.com)
    Date: 2020/01/19 上午12:05
"""

import os
import sys, getopt
import time
import json
import re
import configparser
from enum import Enum
from collections import defaultdict
import copy
import shutil
from pathlib import Path


_NET_ERROR_CODE_LIST = [                # [网络错误码列表] 因网络原因导致失败的识别请求，不参与识别率统计; 本列表为有屏&无屏(含识别cancel)网络错误码
    '1000', '1001', '1002', '1003', '1004', '1005', '1006', 
    '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2100', '7002', 
    '-3001', '-3011', '-3014', '4_30', '4_31'
]
_DEBUG_MODE = False                     # 是否打开调试信息
_WORK_DIRECTORY = './result/'           # 统计结果输出目录(默认值)
_TOOL_DIR = './'                        # 脚本查询目录
_INFO_COUNT = 7                         # 默认信息列数，如SDK_1:jike-false_asr_oneshot_aj_1m/luqi，相关信息为aj、1m、luqi、SDK_1，总共4列
_ENVIRONMENT = 'Darwin'                 # wer工具使用平台
_TOOL_ACUCALC = {                       # wer执行目录、bin、conf指定
    'Darwin': {
        'dir': './tools/wer-client-mac-v2-191212/', 
        'bin': './wer-client-mac', 
        'conf': './conf/wer_client.conf'
    }, 
    'Linux': {
        'dir': './tools/wer-linux/', 
        'bin': './bin/wer'
    },
    'Windows': {
        'dir': './tools/wer-windows/',
        'bin': 'wer_client.py'
    }
}

_WP_DICT = {}.fromkeys(['queryCount', 'detectCount', 'rightCount', 'rightWordCount', 'rightIndexCount', 
    'totalTime', 'wpAvgTime'], 0)
_WP_DICT.update({'wpMaxTime': - sys.maxsize - 1, 'wp_speed_list': []})
_BASE_WHISPER= {}.fromkeys(['queryCount', 'detectCount', 'rightCount', 'normalCount', 'whisperCount', 
    'totalTime', 'wpAvgTime'], 0)
_BASE_WHISPER.update({'wpMaxTime': - sys.maxsize - 1, 'wp_speed_list': []})
_WHISPER_DICT = copy.deepcopy(_BASE_WHISPER)
_WHISPER_DICT.update({'whisperInfo': {}})
_ASR_REQUEST = {}.fromkeys([
    'asrIgnore', 'asrRunning', 'asrReady', 'vadBegin', 'vadEnd', 'recEnd', 
    'asrFirstPartial', 'asrFirstThirdData', 'asrFinalResult', 'asrFirstTTS', 
    'asr_result', 'asr_sn', 'asr_corpus_id', 'errCode', 'vpResult', 'vpAccuracy', 'direction_invalid', 
    'asrError', 'reject_type', 'asr_reject', 'state', 'match_sn'])
_REPORT_PARAM_LIST = {}.fromkeys([
    'wp_query_count', 'wp_count', 'wp_rate', 'false_wp_count', 
    'first_success_count', 'asr_count', 'success_count', 'recall_count', 
    'invalid_asr_request', 'valid_asr_request', 
    'false_asr_count', 'false_interact_count',
    'wp_time', 'partial_time', 'finish_time', 'tts_time', 
    'vad_start_time', 'vad_end_time', 'speed_query_num'], 0)
_REPORT_PARAM_LIST.update({'asr_recall_count': []})
_REPORT_KEY_LIST = ['wp_query_count', 'wp_count', 'wp_rate', 'false_wp_count', 'wp_time', 
    'asr_query_count', 'asr_count', 'invalid_asr_request_count', 'success_count', 'success_rate', 'false_asr_count', 
    'wer', 'ser', 
    'partial_time', 'finish_time', 'tts_time', 'vad_start_time', 'vad_end_time', 'speed_query_num', 
    'first_success_count']

_WORK_TITLE_LIST = ['SDK版本', '测试集名称', 
    '唤醒音频总条数', '唤醒对齐次数', '唤醒成功率', '误唤醒次数', '唤醒时间', 
    '识别音频总条数', '识别请求对齐次数', '无效识别请求次数/有效识别请求次数', 
    '召回次数/识别成功次数', '召回率/识别成功率', '误识别次数/误交互次数', 
    '字准', '句准', '识别首包上屏', '硬延迟', 'TTS首包返回', 'VAD起点', 'VAD尾点', '速度统计条数', 
    'asr_reject次数', 'acoustics_reject个数', 'semantics_reject个数', 'other_reject个数', 'voiceprint_rejcet个数', 
    '错误码详情', '首次识别请求成功次数']
_CODRIVER_WAK_PERFORM_LIST = ['唤醒词', '唤醒音频总条数', '唤醒对齐次数', '唤醒准确次数', '唤醒准确率', 
    '唤醒词误串次数', '唤醒词误串率', '音区误串次数', '音区误串率', '唤醒时间平均值', '唤醒时间最大值']
_XD_WAK_PERFORM_LIST = ['唤醒词', '唤醒音频总条数', '唤醒对齐次数', '唤醒准确次数', '唤醒准确率', 
    '唤醒词误串次数', '唤醒词误串率', '唤醒忽略次数', '唤醒时间平均值']
_QWQD_WAK_PERFORM_LIST = ['唤醒词', '唤醒类型', '唤醒音频总条数', '唤醒对齐次数', '正常应答次数', '轻声应答次数', 
    '唤醒率', '应答准确率', '唤醒时间平均值']
_ROLE_PERFORM_LIST = ['对话总回合数', '角色判定正确回合数', '角色判定正确率',
    '字准（仅统计角色正确判定的回合）', '字准（所有回合）']
_DETAIL_TITILE_LIST = ['唤醒词', 'Query答案', '识别结果', 'SN', 'CorpusID', '标注唤醒起点', '标注唤醒尾点', 
    '标注识别起点', '标注识别尾点', '', '唤醒触发', '识别首包', '最终结果上屏', 'TTS首包', 'VAD起点', 'VAD尾点', 
    '', '唤醒速度', '首包响应时间', '硬延迟时间', 'TTS首包时间', 'VAD起点时间', 'VAD尾点时间']
_VP_TITLE_LIST = {
    '集内': ["识别音频条数", "识别成功次数", "声纹判定总次数", "正确判定次数",
        "错误判定次数", "未识别次数", "正确识别率", "错误识别率", "未识别率"], 
    '集外': ["识别音频条数", "识别成功次数", "声纹判定总次数", "正确判定次数",
        "错误判定次数", "正确识别率", "错误识别率"]
}
_R_TITLE_LIST = ['模式', '类别', '场景', '距离/角度', '测试集', '版本']
_R_WAKEUP_LIST = ['唤醒音频总条数', '唤醒对齐次数', '唤醒率', '误唤醒次数', '唤醒速度']
_R_CODRIVER_WAK_LIST = ['唤醒词', '唤醒音频总条数', '唤醒对齐次数', '唤醒准确次数', '唤醒词误串次数', '音区误串次数',
    '唤醒时间平均值', '唤醒时间最大值', '唤醒准确率']
_R_XD_WAK_LIST = ['唤醒词', '唤醒音频总条数', '唤醒词正确次数', '唤醒词误串次数', '唤醒忽略次数']
_R_FALSE_WP_LIST = ['唤醒词', '误唤醒次数']
_R_CONTRAST_ASR_LIST = ['交集个数', '字准', '句准']
_R_CONTRAST_SEMANTICASR_LIST = ['交集个数', '识别准确率', '识别错误条数']
_R_INTERSECT_ASR_LIST = {
    'asr': ['识别音频总条数', '有效识别请求次数', '识别成功次数（错误码为0）',
        '识别成功率=识别成功次数/有效识别请求次数', '字准', '句准'],
    'mutiplyasr': ['识别音频总条数', '有效识别请求次数', '识别成功次数（错误码为0）',
        '识别成功率=识别成功次数/有效识别请求次数', 
        '召回次数', '召回率=召回次数/识别成功次数', '字准', '句准'],
    'pureasr': ['识别音频总条数', '有效识别请求次数', '识别成功次数（错误码为0）',
        '识别成功率=识别成功次数/有效识别请求次数', 
        '准召次数', '准召率=准召次数/识别成功次数', '字准', '句准'],
    'splitasr': ['识别音频总条数', '有效识别请求次数', '识别成功次数（错误码为0）',
        '识别成功率=识别成功次数/有效识别请求次数', '字准', '句准'],
    'semanticasr': ['识别音频总条数', '有效识别请求次数', '识别成功次数（错误码为0）',
        '识别成功率=识别成功次数/有效识别请求次数', '识别准确率', '识别错误条数']
}
_R_NONE_INTERSECT_ASR_LIST = {
    'asr': ['识别请求对齐次数', '无效识别请求次数', '有效识别请求次数',
        '识别成功次数（错误码为0）', '识别成功率=识别成功次数/有效识别请求次数', 
        '误识别次数', '字准', '句准'],
    'mutiplyasr': ['识别请求对齐次数', '无效识别请求次数', '有效识别请求次数',
        '识别成功次数（错误码为0）', '识别成功率=识别成功次数/有效识别请求次数', 
        '召回次数', '召回率=召回次数/识别成功次数', '首次识别成功次数', '首次识别成功率', 
        '误识别次数/误交互次数', '字准', '句准'],
    'pureasr': ['识别请求对齐次数', '无效识别请求次数', '有效识别请求次数',
        '识别成功次数（错误码为0）', '识别成功率=识别成功次数/有效识别请求次数', 
        '准召次数', '准召率=准召次数/识别成功次数', 
        '误识别次数/误交互次数', '字准', '句准'],
    'splitasr': ['识别请求对齐次数', '无效识别请求次数', '有效识别请求次数',
        '识别成功次数（错误码为0）', '识别成功率=识别成功次数/有效识别请求次数','字准', '句准'],
    'semanticasr': ['识别请求对齐次数', '无效识别请求次数', '有效识别请求次数',
        '识别成功次数（错误码为0）', '识别成功率=识别成功次数/有效识别请求次数', 
        '误识别次数', '识别准确率', '识别错误条数'],
    'roleasr': ['对话总回合数', '角色判定正确回合数', '角色判定正确率', 
        '字准（仅统计角色正确判定的回合）', '字准（所有回合）']
}
_R_SPEED_LIST = {
    'asr': ['识别速度统计条数', '识别首包上屏', '硬延迟', 'TTS首包返回', 'VAD起点', 'VAD尾点'],
    'mutiplyasr': ['识别速度统计条数', '识别首包上屏', '硬延迟', 'TTS首包返回', 'VAD起点', 'VAD尾点'],
    'pureasr': ['识别速度统计条数', '识别首包上屏', '硬延迟', 'TTS首包返回', 'VAD起点', 'VAD尾点'],
    'splitasr': ['首包响应时间平均值', '首包响应时间最大值', '首包响应时间最小值', '(final-end)平均值',
                  '(final-end)最大值', '(final-end)最小值', '初始化时间平均值', '初始化时间最大值', '初始化时间最小值',
                  'Traffic Total', 'Traffic Rx Total', 'Traffic Tx Total'],
    'semanticasr': ['识别速度统计条数', '识别首包上屏', '硬延迟', 'TTS首包返回', 'VAD起点', 'VAD尾点']
}
_R_INTERSECT_VP_LIST = {
    'voiceprint-jn': ['声纹判定总次数', '正确判定次数', '正确判定率', 
        '错误判定次数', '错误判定率', '未识别次数', '未识别率'],
    'voiceprint-jw': ['声纹判定总次数', '正确判定次数', '正确判定率', 
        '错误判定次数', '错误判定率', ],
}
_R_COMMON_VP_LIST = ['唤醒音频总条数', '唤醒对齐次数', 
    '识别音频总条数', '有效识别请求次数', '识别成功次数（错误码为0）']
_SPEED_ANALYSE_LIST = ['中位数', '90分位数', '标准差', '最小值', '最大值']
_ACU_ANALYSE_LIST = ['字准', '句准', '替换错误率', '删除错误率', '插入错误率']
_SPEED_TYPE = {
    'wp': {
        'wp_speed_list': '唤醒速度'
    },
    'asr': {
        'partial_speed': '识别首包速度',
        'finish_speed': '硬延迟',
        'tts_speed': 'TTS首包速度',
        'vad_start_speed': 'VAD起点检测延迟',
        'vad_end_speed': 'VAD尾点检测延迟'
    }
}


_DATABASE = {}                              # 所有集合、版本的测试数据(db中已有数据)
_AIEAP_JSON = {}                            # 所有场景、版本的关键对比结论(用于AI-EAP平台数据上传)
_VERSION_LIST = []                          # 输出结果列表:测试版本
_SAMPLE_LIST = {}                           # 输出结果列表:测试场景
_NEW_DICT = {}                              # 增量统计:新增统计版本、测试集信息
_WORKBOOK_DICT = {}                         # 场景.xls，用于记录每个测试集的详细信息
_DCI_AUDIO_WORK_PATH = ''                   # DCI第一次灌测目录地址
_RESULT_WORKBOOK_NAME = ''                  # 声学报告表格名称
_ERROR_RECORD_FILE_NAME = ''                # 识别错误码文件名称
_LOCATION_RECORD_FILE_NAME = ''             # 声源定位文件名称
_VP_RECORD_FILE_NAME = ''                   # 声纹文件名称
_INFO_RECORD_FILE_NAME = ''                 # 版本信息记录文件名称
_DATABASE_NAME = ''                         # 记录所有集合、版本的测试有效信息
_ERR_JSON_FILE_NAME = ''                    # 统计脚本执行错误码文件记录文件
_RESULT_FLAG = 0                            # 统计脚本执行结果，详细如下
                                            # 0 - succeed : 统计成功，有报告生成，不需要查看错误日志
                                            # 1 - finished : 统计完成，有报告生成，遇到一些问题，但是脚本统计时过滤掉了，需要查看错误日志
                                            # 2 - failed : 统计失败，无报告生成
_DISPLAY_BY_COL = False                     # 唤醒专项报告中，多唤醒词、指令词纵向展示（默认是False，横向展示）
_MANUAL_TEST_MODE = False                   # 人工测试

_PARAM = {
    'CONTRAST_WITH_ALL': True,              # [识别交集统计规则] True: 所有版本一起取交集; False: 两两取交集，每个版本都只与对比版本取交集
    'ASR_SN_WRITE_FLAG': True,              # [黑盒识别集保护] 识别SN、corpus_no是否写入excel，True: 写入excel; False: 不写
    'WRONG_WP_WORDS_RESTRICT': True,        # [query有效性统计规则] 唤醒词错误时，识别、DCI、声纹是否参与统计准确率。True: 不参与统计; False: 参与统计
    'AUDIO_FOR_SERVER_FLAG': False,         # [客户端服务端测试集共享] True: 打开; False: 关闭
    'SUPPORT_RESTRICT': [True, True, True], # [多次识别统计规则] True: 打开，False: 关闭; 总共3个规则，详细如下：
                                            # 未唤醒或误唤醒的不参与统计、首次无识别结果的不参与统计、首次有识别结果但是报网络错误的不参与统计
    'PARTIAL_TIME_RANGE': [0, 8000],        # [识别速度统计规则] 识别首包时间范围，该范围外时，不参与统计
    'FINAL_TIME_RANGE': [0, 8000],          # [识别速度统计规则] 硬延迟时间范围，该范围外时，不参与统计
    'TTS_TIME_RANGE': [1, 8000],            # [识别速度统计规则] TTS首包时间范围，该范围外时，不参与统计
    'PUREASR_ANGLE_RANGE': [-180, 180],     # [纯识别统计规则] 该范围内为角度内，其他情况为角度外
    'WP_LOCATION_RIGHT_RANGE': [-15, 15],   # [声源定位统计规则] 当「标注答案角度」和「信号定位角度」的差值，在WP_LOCATION_RIGHT_RANGE范围内时，认为定位正确；
    'WP_LOCATION_IN_RANGE': [-45, 45],      # 在WP_LOCATION_IN_RANGE范围内时，认为属于相邻灯位；否则认为定位错误；
    'DCI_TIME_RESTRICT': 500,               # [DCI统计规则] 多台设备唤醒时刻的差值 < 该值 时，认为多台设备是同一时刻唤醒，DCI组网成功；否则组网失败
    'WP_RATE_RULES': [-2, 3],               # [声学结论生成规则] 唤醒率 准出范围，单位：% 
    'FALSE_WP_RULES': [-5, 5],              # [声学结论生成规则] 误唤醒 准出范围，单位：% 
    'ASR_SUCCESS_RATE_RULES': [-1, 2],      # [声学结论生成规则] 识别成功率 准出范围，单位：% 
    'ASR_RECALL_RATE_RULES': [-2, 2],       # [声学结论生成规则] 多次识别召回率 准出范围，单位：% 
    'ASR_WER_RULES': [-2, 2],               # [声学结论生成规则] 识别字准 准出范围，单位：% 
    'ASR_SER_RULES': [-2, 2],               # [声学结论生成规则] 识别句准 准出范围，单位：% 
    'ASR_ERROR_CODE_RULES': [-1, 1],        # [声学结论生成规则] 识别错误码 准出范围，单位：%
    'VP_RIGHT_RATE_RULES': [-2, 2],         # [声学结论生成规则] 声纹判定正确率 准出范围，单位：% 
    'VP_WRONG_RATE_RULES': [-2, 2],         # [声学结论生成规则] 声纹判定错误率 准出范围，单位：% 
    'VP_UNRECG_RATE_RULES': [-2, 2]         # [声学结论生成规则] 声纹判定未识别率 准出范围，单位：% 
}


class SpeechType(Enum):                     # 声学灌测类型 : get_speech_type(sampleset_name)
    """语音唤醒、识别类型"""
    WP = 1                                  # 纯唤醒
    WP_LOCATION = 2                         # 声源定位
    DCI = 3                                 # DCI
    PUER_ASR = 4                            # 纯识别（大屏）
    SPLIT_ASR = 5                           # 单条识别（codriver）
    MULTI_ASR = 6                           # 多次识别
    ASR = 7                                 # 单次识别
    SEMANTIC_ASR = 8                        # 语义识别
    VOICE_PRINT = 9                         # 声纹
    WHISPER = 10                            # 轻问轻答
    OFFLINE_ASR = 11                        # 离线识别
    ROLE_ASR = 12                           # 听清识别 - 双人交互模式

SPEECH_MODE = {                             # 声学灌测模式 : 'wp'（纯唤醒）；'asr'（纯识别）；'wp+asr'（唤醒+识别）
    'wp': [
        SpeechType.WP, 
        SpeechType.WP_LOCATION, 
        SpeechType.DCI
    ],
    'asr': [
        SpeechType.PUER_ASR, 
        SpeechType.ROLE_ASR, 
        SpeechType.SPLIT_ASR
    ],
    'wp+asr': [
        SpeechType.MULTI_ASR, 
        SpeechType.ASR, 
        SpeechType.SEMANTIC_ASR, 
        SpeechType.OFFLINE_ASR, 
        SpeechType.VOICE_PRINT,
        SpeechType.WHISPER
    ]
}                       


def get_speech_type(sample_name):
    """
    得到测试类型
    【仅唤醒】1、普通唤醒；2、唤醒+声源定位；3、dci
    【仅识别】4、纯识别；5、单条识别
    【唤醒+识别】6、多次识别；7、单次识别；8、语义识别；9、声纹；
    """
    if 'whisper' in sample_name:
        return SpeechType.WHISPER
    elif 'asr' in sample_name:
        if 'mutiplyasr' in sample_name:
            return SpeechType.MULTI_ASR
        elif 'pureasr' in sample_name:
            return SpeechType.PUER_ASR
        elif 'roleasr' in sample_name:
            return SpeechType.ROLE_ASR
        elif 'split-audio' in sample_name:
            return SpeechType.SPLIT_ASR
        elif 'semanticasr' in sample_name:
            return SpeechType.SEMANTIC_ASR
        elif 'offlineasr' in sample_name:
            return SpeechType.OFFLINE_ASR
        else:
            return SpeechType.ASR
    elif 'wp' in sample_name:
        if 'wp_location' in sample_name:
            return SpeechType.WP_LOCATION
        elif 'wp_dci' in sample_name:
            return SpeechType.DCI
        else:
            return SpeechType.WP
    elif 'voiceprint' in sample_name:
        return SpeechType.VOICE_PRINT
    else:
        print(sample_name, '未知测试类型，请检查集合命名，不符合规范')
        record_err(sample_name, 1103, '未知测试类型，请检查集合命名，不符合规范', 2)
        return 0


def get_scene_list(scene_name):
    """
    得到测试场景和音频名称
    """
    last_scene = scene_name.split('_', 4)[-1]
    scene_name = scene_name.rsplit('_' + last_scene, 1)[0]
    scene_item = scene_name.rsplit('_', len(scene_name.split('_')) - 3)
    scene_list = []
    for item in scene_item + [last_scene]:
        scene_list.append(item)
    return scene_list


def get_scene_item(sampleset_name):
    """
    得到测试场景和音频名称
    """
    if '/' in sampleset_name:
        return sampleset_name.split('/')[0], sampleset_name.split('/')[1]
    else:
        print("非法测试集命名，请检查！！！")
        leng = len(sampleset_name.split('_'))
        if leng > 5:
            return sampleset_name.rsplit('_', leng - 5)[0], sampleset_name.split('_', 5)[-1]
        else:
            return sampleset_name, ''


def get_scene_name(sampleset_name):
    """
    拆分测试场景和距离
    """
    audio_scene, audio_name = get_scene_item(sampleset_name)
    if 'wp_dci' in audio_scene:
        length = len(audio_scene.split('_'))
        if length > 4:
            dci_audio = audio_scene.rsplit('_', 1)[0]
            dci_name = audio_scene.rsplit('_', 1)[1]
            return dci_audio, dci_name
        else:
            return audio_scene, audio_name
    else:
        return audio_scene, audio_name


def get_scene_info(sampleset_name):
    """
    拆分测试场景和距离
    """
    audio_scene, audio_name = get_scene_item(sampleset_name)
    if 'wp_dci' in audio_scene:
        dci_audio = audio_scene.rsplit('_', 1)[0]
        dci_name = audio_scene.rsplit('_', 1)[1]
        return [dci_audio, dci_name, audio_name.split('_')[0], audio_name.split('_')[1]]
    else:
        item = audio_scene.split('_')
        return [audio_scene, audio_name, item[4], None]


def get_dci_info(sampleset_name):
    """
    拆分DCI的测试场景、音频集唯一ID、版本组合
    """
    scane_name, audio_name = sampleset_name.split('/')
    enviroment = scane_name.split('_')[-1]
    if '_' in audio_name:
        dci_audio, dci_group = audio_name.split('_', 1)
        return enviroment, dci_audio, dci_group
    else:
        return enviroment, audio_name, ''
    

def get_save_path(audio_scene, audio_name=''):
    """
    测试数据归档路径
    """
    path = ''
    if 'wp_dci' in audio_scene:
        item = audio_scene.split('_')
        path = os.path.join(_WORK_DIRECTORY, item[1], item[2], item[3])
    else:
        item = audio_scene.split('_', 4)
        path = os.path.join(_WORK_DIRECTORY, item[1], item[2], item[3], item[4])
    if audio_name != '':
        path = os.path.join(path, audio_name)
    return path


def get_scene_data(sample_name, sdk_version=''):
    """
    获取对应集合的数据
    """
    scene_name, audio_name = get_scene_name(sample_name)
    scene_item = get_scene_list(scene_name)
    json_data = _DATABASE[scene_item[0]]
    for item in scene_item[1:]:
        json_data = json_data[item]
    if audio_name != '':
        json_data = json_data[audio_name]
    if sdk_version == '':
        return json_data
    else:
        return json_data[sdk_version]
    

def is_jikemode_sn(sn):
    """
    判断是否是极客模式的SN
    """
    if sn is None:
        return False
    if not '_' in sn or '_qc' in sn or 'DOT_ASR' in sn:
        return False
    else:
        return True


def save_result():
    """
    1、生成result.xlsx，供冰夷平台展示测试结论
    2、生成result.json，供EAP平台展示测试结论
    3、遍历answer目录，为共享给服务端的测试集添加条数
    """
    for workbook_path in _WORKBOOK_DICT:
        _WORKBOOK_DICT[workbook_path].save(workbook_path)
        
    if _RESULT_FLAG != 2:
        if os.path.exists(_RESULT_WORKBOOK_NAME):
            result_excel_name = _RESULT_WORKBOOK_NAME
        elif os.path.exists(os.path.join(_WORK_DIRECTORY, 'dci_perform.xlsx')):
            result_excel_name = os.path.join(_WORK_DIRECTORY, 'dci_perform.xlsx')
        shutil.copy(result_excel_name, os.path.join(_WORK_DIRECTORY, 'result.xlsx'))

    if len(_AIEAP_JSON):
        save_json_data(os.path.join(_WORK_DIRECTORY, 'result.json'), _AIEAP_JSON)

    answer_path = os.path.join(_WORK_DIRECTORY, 'server')
    if os.path.exists(answer_path):
        time_stamp = time.strftime('%Y%m%d')
        for txt_file in Path(answer_path).iterdir():
            file_path = Path(answer_path, txt_file)
            if '.txt' in txt_file.name and txt_file.is_file():
                count = get_row_count_of_txtfile(str(file_path))
                new_name = file_path.name.replace('.txt', '_' + str(count) + 'query_' + time_stamp + '.txt')\
                    .replace('-', '_')
                txt_file.rename(Path(txt_file.parent, new_name))


def record_err(address, code, description, flags=1):
    """
    记录统计错误信息
    """
    global _RESULT_FLAG
    _RESULT_FLAG = flags
    with open(_ERR_JSON_FILE_NAME, 'a+', encoding='utf-8') as f:
        err_info = '\t{\n' + \
            '\t\t"error_address" : "' + address + '",\n' + \
            '\t\t"error_code" : ' + str(code) + ',\n' + \
            '\t\t"error_description" : "' + description + '"\n' + \
            '\t}\n'
        f.write(err_info)
    f.close()


def parse_args(argv):
    """输入参数解析
    """
    global _WORK_DIRECTORY
    work_dir = _WORK_DIRECTORY
    dci_work_dir = ''
    conf_path = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:o:c:d:', ['help', 'in=', 'out=', 'conf=', 'dir='])
    except getopt.GetoptError:
        print('python parseAudioStreamPerfom.py answer_result_file_path -o <output_dir> -d <dci_dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python parseAudioStreamPerfom.py answer_result_file_path -o <output_dir> -d <dci_dir>')
            sys.exit()
        elif opt in ('-o', '--out'):
            work_dir = str(arg)
        elif opt in ('-c', '--conf'):
            conf_path = str(arg)
        elif opt in ('-d', '--dir'):
            dci_work_dir = str(arg)
    return work_dir, dci_work_dir, conf_path
        

def update_global_value(dci_path="", conf_path="", script_dir=""):
    """
    更新中间信息存储位置
    """
    global _DCI_AUDIO_WORK_PATH, _RESULT_WORKBOOK_NAME, _VERSION_LIST, _DATABASE_NAME
    global _ERROR_RECORD_FILE_NAME, _ERR_JSON_FILE_NAME, _RESULT_FLAG
    global _LOCATION_RECORD_FILE_NAME, _INFO_RECORD_FILE_NAME, _VP_RECORD_FILE_NAME
    global _DATABASE, _AIEAP_JSON, _VERSION_LIST, _SAMPLE_LIST, _NEW_DICT, _WORKBOOK_DICT
    global _PARAM, _WORK_DIRECTORY, _TOOL_DIR, _TOOL_ACUCALC
    # [0] clear parameters
    _RESULT_FLAG = 0
    _DATABASE = {}
    _AIEAP_JSON = {}
    _VERSION_LIST = []
    _SAMPLE_LIST = {}
    _NEW_DICT = {}
    _WORKBOOK_DICT = {}
    # [1] init path
    if script_dir != '':
        script_dir = os.path.dirname(script_dir)
    if script_dir == '.' or script_dir == '':
        script_dir = os.getcwd()
    _TOOL_DIR = os.path.join(script_dir, _TOOL_DIR)
    for platform in _TOOL_ACUCALC:
        _TOOL_ACUCALC[platform]['dir'] = os.path.join(script_dir, _TOOL_ACUCALC[platform]['dir'])
    _WORK_DIRECTORY = os.path.abspath(_WORK_DIRECTORY)
    _RESULT_WORKBOOK_NAME = os.path.join(_WORK_DIRECTORY, '统计结果.xlsx')
    _ERROR_RECORD_FILE_NAME = os.path.join(_WORK_DIRECTORY, '错误码记录.txt')
    _ERR_JSON_FILE_NAME = os.path.join(_WORK_DIRECTORY, 'error_info.txt')
    _LOCATION_RECORD_FILE_NAME = os.path.join(_WORK_DIRECTORY, '声源定位结果记录.txt')
    _VP_RECORD_FILE_NAME = os.path.join(_WORK_DIRECTORY, '声纹判别结果记录.txt')
    _INFO_RECORD_FILE_NAME = os.path.join(_WORK_DIRECTORY, '测试信息记录.txt')
    _DCI_AUDIO_WORK_PATH = dci_path
    _DATABASE_NAME = os.path.join(_WORK_DIRECTORY, 'stream_data')
    # [2] init configuration
    if os.path.exists(conf_path):
        with open(conf_path, 'r', encoding='utf-8') as conf_file:
            for line in conf_file:
                line = line.strip()
                if line == '':
                    continue
                _VERSION_LIST.append(line)
    config_parser(_PARAM)


def get_row_count_of_txtfile(file_path, encoding='utf-8'):
    """
    得到txt文本的行数
    """
    if os.path.exists(file_path):
        count = -1
        f = open(file_path, 'r', encoding='utf-8')
        for count, line in enumerate(f):
            count += 1
        if count == -1:
            count = 0
        f.close()
        return count
    else:
        return 0


def init_defalutdict(layer):
    """
    初始化指定层数的dict
    """
    default_dict = {}
    for i in range(layer):
        default_dict = defaultdict(lambda: default_dict)
    return default_dict


def save_json_data(json_file_name, data):
    """
    通用函数: json格式规范化后, 重新写入文件
    """
    if os.path.exists(json_file_name):
        os.remove(json_file_name)
    json_file = open(json_file_name, 'w', encoding='utf-8')
    json_data = json.dumps(data, indent=4, ensure_ascii=False, separators=(',', ': '))
    json_file.write(json_data)
    json_file.close()


def listToString(initList, key=''):
    """
    把list中的值按key分割，拼接成一个string
    """
    listString = ''
    for values in initList[:-1]:
        listString += values + key
    listString += initList[-1]
    return listString


def getLength(value):
    """
    得到utf8字符串长度
    """
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def str_2_bool(in_str):
    """string 转 bool"""
    if isinstance(in_str, list):
        out_str = []
        for item in in_str:
            if item in ['True', 'true', '1']:
                out_str.append(True)
            else:
                out_str.append(False)
        return out_str
    else:
        if in_str in ['True', 'true', '1']:
            return True
        else:
            return False


def get_value(in_str, type):
    """解析匹配参数"""
    x = None
    if '[' in in_str:
        if 'None' in in_str:
            x = [None, None]
        else:
            x = re.split(r',|\[|\]|\ ', in_str)
            x = [i for i in x if(len(str(i))!=0)]
            if type == 'int':
                x = list(map(int, x))
            elif type == 'bool':
                x = str_2_bool(x)
    else:
        if type == 'int':
            x = int(in_str)
        elif type == 'bool':
            x = str_2_bool(in_str)
    return x


def config_parser(param):
    """读取并赋值匹配参数"""
    parse_conf = os.path.join(_TOOL_DIR, 'parse.conf')
    if os.path.exists(parse_conf):
        config = configparser.ConfigParser()
        config.read(parse_conf, encoding='utf-8')
        for key in param:
            if config.has_option('parse', key):
                if isinstance(param[key], bool) or key == 'SUPPORT_RESTRICT':
                    param[key] = get_value(config.get('parse', key), 'bool')
                else:
                    param[key] = get_value(config.get('parse', key), 'int')
