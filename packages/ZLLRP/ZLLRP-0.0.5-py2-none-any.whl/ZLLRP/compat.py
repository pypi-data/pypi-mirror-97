# -*- coding: utf-8 -*-
# @CreateTime : 2020/1/15 15:45
# @Author     : Liu Gang
# @File       : compat.py
# @Software   : PyCharm

import sys

PY3 = sys.version_info[0] == 3

if PY3:
    def iteritems(d):
        return iter(d.items())


    def iterkeys(d):
        return iter(d.keys())


    std_str = bytes


    def conv_bytes_str(bytes_str):
        bytes_str_c = ""
        for c in bytes_str:
            bytes_str_c += "{0:02X} ".format(c)

        return bytes_str_c

else:
    def iteritems(d):
        return d.iteritems()


    def iterkeys(d):
        return d.iterkeys()


    std_str = str


    def conv_bytes_str(msg_str):
        msg_str_c = ""
        for c in msg_str:
            msg_str_c += "{0:02X} ".format(ord(c))

        return msg_str_c
