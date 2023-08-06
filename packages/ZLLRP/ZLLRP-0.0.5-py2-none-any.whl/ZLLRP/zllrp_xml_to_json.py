# encoding: utf-8
# @Time    : 2020/3/4 0004 16:11
# @Author  : Liu Gang
# @Site    : 
# @File    : zllrp_xml_to_json.py
# @Software: PyCharm

import json
from zllrp_prot_lib import _PARAM
from xml.dom import minidom, Node

_TYPE_U1 = 1
_TYPE_U4 = 4
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

type_map = {
    "u1": _TYPE_U1,
    "u4": _TYPE_U4,
    "u7": _TYPE_U7,
    "u8": _TYPE_U8,
    "u16": _TYPE_U16,
    "u32": _TYPE_U32,
    "u64": _TYPE_U64,
    "s8": _TYPE_S8,
    "s16": _TYPE_S16,
    "s32": _TYPE_S32,
    "s64": _TYPE_S64,
    "u1v": _TYPE_U1V,
    "u8v": _TYPE_U8V,
    "utf8v": _TYPE_UTF8V,
    "u16v": _TYPE_U16V,
    "u32v": _TYPE_U32V
}

xml_parse = minidom.parse("zllrpStandardDef.xml")
choice_tags = xml_parse.documentElement.getElementsByTagName("choiceDefinition")
message_list_map = list()
msg_tags = xml_parse.documentElement.getElementsByTagName("messageDefinition")


def get_choice(ch_name):
    for choices in choice_tags:
        if choices.getAttribute("name") == ch_name:
            return choices
    else:
        return False


for msgs in msg_tags:
    msg_dict = dict()
    msg_dict["msg_name"] = msgs.getAttribute("name")
    msg_dict["msg_type"] = int(msgs.getAttribute("typeNum"))
    par_list = list()
    for children in msgs.childNodes:
        if children.nodeType == Node.ELEMENT_NODE:
            par_detail_dict = dict()
            if children.tagName == "parameter":
                par_detail_dict["name"] = children.getAttribute("type")
                par_detail_dict["par_kind"] = _PARAM
                par_detail_dict["count"] = children.getAttribute("repeat")
            elif children.tagName == "field":
                par_detail_dict["name"] = children.getAttribute("name")
                par_detail_dict["par_kind"] = type_map[children.getAttribute("type")]
                par_detail_dict["count"] = "1"
            elif children.tagName == "reserved":
                par_detail_dict["name"] = "Reserved"
                par_detail_dict["par_kind"] = int(children.getAttribute("bitCount"))
                par_detail_dict["count"] = "1"
            else:
                continue

            par_list.append(par_detail_dict)
    msg_dict["msg_par"] = par_list

    message_list_map.append(msg_dict)

with open("mssage_list_map.json", "w") as msg_fp:
    json.dump(message_list_map, msg_fp, indent=4)

parameter_list_map = list()
par_tags = xml_parse.documentElement.getElementsByTagName("parameterDefinition")


def get_par_detail(ele, count=None):
    ret_par_detail = dict()
    if ele.tagName == "parameter":
        ret_par_detail["name"] = ele.getAttribute("type")
        ret_par_detail["par_kind"] = _PARAM
        ret_par_detail["count"] = ele.getAttribute("repeat") if count is None else count

    elif ele.tagName == "field":
        ret_par_detail["name"] = ele.getAttribute("name")
        ret_par_detail["par_kind"] = type_map[ele.getAttribute("type")]
        ret_par_detail["count"] = "1"

    elif ele.tagName == "reserved":
        ret_par_detail["name"] = "Reserved"
        ret_par_detail["par_kind"] = int(ele.getAttribute("bitCount"))
        ret_par_detail["count"] = "1"
    # elif ele.tagName == "choice":
    #     choice_name = children.getAttribute("type")
    #     choice_ele = get_choice(choice_name)
    #     choice_count = children.getAttribute("repeat")
    else:
        return False
    return ret_par_detail


for pars in par_tags:
    par_dict = dict()
    par_dict["par_name"] = pars.getAttribute("name")
    par_dict["par_type"] = int(pars.getAttribute("typeNum"))
    par_list = list()
    for children in pars.childNodes:
        if children.nodeType == Node.ELEMENT_NODE:
            if children.tagName == "choice":
                choice_name = children.getAttribute("type")
                choice_ele = get_choice(choice_name)
                choice_count = children.getAttribute("repeat")
                for choice_chld in choice_ele.childNodes:
                    if choice_chld.nodeType == Node.ELEMENT_NODE:
                        par_detail_dict = get_par_detail(choice_chld, choice_count)
                        if par_detail_dict is False:
                            continue
                        par_list.append(par_detail_dict)
            else:
                par_detail_dict = get_par_detail(children)
                if par_detail_dict is False:
                    continue
                par_list.append(par_detail_dict)
            # if children.tagName == "parameter":
            #     par_detail_dict["name"] = children.getAttribute("type")
            #     par_detail_dict["par_kind"] = _PARAM
            #     par_detail_dict["count"] = children.getAttribute("repeat")
            #
            # elif children.tagName == "field":
            #     par_detail_dict["name"] = children.getAttribute("name")
            #     par_detail_dict["par_kind"] = type_map[children.getAttribute("type")]
            #     par_detail_dict["count"] = "1"
            #
            # elif children.tagName == "reserved":
            #     par_detail_dict["name"] = "Reserved"
            #     par_detail_dict["par_kind"] = int(children.getAttribute("bitCount"))
            #     par_detail_dict["count"] = "1"
            #
            # else:
            #     continue

    par_dict["par_item"] = par_list

    parameter_list_map.append(par_dict)

with open("parameter_list_map.json", "w") as par_fp:
    json.dump(parameter_list_map, par_fp, indent=4)
