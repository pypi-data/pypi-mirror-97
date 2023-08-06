# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-05-29 09:40:42
:LastEditTime: 2021-02-08 11:34:05
:LastEditors: HuangJingCan
:description: 机台（盒子）
"""
import decimal
import copy
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.enum import *
from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.behavior_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.db_models.machine.machine_value_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.behavior.behavior_report_model import *
from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *


class MachineHandler(SevenBaseHandler):
    """
    :description: 保存机台（业务各自实现）
    """
    @filter_check_params("act_id,machine_name")
    def post_async(self):
        """
        :description: 保存机台（业务各自实现）
        :param act_id：活动id
        :param machine_name：机台名称
        :return: 
        :last_editors: HuangJingCan
        """
        pass


class MachineListHandler(SevenBaseHandler):
    """
    :Description: 机台信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :Description: 获取机台列表
        :param act_id：活动id
        :param page_index：页索引
        :param page_size：页大小
        :return: list
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))

        if act_id <= 0:
            return self.reponse_json_error_params()

        page_list, total = MachineInfoModel().get_dict_page_list("*", page_index, page_size, "act_id=%s", "", "sort_index desc", act_id)

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class MachineDelHandler(SevenBaseHandler):
    """
    :description: 删除机台
    """
    @filter_check_params("machine_id")
    def get_async(self):
        """
        :description: 删除机台
        :param machine_id：机台id
        :return: reponse_json_success
        :last_editors: HuangJingCan
        """
        machine_id = int(self.get_param("machine_id", 0))

        if machine_id <= 0:
            return self.reponse_json_error_params()

        ActPrizeModel().del_entity("machine_id=%s", machine_id)

        MachineInfoModel().del_entity("id=%s", machine_id)

        MachineValueModel().del_entity("machine_id=%s", machine_id)

        BehaviorOrmModel().del_entity("key_name='openUserCount_" + str(machine_id) + "' or key_name='openCount_" + str(machine_id) + "'")

        self.create_operation_log(OperationType.delete.value, "machine_info_tb", "MachineDelHandler", None, machine_id)

        self.reponse_json_success()


class MachineReleaseHandler(SevenBaseHandler):
    """
    :description: 机台上下架
    """
    @filter_check_params("machine_id,is_release")
    def get_async(self):
        """
        :description: 机台上下架
        :param machine_id：机台id
        :param is_release：是否发布（0下架1上架）
        :return: 
        :last_editors: HuangJingCan
        """
        machine_id = int(self.get_param("machine_id", 0))
        is_release = int(self.get_param("is_release", 0))

        if machine_id <= 0:
            return self.reponse_json_error_params()

        MachineInfoModel().update_table("is_release=%s", "id=%s", [is_release, machine_id])

        self.reponse_json_success()


class MachineValueLogHandler(SevenBaseHandler):
    """
    :description: 用户机台配置记录
    """
    @filter_check_params("act_id,user_open_id")
    def get_async(self):
        """
        :description: 用户机台配置记录
        :param act_id：活动id
        :param user_open_id：用户唯一标识
        :return 列表
        :last_editors: HuangJingCan
        """
        act_id = self.get_param("act_id")
        user_open_id = self.get_param("user_open_id")

        machine_info_model = MachineInfoModel()
        machine_value_model = MachineValueModel()
        machine_value_log_model = MachineValueLogModel()

        machine_info_list = machine_info_model.get_list("act_id=%s", params=act_id)
        machine_value_log_list_dict = machine_value_log_model.get_dict_list("act_id=%s and open_id=%s", order_by='id desc', params=[act_id, user_open_id])
        machine_value_list = machine_value_model.get_list("act_id=%s and open_id=%s", params=[act_id, user_open_id])

        machine_value_log_groups = []
        for machine_info in machine_info_list:
            machine_value_log_group = {}
            machine_value_log_group["machine_id"] = machine_info.id
            machine_value_log_group["machine_name"] = machine_info.machine_name
            for machine_value in machine_value_list:
                if machine_value.machine_id == machine_info.id:
                    machine_value_log_group["surplus_value"] = machine_value.surplus_value
                    machine_value_log_group["open_value"] = machine_value.open_value
                    continue
            if "surplus_value" not in machine_value_log_group.keys():
                machine_value_log_group["surplus_value"] = 0
            if "open_value" not in machine_value_log_group.keys():
                machine_value_log_group["open_value"] = 0
            machine_value_log_group["machine_value_log_list"] = [i for i in machine_value_log_list_dict if i["machine_id"] == machine_info.id]
            machine_value_log_groups.append(machine_value_log_group)

        self.reponse_json_success(machine_value_log_groups)