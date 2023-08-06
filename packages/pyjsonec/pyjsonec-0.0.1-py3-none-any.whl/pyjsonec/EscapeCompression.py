#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/3/6 16:21
# @Author  : Anran
# @File    : EscapeCompression.py
# @Function:
import json

class EscapeCompression:
    def __init__(self):
        pass

    def data_escape(self, data):
        """
        :param data: json or dict
        :return: escape data
        """
        try:
            new_data = json.dumps(data).replace('"', '\\"')
            return json.dumps(new_data)
        except Exception as e:
            return str(e)

    def data_compression(self, data):
        """
        :param data: json or dict
        :return: compression data
        """
        try:
            new_data = str(data).replace(' ', '').replace("\n", "")
            return json.dumps(new_data)
        except Exception as e:
            return str(e)

