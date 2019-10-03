# -*- coding: utf-8 -*-
import re
import os
from log.logger_client import set_logger

logger = set_logger()


def format_output(data_to_format):
    list_without_brackets = filter(
        None,
        [value.strip().replace('(', ' ').replace(')', '') for value in data_to_format]
        )
    result_dict = {}
    for values in list_without_brackets:
        name = values.split()[0]
        value = ' '.join(values.split()[1:])
        result_dict[name] = value
    if result_dict["STATUS"] == "Running":
        result_dict["STATUS"] = 1
    else:
        result_dict["STATUS"] = 0
    return result_dict


def get_mq_manager_status(mq_manager_data):
    pattern = "QMNAME"
    result = format_output(mq_manager_data.split(')'))
    return result


def get_mq_managers(mq_managers_data):
    mq_managers = []
    mqmanager_name_regexp = 'QMNAME\(([^)]+)\)'
    output_list = filter(None, mq_managers_data.split('\n'))
    for mq_manager in output_list:
        mq_manager_name = re.search(mqmanager_name_regexp, mq_manager).group(1)
        mq_managers.append(mq_manager_name)
    return mq_managers


def make_metric_for_mq_manager_status(mq_manager_status_data):
    metric_name = 'mq_manager_status'
    # Unpack tags
    metric_data = '%s{default="%s", instname="%s", instpath="%s", instver="%s", qmname="%s", standby="%s"} %d\n' % (
            metric_name,
            mq_manager_status_data["DEFAULT"],
            mq_manager_status_data["INSTNAME"],
            mq_manager_status_data["INSTPATH"],
            mq_manager_status_data["INSTVER"],
            mq_manager_status_data["QMNAME"],
            mq_manager_status_data["STANDBY"],
            mq_manager_status_data["STATUS"]
            )
    return metric_data, mq_manager_status_data["STATUS"]