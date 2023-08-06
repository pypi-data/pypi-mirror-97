# -*- coding: utf-8 -*-
# @CreateTime : 2020/1/19 13:03
# @Author     : Liu Gang
# @File       : zllrp_prot_lib.py
# @Software   : PyCharm
import struct
import yaml
from ZLLRP.compat import std_str, conv_bytes_str, PY3

_PARAM = "parameter"
_TYPE_U1 = 1
_TYPE_U3 = 3
_TYPE_U4 = 4
_TYPE_U5 = 5
_TYPE_U6 = 6
_TYPE_U7 = 7
_TYPE_U8 = 8
_TYPE_U16 = 16
_TYPE_U32 = 32
_TYPE_U64 = 64
_TYPE_S8 = 0.08
_TYPE_S16 = 0.16
_TYPE_S32 = 0.32
_TYPE_S64 = 0.64
_TYPE_S1V = -1
_TYPE_UTF8V = -8
_TYPE_S16V = -16
_TYPE_S32V = -32

_UV_BASE = -80
_TYPE_U1V = -10
_TYPE_U8V = _UV_BASE
_TYPE_U16V = _UV_BASE * 2
_TYPE_U32V = _UV_BASE * 4

_COUNT_1 = "1"
_COUNT_0_1 = "0-1"
_COUNT_1_N = "1-N"
_COUNT_0_N = "0-N"

struct_format_dict = {
    _TYPE_U8: 'B', _TYPE_U8V: 'B',
    _TYPE_U16: '!H', _TYPE_U16V: 'H',
    _TYPE_U32: '!I', _TYPE_U32V: 'I',
    _TYPE_U64: '!Q',
    _TYPE_S8: 'b',
    _TYPE_S16: '!h',
    _TYPE_S32: '!i',
    _TYPE_S64: '!q',
}


class ZLLRP:
    def __init__(self, json_path="./"):
        self.msg_header_fmt = "!QBHII"
        self.par_header_fmt = "!HH"
        self.msg_header_len = struct.calcsize(self.msg_header_fmt)
        self.par_header_len = struct.calcsize(self.par_header_fmt)

        self.fpdh_list = ["京", "津", "冀", "晋", "蒙", "辽", "吉", "黑", "沪", "苏", "浙", "皖", "闽", "赣",
                          "鲁", "豫", "鄂", "湘", "粤", "桂", "琼", "渝", "川", "贵", "云", "藏", "陕", "甘",
                          "青", "宁", "新", "港", "澳"]

        try:
            with open(json_path + "mssage_list_map.json", "r") as fp:
                print("Using json File Config")
                self.message_list_map = yaml.safe_load(fp)
        except IOError:
            self.message_list_map = [
                {
                    'msg_type': 300,
                    'msg_name': 'Keepalive',
                    'msg_par': []
                }, {
                    'msg_type': 301,
                    'msg_name': 'KeepaliveAck',
                    'msg_par': []
                }, {
                    'msg_type': 302,
                    'msg_name': 'DeviceEventNotification',
                    'msg_par': [
                        {'name': 'UTCTimestamp', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'GPIEvent', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SelectSpecEvent', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AntennaSpecEvent', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AntennaStatusEvent', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'ConnectionAttemptEvent', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                    ]
                }, {
                    'msg_type': 303,
                    'msg_name': 'Disconnect',
                    'msg_par': []
                }, {
                    'msg_type': 304,
                    'msg_name': 'DisconnectAck',
                    'msg_par': []
                }, {
                    'msg_type': 400,
                    'msg_name': 'AddSelectSpec',
                    'msg_par': [
                        {'name': 'SelectSpec', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 401,
                    'msg_name': 'AddSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 402,
                    'msg_name': 'DeleteSelectSpec',
                    'msg_par': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 403,
                    'msg_name': 'DeleteSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 404,
                    'msg_name': 'StartSelectSpec',
                    'msg_par': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 405,
                    'msg_name': 'StartSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 406,
                    'msg_name': 'StopSelectSpec',
                    'msg_par': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 407,
                    'msg_name': 'StopSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 408,
                    'msg_name': 'EnableSelectSpec',
                    'msg_par': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 409,
                    'msg_name': 'EnableSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 410,
                    'msg_name': 'DisableSelectSpec',
                    'msg_par': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 411,
                    'msg_name': 'DisableSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 412,
                    'msg_name': 'GetSelectSpec',
                    'msg_par': []
                }, {
                    'msg_type': 413,
                    'msg_name': 'GetSelectSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'SelectSpec', 'par_kind': _PARAM, 'count': _COUNT_0_N}
                    ]
                }, {
                    'msg_type': 450,
                    'msg_name': 'AddAccessSpec',
                    'msg_par': [
                        {'name': 'AccessSpec', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 451,
                    'msg_name': 'AddAccessSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 452,
                    'msg_name': 'DeleteAccessSpec',
                    'msg_par': [
                        {'name': 'AccessSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 453,
                    'msg_name': 'DeleteAccessSpecAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 500,
                    'msg_name': 'TagSelectAccessReport',
                    'msg_par': [
                        {'name': 'TagReportData', 'par_kind': _PARAM, 'count': _COUNT_0_N}
                    ]
                }, {
                    'msg_type': 660,
                    'msg_name': 'GetDeviceConfig',
                    'msg_par': [
                        {'name': 'RequestedData', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 661,
                    'msg_name': 'GetDeviceConfigAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'Identification', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'DeviceEventNotificationSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AlarmConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AntennaProperties', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'AntennaConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'ModuleDepth', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SelectReportSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AccessReportSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'CommunicationConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'LocationConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SecurityModuleConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'msg_type': 662,
                    'msg_name': 'SetDeviceConfig',
                    'msg_par': [
                        {'name': 'ResetToFactoryDefault', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1},
                        {'name': 'Identification', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'DeviceEventNotificationSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AlarmConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AntennaConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'ModuleDepth', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SelectReportSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AccessReportSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'CommunicationConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'LocationConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SecurityModuleConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'msg_type': 663,
                    'msg_name': 'SetDeviceConfigAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 700,
                    'msg_name': 'GetVersion',
                    'msg_par': [
                        {'name': 'VerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'msg_type': 701,
                    'msg_name': 'GetVersionAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'VersionInfo', 'par_kind': _PARAM, 'count': _COUNT_0_N},

                    ]
                }, {
                    'msg_type': 740,
                    'msg_name': 'DiagnosticTest',
                    'msg_par': [
                        {'name': 'DiagnosticTestItem', 'par_kind': _PARAM, 'count': _COUNT_1_N}
                    ]
                }, {
                    'msg_type': 741,
                    'msg_name': 'DiagnosticTestAck',
                    'msg_par': [
                        {'name': 'Status', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'DiagnosticTestResultItem', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                    ]
                }
            ]

        try:
            with open(json_path + "parameter_list_map.json", "r") as fp:
                self.parameter_list_map = yaml.safe_load(fp)
        except IOError:
            self.parameter_list_map = [
                {
                    'par_type': 300,
                    'par_name': 'Status',
                    'par_item': [
                        {'name': 'StatusCode', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'ErrorDescription', 'par_kind': _TYPE_UTF8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 301,
                    'par_name': 'UTCTimestamp',
                    'par_item': [
                        {
                            'name': 'Microseconds', 'par_kind': _TYPE_U64, 'count': _COUNT_1
                        }
                    ]
                }, {
                    'par_type': 302,
                    'par_name': 'GPIEvent',
                    'par_item': [
                        {'name': 'GPIPortNumber', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'GPIEvent', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 303,
                    'par_name': 'SelectSpecEvent',
                    'par_item': [
                        {'name': 'EventType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'PreemptingSelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 304,
                    'par_name': 'AntennaSpecEvent',
                    'par_item': [
                        {'name': 'EventType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'SpecIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 305,
                    'par_name': 'AntennaStatusEvent',
                    'par_item': [
                        {'name': 'EventType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 306,
                    'par_name': 'ConnectionAttemptEvent',
                    'par_item': [
                        {'name': 'ConnectionStatus',
                         'par_kind': _TYPE_U16,
                         'count': _COUNT_1
                         }
                    ]
                }, {
                    'par_type': 400,
                    'par_name': 'SelectSpec',
                    'par_item': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'Priority', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'CurrentState', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'Persistence', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1},
                        {'name': 'SelectSpecStartTrigger', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'SelectSpecStopTrigger', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'AntennaSpec', 'par_kind': _PARAM, 'count': _COUNT_1_N},
                        {'name': 'SelectReportSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 401,
                    'par_name': 'SelectSpecStartTrigger',
                    'par_item': [
                        {'name': 'SelectSpecStartTriggerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'PeriodicTrigger', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'GPITrigger', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                },
                {
                    'par_type': 402,
                    'par_name': 'PeriodicTrigger',
                    'par_item': [
                        {'name': 'Offset', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'Period', 'par_kind': _TYPE_U32, 'count': _COUNT_0_1},
                        {'name': 'UTCTimestamp', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 403,
                    'par_name': 'GPITrigger',
                    'par_item': [
                        {'name': 'GPIPortNum', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'GPIEvent', 'par_kind': _TYPE_U1, 'count': _COUNT_0_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_0_1},
                        {'name': 'Timeout', 'par_kind': _TYPE_U32, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 404,
                    'par_name': 'SelectSpecStopTrigger',
                    'par_item': [
                        {'name': 'SelectSpecStopTriggerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'DurationValue', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'GPITrigger', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 405,
                    'par_name': 'AntennaSpec',
                    'par_item': [
                        {'name': 'AntennaIDs', 'par_kind': _TYPE_U8V, 'count': _COUNT_1},
                        {'name': 'AntennaSpecStopTrigger', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'RfSpec', 'par_kind': _PARAM, 'count': _COUNT_1_N}
                    ]
                }, {
                    'par_type': 406,
                    'par_name': 'AntennaSpecStopTrigger',
                    'par_item': [
                        {'name': 'AntennaSpecStopTriggerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'DurationValue', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'GPITrigger', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'TagObservationTrigger', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 407,
                    'par_name': 'TagObservationTrigger',
                    'par_item': [
                        {'name': 'TriggerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'NumberOfTags', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'NumberOfAttempts', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'TValue', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'Timeout', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 408,
                    'par_name': 'RfSpec',
                    'par_item': [
                        {'name': 'RfSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'ProtocolID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'SelectType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'MemoryBank', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AntennaConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_N}
                    ]
                }, {
                    'par_type': 409,
                    'par_name': 'MemoryBank',
                    'par_item': [
                        {'name': 'MemoryBankID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'ReadType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'Pointer', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'Count', 'par_kind': _TYPE_U16, 'count': _COUNT_0_1},
                        {'name': 'BankType', 'par_kind': _TYPE_U8, 'count': _COUNT_0_N}
                    ]
                }, {
                    'par_type': 410,
                    'par_name': 'SelectReportSpec',
                    'par_item': [
                        {'name': 'SelectReportTrigger', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'NValue', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'EnableSelectSpecID', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableSpecIndex', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableRfSpecID', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableAntennaID', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnablePeakRSSI', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableFirstSeenTimestamp', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableLastSeenTimestamp', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableTagSeenCount', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableAccessSpecID', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableProtocolID', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'EnableTagSpeed', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U5, 'count': _COUNT_1},
                        {'name': 'ReportDestination', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                    ]
                }, {
                    'par_type': 411,
                    'par_name': 'ReportDestination',
                    'par_item': [
                        {'name': 'CommLinkConfiguration', 'par_kind': _PARAM, 'count': _COUNT_1_N}
                    ]
                }, {
                    'par_type': 450,
                    'par_name': 'AccessSpec',
                    'par_item': [
                        {'name': 'AccessSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'ProtocolID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'CurrentState', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Persistence', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U6, 'count': _COUNT_1},
                        {'name': 'AccessSpecStopTrigger', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'AccessCommand', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'AccessReportSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 451,
                    'par_name': 'AccessSpecStopTrigger',
                    'par_item': [
                        {'name': 'AccessSpecStopTriggerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'OperationCountValue', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 452,
                    'par_name': 'AccessCommand',
                    'par_item': [
                        {'name': 'HbMatchSpec', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'HbReadSpec', 'par_kind': _PARAM, 'count': _COUNT_1_N},
                        {'name': 'HbWriteSpec', 'par_kind': _PARAM, 'count': _COUNT_1_N},
                        {'name': 'HbPrivateWriteSpec', 'par_kind': _PARAM, 'count': _COUNT_1_N},
                        {'name': 'ClientRequestSpec', 'par_kind': _PARAM, 'count': _COUNT_1_N},
                        {'name': 'SecurityModuleSpec', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                    ]
                }, {
                    'par_type': 453,
                    'par_name': 'HbMatchSpec',
                    'par_item': [
                        {'name': 'HbTargetTag', 'par_kind': _PARAM, 'count': _COUNT_1_N}
                    ]
                }, {
                    'par_type': 454,
                    'par_name': 'HbTargetTag',
                    'par_item': [
                        {'name': 'MemoryType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'MatchType', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1},
                        {'name': 'TagMask', 'par_kind': _TYPE_U1V, 'count': _COUNT_1},
                        {'name': 'TagData', 'par_kind': _TYPE_U1V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 457,
                    'par_name': 'AccessReportSpec',
                    'par_item': [
                        {'name': 'AccessReportTrigger', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'ReportDestination', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 500,
                    'par_name': 'TagReportData',
                    'par_item': [
                        {'name': 'TID', 'par_kind': _TYPE_U8V, 'count': _COUNT_1},
                        {'name': 'SelectSpecID', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SpecIndex', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'RfSpecID', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AntennaID', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'PeakRSSI', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'FirstSeenTimestampUTC', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'LastSeenTimestampUTC', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'TagSeenCount', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'AccessSpecID', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'ProtocolID', 'par_kind': _PARAM, 'count': _COUNT_0_1},  # Add for dual mod
                        {'name': 'TagSpeed', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        # Add for dual mod 200304 Liugang
                        {'name': 'GenaralSelectSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'CustomizedSelectSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'HbReadSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'HbCustomizedReadSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'HbWriteSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'HbPrivateWriteSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'ClientRequestSpecResult', 'par_kind': _PARAM, 'count': _COUNT_0_N}
                    ]
                }, {
                    'par_type': 501,
                    'par_name': 'SelectSpecID',
                    'par_item': [
                        {'name': 'SelectSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 502,
                    'par_name': 'SpecIndex',
                    'par_item': [
                        {'name': 'SpecIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 503,
                    'par_name': 'RfSpecID',
                    'par_item': [
                        {'name': 'RfSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 504,
                    'par_name': 'AntennaID',
                    'par_item': [
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 505,
                    'par_name': 'PeakRSSI',
                    'par_item': [
                        {'name': 'PeakRSSI', 'par_kind': _TYPE_S8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 506,
                    'par_name': 'FirstSeenTimestampUTC',
                    'par_item': [
                        {'name': 'FirstSeenTimestampUTC', 'par_kind': _TYPE_U64, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 507,
                    'par_name': 'LastSeenTimestampUTC',
                    'par_item': [
                        {'name': 'LastSeenTimestampUTC', 'par_kind': _TYPE_U64, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 508,
                    'par_name': 'TagSeenCount',
                    'par_item': [
                        {'name': 'TagSeenCount', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 509,
                    'par_name': 'AccessSpecID',
                    'par_item': [
                        {'name': 'AccessSpecID', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1518,
                    'par_name': 'ProtocolID',
                    'par_item': [
                        {'name': 'ProtocolID', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 41479,
                    'par_name': 'TagSpeed',
                    'par_item': [
                        {'name': 'TagSpeed', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 510,
                    'par_name': 'GenaralSelectSpecResult',
                    'par_item': [
                        {'name': 'Result', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'TagData', 'par_kind': _TYPE_U16V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 517,
                    'par_name': 'CustomizedSelectSpecResult',
                    'par_item': [
                        {'name': 'Result', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'ReadDataInfo', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 511,
                    'par_name': 'HbReadSpecResult',
                    'par_item': [
                        {'name': 'Result', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'OpSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'ReadData', 'par_kind': _TYPE_U16V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 512,
                    'par_name': 'ClientRequestSpecResult',
                    'par_item': [
                        {'name': 'OpSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 513,
                    'par_name': 'HbWriteSpecResult',
                    'par_item': [
                        {'name': 'Result', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'ResultDescription', 'par_kind': _TYPE_U8V, 'count': _COUNT_1},
                        {'name': 'OpSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 514,
                    'par_name': 'HbPrivateWriteSpecResult',
                    'par_item': [
                        {'name': 'Result', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'ResultDescription', 'par_kind': _TYPE_U8V, 'count': _COUNT_1},
                        {'name': 'OpSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 515,
                    'par_name': 'HbCustomizedReadSpecResult',
                    'par_item': [
                        {'name': 'Result', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'OpSpecID', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'ReadDataInfo', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 516,
                    'par_name': 'ReadDataInfo',
                    'par_item': [
                        {'name': 'CID', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'FPDH', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SYXZ', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'CCRQ', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'CLLX', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'PL', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'GL', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'HPZL', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'HPHMXH', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'JYYXQ', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'QZBFQ', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'CSYS', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'ZKZL', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 660,
                    'par_name': 'DeviceEventNotificationSpec',
                    'par_item': [
                        {'name': 'EventNotificationState', 'par_kind': _PARAM, 'count': _COUNT_1_N}
                    ]
                }, {
                    'par_type': 661,
                    'par_name': 'EventNotificationState',
                    'par_item': [
                        {'name': 'EventType', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'NotificationState', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 662,
                    'par_name': 'AntennaProperties',
                    'par_item': [
                        {'name': 'AntennaConnected', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1},
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AntennaGain', 'par_kind': _TYPE_S16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 663,
                    'par_name': 'AntennaConfiguration',
                    'par_item': [
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'TransmitPowerIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'FrequencyIndexes', 'par_kind': _TYPE_U16V, 'count': _COUNT_1},
                        {'name': 'ForDataRateIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'RevDataRateIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'ForModulationIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'RevDataEncodingIndex', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 664,
                    'par_name': 'ModuleDepth',
                    'par_item': [
                        {'name': 'Index', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 665,
                    'par_name': 'Identification',
                    'par_item': [
                        {'name': 'DeviceName', 'par_kind': _TYPE_UTF8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 666,
                    'par_name': 'AlarmConfiguration',
                    'par_item': [
                        {'name': 'AlarmMask', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AlarmThreshod', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 667,
                    'par_name': 'AlarmThreshod',
                    'par_item': [
                        {'name': 'TemperatureMaxValue', 'par_kind': _TYPE_S8, 'count': _COUNT_1},
                        {'name': 'TemperatureMinValue', 'par_kind': _TYPE_S8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 668,
                    'par_name': 'CommunicationConfiguration',
                    'par_item': [
                        {'name': 'CommLinkConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'EthernetIpv4Configuration', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'EthernetIpv6Configuration', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'SerialPortConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_N},
                        {'name': 'NTPConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 669,
                    'par_name': 'CommLinkConfiguration',
                    'par_item': [
                        {'name': 'LinkType', 'par_kind': _TYPE_U8, 'count': _COUNT_0_N},
                        {'name': 'KeepaliveSpec', 'par_kind': _PARAM, 'count': _COUNT_1},
                        {'name': 'TcpLinkConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SerialLinkConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'HttpLinkConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 670,
                    'par_name': 'KeepaliveSpec',
                    'par_item': [
                        {'name': 'KeepaliveTriggerType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'PeriodicTriggerValue', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 671,
                    'par_name': 'TcpLinkConfiguration',
                    'par_item': [
                        {'name': 'CommMode', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'IsSSL', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1},
                        {'name': 'ClientModeConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'ServerModeConfiguration', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 672,
                    'par_name': 'ClientModeConfiguration',
                    'par_item': [
                        {'name': 'Port', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'IPAddress', 'par_kind': _PARAM, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 673,
                    'par_name': 'IPAddress',
                    'par_item': [
                        {'name': 'Version', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'Address', 'par_kind': _TYPE_U32V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 674,
                    'par_name': 'ServerModeConfiguration',
                    'par_item': [
                        {'name': 'Port', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 675,
                    'par_name': 'SerialLinkConfiguration',
                    'par_item': [
                        {'name': 'IfIndex', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'SrcAddr', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'DstAddr', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 676,
                    'par_name': 'HttpLinkConfiguration',
                    'par_item': [
                        {'name': 'ServerUrl', 'par_kind': _TYPE_UTF8V, 'count': _COUNT_1},
                    ]
                }, {
                    'par_type': 677,
                    'par_name': 'EthernetIpv4Configuration',
                    'par_item': [
                        {'name': 'IfIndex', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'IPAddress', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'IPMask', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'GateWayAddr', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'DNSAddr', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'IsDHCP', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 678,
                    'par_name': 'EthernetIpv6Configuration',
                    'par_item': [
                        {'name': 'IfIndex', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'IPAddress', 'par_kind': _TYPE_U32V, 'count': _COUNT_1},
                        {'name': 'IPMask', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'GateWayAddr', 'par_kind': _TYPE_U32V, 'count': _COUNT_1},
                        {'name': 'DNSAddr', 'par_kind': _TYPE_U32V, 'count': _COUNT_1},
                        {'name': 'IsDHCP', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 679,
                    'par_name': 'NTPConfiguration',
                    'par_item': [
                        {'name': 'NtpPeriodicTime', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'IPAddress', 'par_kind': _PARAM, 'count': _COUNT_1_N}
                    ]
                }, {
                    'par_type': 680,
                    'par_name': 'SerialPortConfiguration',
                    'par_item': [
                        {'name': 'IfIndex', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AttributeIndex', 'par_kind': _TYPE_U8, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 681,
                    'par_name': 'LocationConfiguration',
                    'par_item': [
                        {'name': 'LocationType', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'GpsLocation', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'BdsLocation', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 682,
                    'par_name': 'GpsLocation',
                    'par_item': [
                        {'name': 'Longitude', 'par_kind': _TYPE_S32, 'count': _COUNT_1},
                        {'name': 'Latitude', 'par_kind': _TYPE_S32, 'count': _COUNT_1},
                        {'name': 'Altitude', 'par_kind': _TYPE_S32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 683,
                    'par_name': 'BdsLocation',
                    'par_item': [
                        {'name': 'Longitude', 'par_kind': _TYPE_S32, 'count': _COUNT_1},
                        {'name': 'Latitude', 'par_kind': _TYPE_S32, 'count': _COUNT_1},
                        {'name': 'Altitude', 'par_kind': _TYPE_S32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 684,
                    'par_name': 'SecurityModuleConfiguration',
                    'par_item': [
                        {'name': 'GenaralConfigData', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'PrivateConfigData', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 685,
                    'par_name': 'GenaralConfigData',
                    'par_item': [
                        {'name': 'RTCTime', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'SecurityModuleSN', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'ReadMode', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 686,
                    'par_name': 'RTCTime',
                    'par_item': [
                        {'name': 'Seconds', 'par_kind': _TYPE_U64, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 687,
                    'par_name': 'SecurityModuleSN',
                    'par_item': [
                        {'name': 'SerialNumber', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 688,
                    'par_name': 'ReadMode',
                    'par_item': [
                        {'name': 'RepeatReadFlag', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1},
                        {'name': 'Timer', 'par_kind': _TYPE_U32, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 690,
                    'par_name': 'PrivateConfigData',
                    'par_item': [
                        {'name': 'ConfigData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 700,
                    'par_name': 'VersionInfo',
                    'par_item': [
                        {'name': 'VersionData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1},
                        {'name': 'UsedOrSpare', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'SetUse', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'HasRun', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'CanRun', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U4, 'count': _COUNT_1},
                        {'name': 'VerDescInfo', 'par_kind': _TYPE_UTF8V, 'count': _COUNT_1},
                    ]
                }, {
                    'par_type': 740,
                    'par_name': 'DiagnosticTestItem',
                    'par_item': [
                        {'name': 'DiagnosticTestID', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 741,
                    'par_name': 'DiagnosticTestResultItem',
                    'par_item': [
                        {'name': 'DiagnosticTestID', 'par_kind': _TYPE_U16, 'count': _COUNT_1},
                        {'name': 'DiagnosticTestResultCode', 'par_kind': _TYPE_U32, 'count': _COUNT_1},
                        {'name': 'DiagnosticTestResultAntennaConnected', 'par_kind': _PARAM, 'count': _COUNT_0_1},
                        {'name': 'DiagnosticTestResultAntennaVSWR', 'par_kind': _PARAM, 'count': _COUNT_0_1}
                    ]
                }, {
                    'par_type': 742,
                    'par_name': 'DiagnosticTestResultAntennaConnected',
                    'par_item': [
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AntennaConnected', 'par_kind': _TYPE_U1, 'count': _COUNT_1},
                        {'name': 'Reserved', 'par_kind': _TYPE_U7, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 743,
                    'par_name': 'DiagnosticTestResultAntennaVSWR',
                    'par_item': [
                        {'name': 'AntennaID', 'par_kind': _TYPE_U8, 'count': _COUNT_1},
                        {'name': 'AntennaVSWR', 'par_kind': _TYPE_U16, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1001, 'par_name': 'CID', 'par_item': [
                        {'name': 'CIDData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1002, 'par_name': 'FPDH', 'par_item': [
                        {'name': 'FPDHData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1003, 'par_name': 'SYXZ', 'par_item': [
                        {'name': 'SYXZData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1004, 'par_name': 'CCRQ', 'par_item': [
                        {'name': 'CCRQData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1005, 'par_name': 'CLLX', 'par_item': [
                        {'name': 'CLLXData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1006, 'par_name': 'GL', 'par_item': [
                        {'name': 'GLData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1007, 'par_name': 'PL', 'par_item': [
                        {'name': 'PLData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1008, 'par_name': 'HPZL', 'par_item': [
                        {'name': 'HPZLData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1009, 'par_name': 'HPHMXH', 'par_item': [
                        {'name': 'HPHMXHData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1010, 'par_name': 'JYYXQ', 'par_item': [
                        {'name': 'JYYXQData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1011, 'par_name': 'QZBFQ', 'par_item': [
                        {'name': 'QZBFQData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1012, 'par_name': 'ZKZL', 'par_item': [
                        {'name': 'ZKZLData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }, {
                    'par_type': 1013, 'par_name': 'CSYS', 'par_item': [
                        {'name': 'CSYSData', 'par_kind': _TYPE_U8V, 'count': _COUNT_1}
                    ]
                }
            ]

    def par_encode_proc(self, par_list, par_content):
        """
        根据参数类型,将待打包的字典进行打包
        @param par_list:
        @param par_content:
        @return:
        """
        par_content_encode = std_str()
        bits_count = 8
        byte_buffer = 0x00
        for par in par_list:
            par_item_name = par['name']  # 参数名
            par_item_kind = par['par_kind']  # 参数类型
            par_item_count = par['count']  # 参数个数
            if par_item_count == _COUNT_1:
                # 固定一个参数
                content_list = [par_content[par_item_name]]
            elif par_item_count == _COUNT_1_N:
                # 1~N个参数
                if type(par_content[par_item_name]) == list:
                    content_list = par_content[par_item_name]
                else:
                    content_list = [par_content[par_item_name]]
            elif par_item_count == _COUNT_0_1:
                # 0 ~ 1个参数
                try:
                    # 可能为0个参数,所以需抓取异常
                    content_list = [par_content[par_item_name]]
                except KeyError:
                    continue
            else:
                # 其他,即0~N个, 按照list进行打包
                try:
                    if type(par_content[par_item_name]) == list:
                        content_list = par_content[par_item_name]
                    else:
                        content_list = [par_content[par_item_name]]
                except KeyError:
                    continue

            for content in content_list:
                if par_item_kind == _PARAM:
                    # 类型为参数, 则进行递归打包
                    encode_ret = self.zllrp_par_encode(par_item_name, content)
                    if encode_ret is False:
                        continue
                    else:
                        par_content_encode += encode_ret
                elif par_item_kind == _TYPE_UTF8V:
                    str_len = len(content)
                    len_encode = struct.pack("!H", str_len)
                    str_encode = struct.pack("{0}s".format(str_len), content)
                    par_content_encode += len_encode + str_encode

                elif par_item_kind == _TYPE_U1V:
                    pass
                elif par_item_kind == _TYPE_U8V \
                        or par_item_kind == _TYPE_U16V \
                        or par_item_kind == _TYPE_U32V:
                    # 数组类型
                    arr_len = len(content)
                    len_encode = struct.pack("!H", arr_len)
                    arr_encode = std_str()
                    arr_format = "!{0}".format(struct_format_dict[par_item_kind])
                    for arr in content:
                        arr_encode += struct.pack(arr_format, arr)

                    par_content_encode += len_encode + arr_encode

                elif par_item_kind == _TYPE_U1 or \
                        par_item_kind == _TYPE_U3 or \
                        par_item_kind == _TYPE_U4 or \
                        par_item_kind == _TYPE_U5 or \
                        par_item_kind == _TYPE_U6 or \
                        par_item_kind == _TYPE_U7:
                    # bit类型根据不同长度打包, 由bits_count控制, 必须保证bits_count能到8位

                    bits_mask = 0xFF >> (8 - par_item_kind)
                    byte_value = (content & bits_mask) << (bits_count - par_item_kind)
                    byte_buffer += byte_value

                    bits_count -= par_item_kind
                    if bits_count == 0:
                        # 集齐8位,合成一个字节
                        par_content_encode += struct.pack('B', byte_buffer)
                        bits_count = 8
                        byte_buffer = 0x00
                else:
                    # 正常字节打包,根据字节长度打包
                    struct_encode = struct.pack(struct_format_dict[par_item_kind], content)
                    par_content_encode += struct_encode

        return par_content_encode

    def zllrp_msg_encode(self, dev_sn, msg_ver, msg_name, msg_id, msg_content):
        """
        消息打包.
        @param dev_sn:
        @param msg_ver:
        @param msg_name:
        @param msg_id:
        @param msg_content:
        @return:
        """
        for msg_items in self.message_list_map:
            # 找到对应的消息号的消息结构
            if msg_items['msg_name'] == msg_name:
                msg_type = msg_items['msg_type']
                msg_par_list = msg_items['msg_par']
                break
        else:
            print("msg {0} not found!".format(msg_name))
            return False

        # 对消息体进行编码
        msg_content_encode = self.par_encode_proc(msg_par_list, msg_content)

        msg_data = struct.pack(self.msg_header_fmt, dev_sn, msg_ver, msg_type, len(msg_content_encode),
                               msg_id) + msg_content_encode
        return msg_data

    def zllrp_par_encode(self, par_name, par_content):
        """
        参数打包
        @param par_name:
        @param par_content:
        @return:
        """
        for par_items in self.parameter_list_map:
            if par_items['par_name'] == par_name:
                par_type = par_items['par_type']
                par_list = par_items['par_item']
                break
        else:
            print("par {0} not found!".format(par_name))
            return False

        par_content_encode = self.par_encode_proc(par_list, par_content)

        par_data = struct.pack(self.par_header_fmt, par_type, len(par_content_encode)) + par_content_encode

        return par_data

    def msg_header_decode(self, data):
        """
        消息头解包
        @param data:
        @return:
        """
        body = data[0:self.msg_header_len]
        return struct.unpack(self.msg_header_fmt, body), data[self.msg_header_len:]

    def par_decode_proc(self, par_item_list, body_decode):
        """
        参数解包
        @param par_item_list: 参数list
        @param body_decode: 待解包串
        @return: 解包结果, 剩余待解包串
        """
        par_item_dict = dict()
        bits_count = 8
        for par_item in par_item_list:
            if len(body_decode) == 0:
                break
            # print(conv_bytes_str(body_decode))
            par_item_name = par_item['name']
            par_item_kind = par_item['par_kind']
            par_item_count = par_item['count']
            if par_item_kind == _PARAM:
                # 为参数类型,则递归解包
                if par_item_count == _COUNT_1 or par_item_count == _COUNT_0_1:
                    zllrp_par_ret, body_decode = self.zllrp_par_decode(par_item_name, body_decode)
                    if zllrp_par_ret is False:
                        continue
                    par_item_dict[par_item_name] = zllrp_par_ret
                else:
                    ret_item_list = list()
                    while len(body_decode) > 0:
                        # print("parm decode name:", par_item_name)
                        zllrp_par_ret, body_decode = self.zllrp_par_decode(par_item_name, body_decode)
                        if zllrp_par_ret is False:
                            break
                        ret_item_list.append(zllrp_par_ret)

                    if len(ret_item_list) != 0:
                        # print("Complete:", par_item_name)
                        par_item_dict[par_item_name] = ret_item_list

            elif par_item_kind == _TYPE_UTF8V:
                # UTF8 字符串
                (str_len,) = struct.unpack("!H", body_decode[:2])
                # print("str_len:", str_len)
                str_fmt = "{0}s".format(str_len)
                (par_item_dict[par_item_name],) = struct.unpack(str_fmt, body_decode[2:2 + str_len])
                body_decode = body_decode[2 + str_len:]

            elif par_item_kind == _TYPE_U8V \
                    or par_item_kind == _TYPE_U16V \
                    or par_item_kind == _TYPE_U32V:
                (str_len,) = struct.unpack("!H", body_decode[:2])
                ele_len = int(par_item_kind / _UV_BASE)
                ele_format = struct_format_dict[par_item_kind]
                str_fmt = "!{0}{1}".format(str_len, ele_format)
                # print(f"{str_fmt},{ele_len}")
                par_item_dict[par_item_name] = struct.unpack(str_fmt, body_decode[2:2 + str_len * ele_len])
                body_decode = body_decode[2 + str_len * ele_len:]

            # elif par_item_kind == _TYPE_U8V:
            #     # 单字节数组
            #     (str_len,) = struct.unpack("!H", body_decode[:2])
            #     str_fmt = "{0}B".format(str_len)
            #     par_item_dict[par_item_name] = struct.unpack(str_fmt, body_decode[2:2 + str_len])
            #     body_decode = body_decode[2 + str_len:]
            #
            # elif par_item_kind == _TYPE_U16V:
            #     (str_len,) = struct.unpack("!H", body_decode[:2])
            #     str_fmt = "!{0}H".format(str_len)
            #     par_item_dict[par_item_name] = struct.unpack(str_fmt, body_decode[2:2 + str_len * 2])
            #     body_decode = body_decode[2 + str_len * 2:]
            #
            # elif par_item_kind == _TYPE_U32V:
            #     (str_len,) = struct.unpack("!H", body_decode[:2])
            #     str_fmt = "!{0}I".format(str_len)
            #     par_item_dict[par_item_name] = struct.unpack(str_fmt, body_decode[2:2 + str_len * 4])
            #     body_decode = body_decode[2 + str_len * 4:]

            elif par_item_kind == _TYPE_U1V:
                (str_len,) = struct.unpack("!H", body_decode[:2])
                str_fmt = "{0}B".format(str_len)
                par_item_dict[par_item_name] = struct.unpack(str_fmt, body_decode[2:2 + str_len])
                body_decode = body_decode[2 + str_len:]

            elif par_item_kind == _TYPE_U1 or \
                    par_item_kind == _TYPE_U3 or \
                    par_item_kind == _TYPE_U4 or \
                    par_item_kind == _TYPE_U5 or \
                    par_item_kind == _TYPE_U6 or \
                    par_item_kind == _TYPE_U7:
                if PY3:
                    operate_byte = body_decode[0]
                else:
                    (operate_byte,) = struct.unpack('B', body_decode[0])
                bits_mask = 0xFF >> (8 - par_item_kind)
                shift_count = bits_count - par_item_kind
                par_item_dict[par_item_name] = operate_byte >> shift_count & bits_mask

                bits_count -= par_item_kind
                if bits_count <= 0:
                    bits_count = 8
                    body_decode = body_decode[1:]
            else:
                decode_len = struct.calcsize(struct_format_dict[par_item_kind])
                (par_item_dict[par_item_name],) = struct.unpack(struct_format_dict[par_item_kind],
                                                                body_decode[0:decode_len])
                body_decode = body_decode[decode_len:]

            # print("decode:", par_item_dict)

        return par_item_dict, body_decode

    def zllrp_msg_decode(self, data):
        try:
            (dev_sn, msg_ver, msg_type, msg_len, msg_id), body = self.msg_header_decode(data)
        except struct.error:
            return False
        else:
            for msg_items in self.message_list_map:
                if msg_items['msg_type'] == msg_type:
                    msg_name = msg_items['msg_name']
                    msg_par_list = msg_items['msg_par']
                    break
            else:
                print("msg {0} not found!".format(msg_type))
                return False
        ret_msg_dict = dict()
        # print("Decoding:", msg_name)
        (ret_msg_dict[msg_name], body) = self.par_decode_proc(msg_par_list, body)

        ret_msg_dict[msg_name]['DeviceSN'] = dev_sn
        ret_msg_dict[msg_name]['Ver'] = msg_ver
        ret_msg_dict[msg_name]['Type'] = msg_type
        ret_msg_dict[msg_name]['Len'] = msg_len
        ret_msg_dict[msg_name]['ID'] = msg_id
        # print("Final_Decode:", ret_msg_dict)

        if len(body) != 0:
            if data[0:7] != body[0:7]:
                print("drop msg:{0}".format(conv_bytes_str(body)))
                body = ""

        return ret_msg_dict, body

    def zllrp_par_decode(self, par_name, data):
        # print("zllrp_par_name:", par_name)
        # print("zllrp_par_decode:" + conv_bytes_str(data))

        for par_items in self.parameter_list_map:
            if par_items['par_name'] == par_name:
                par_type = par_items['par_type']
                par_item_list = par_items['par_item']
                break
        else:
            print('par {0} no found'.format(par_name))
            return False, data
        # print(par_name)
        par_type_decode, par_len_decode = struct.unpack(self.par_header_fmt, data[:self.par_header_len])

        body_decode = data[self.par_header_len:]

        if par_type != par_type_decode:
            # print("par type decode error")
            return False, data
        par_dict = dict()
        # print("Decoding:", par_name)
        (par_dict[par_name], body_decode) = self.par_decode_proc(par_item_list, body_decode)
        # print("Decode:", par_dict)
        return par_dict[par_name], data[self.par_header_len + par_len_decode:]


class ZLLRPSelSpec(dict):
    def __init__(self, sel_spec_id, reader_type, priority=0, state=0,
                 antennas=None, ant_config=None, duration_ms=0,
                 report_every_n_tags=1):
        """

        :param reader_type: 0,HB Inventory;
                            1,HB Invent Read;
                            2,HB_6C Inventory
        :param sel_spec_id:
        :param priority:
        :param state:
        :param antennas:
        :param duration_ms:
        :param report_every_n_tags:
        """
        super(ZLLRPSelSpec, self).__init__()
        # Sanity checks
        if sel_spec_id <= 0:
            raise ValueError("spec id should >0")

        if priority < 0 or priority > 7:
            raise ValueError("priority in 0~7")

        if state < 0 or state > 2:
            raise ValueError("state in 0~2")

        if antennas is None:
            antennas = [1]
        else:
            if not isinstance(antennas, list):
                raise ValueError("antennas should be list")

        if reader_type == 0:
            rf_spec = {
                'RfSpecID': sel_spec_id,
                'ProtocolID': 0,  # 0, HB
                'SelectType': reader_type,  # 0, inventory; 1, read
            }

        elif reader_type == 1:
            rf_spec = {
                'RfSpecID': sel_spec_id,
                'ProtocolID': 0,  # 0, HB
                'SelectType': reader_type,  # 0, inventory; 1, read
                'MemoryBank': {
                    'MemoryBankID': 0,  # user ID
                    'ReadType': 0,  # 0, Length; 1, Bank Type
                    'Pointer': 4,  # offset
                    'Count': 10,  # length
                    'BankType': 2  # 0, head half; 1, tail half; 2, total
                }
            }
        # HB_6c 6C Inventory
        elif reader_type == 2:
            rf_spec = {
                'RfSpecID': sel_spec_id,
                'ProtocolID': 1,  # 0, HB ; 1, 6C
                'SelectType': 0,  # 0, inventory; 1, read
            }

        else:
            rf_spec = {
                'RfSpecID': sel_spec_id,
                'ProtocolID': 0,  # 0, HB
                'SelectType': 0,  # 0, inventory; 1, read
            }

        if ant_config is not None:
            ant_config_key = "C1G2AntennaConfiguration" if reader_type == 2 else "AntennaConfiguration"
            rf_spec[ant_config_key] = ant_config

        self["SelectSpec"] = {
            'SelectSpecID': sel_spec_id,
            'Priority': priority,  # 0~7
            'CurrentState': state,  # 0, Disable; 1, Inactive; 2, Active
            'Persistence': 0,
            'Reserved': 0,
            'SelectSpecStartTrigger': {
                'SelectSpecStartTriggerType': 0  # 0, No condition; 1, immediately; 2, Period; 3, GPI
            },
            'SelectSpecStopTrigger': {
                'SelectSpecStopTriggerType': 0,  # 0, No condition; 1, continue; 2 GPI
                'DurationValue': 0  # millisecond
            },
            'AntennaSpec': {
                'AntennaIDs': antennas,
                'AntennaSpecStopTrigger': {
                    'AntennaSpecStopTriggerType': 3,  # 0, No condition; 1, continue; 2, GPI; 3, same as Tag
                    'DurationValue': duration_ms,
                    'TagObservationTrigger': {
                        'TriggerType': 2,  # 0, N Tags; 1, T sec; 2, A Attempts;
                        'NumberOfTags': 0,
                        'NumberOfAttempts': 1,
                        'TValue': 0,
                        'Timeout': 0
                    }
                },
                'RfSpec': rf_spec
            },
            'SelectReportSpec': {
                # 0, no condition; 1, tag count N or Ant stop; 2, tag count N or sel stop; 3, No report
                'SelectReportTrigger': 2,
                'NValue': report_every_n_tags,
                'EnableSelectSpecID': 1,
                'EnableSpecIndex': 1,
                'EnableRfSpecID': 1,
                'EnableAntennaID': 1,
                'EnablePeakRSSI': 1,
                'EnableFirstSeenTimestamp': 1,
                'EnableLastSeenTimestamp': 1,
                'EnableTagSeenCount': 1,
                'EnableAccessSpecID': 1,
                # dual mode
                'EnableProtocolID': 0,
                'EnableTagSpeed': 0,

                'Reserved': 0
            }
        }


if __name__ == '__main__':
    print(ZLLRPSelSpec(11, 0))
