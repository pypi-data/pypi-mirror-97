# -*- coding: utf-8 -*-
"""
:Author: LaiKaiXiang
:Date: 2020-11-12 10:21:54
:LastEditTime: 2021-02-26 10:05:45
:LastEditors: HuangJingCan
:description: 任务
"""
from copy import deepcopy
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.enum import *
from seven_cloudapp.models.seven_model import *
from seven_cloudapp.models.behavior_model import *

from seven_cloudapp.models.db_models.task.task_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *


class TaskSaveHandler(SevenBaseHandler):
    """
    :description 保存任务列表
    """
    # def get_async(self):
    #     task_info = TaskInfoModel().get_entity_by_id(11)
    #     self.save_orm_task_config(2, "3000000026366853", task_info.task_type, task_info.task_config, 1)
    #     task_info = TaskInfoModel().get_entity_by_id(12)
    #     self.save_orm_task_config(2, "3000000026366853", task_info.task_type, task_info.task_config, 1)

    @filter_check_params("task_list,act_id,app_id")
    def post_async(self):
        """
        :description: 保存任务列表
        :param act_id：活动id
        :param app_id：app_id
        :param task_list：任务列表
        :return reponse_json_success
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))
        app_id = self.get_param("app_id")
        task_list = self.get_param("task_list")
        task_list = self.json_loads(task_list)
        task_model = TaskInfoModel()
        for item in task_list:
            if "id" in item.keys():
                task_info = task_model.get_entity_by_id(int(item["id"]))
                if task_info:
                    task_info_old = deepcopy(task_info)
                    task_info.task_type = int(item["task_type"])
                    if item.__contains__("task_config"):
                        task_info.task_config = self.json_dumps(item["task_config"])
                    task_info.sort_index = int(item["sort_index"])
                    task_info.is_release = int(item["is_release"])
                    task_info.modify_date = self.get_now_datetime()
                    is_change = int(item["is_change"]) if item.__contains__("is_change") else 0
                    task_model.update_entity(task_info, "task_config,sort_index,is_release,modify_date")

                    self.create_operation_log(OperationType.update.value, task_info.__str__(), "TaskSaveHandler", self.json_dumps(task_info_old.__dict__), self.json_dumps(task_info.__dict__))

                    self.save_orm_task_config(act_id, app_id, task_info.task_type, task_info.task_config, is_change)

            else:
                task_info = TaskInfo()
                task_info.act_id = act_id
                task_info.app_id = app_id
                task_info.task_type = int(item["task_type"])
                if item.__contains__("task_config"):
                    task_info.task_config = self.json_dumps(item["task_config"])
                task_info.sort_index = int(item["sort_index"])
                task_info.is_release = int(item["is_release"])
                task_info.create_date = self.get_now_datetime()
                is_change = int(item["is_change"]) if item.__contains__("is_change") else 0
                task_model.add_entity(task_info)

                self.create_operation_log(OperationType.add.value, task_info.__str__(), "TaskSaveHandler", None, self.json_dumps(task_info))

                self.save_orm_task_config(act_id, app_id, task_info.task_type, task_info.task_config, is_change)

        self.reponse_json_success()

    def save_orm_task_config(self, act_id, app_id, task_type, task_config, is_change):
        """
        :description: 增加行为映射数据
        :param act_id：活动id
        :param app_id：app_id
        :param task_type：任务类型
        :param task_config：任务配置
        :param is_change：是否变动
        :return 
        :last_editors: HuangJingCan
        """
        if task_config:
            if type(task_config) == str:
                task_config = ast.literal_eval(task_config)
            reward_list = task_config["reward_list"] if task_config.__contains__("reward_list") else []
            if reward_list:
                if is_change == 1:
                    BehaviorOrmModel().del_entity("act_id=%s and task_type=%s", [act_id, task_type])
                    if task_type == 14:
                        # 累计消费
                        for reward in reward_list:
                            self.save_orm_task(act_id, app_id, task_type, "AddUpBuy", reward['key'], f"累计满{reward['money']}元")
                    elif task_type == 15:
                        # 单笔订单消费
                        for reward in reward_list:
                            self.save_orm_task(act_id, app_id, task_type, "SingleBuy", reward['key'], f"单笔满{reward['money']}元")

    def save_orm_task(self, act_id, app_id, task_type, key_name_prefix, task_key, group_sub_name):
        """
        :description: 增加行为映射数据
        :param act_id：活动id
        :param app_id：app_id
        :param task_type：任务类型
        :param task_key：任务key
        :param group_sub_name：任务分组二级名称
        :return 
        :last_editors: HuangJingCan
        """
        act_dict = ActInfoModel().get_dict_by_id(act_id)
        act_type = 0
        if act_dict:
            act_type = act_dict["act_type"]
        orm_infos = []
        for i in range(3):
            behavior_orm = BehaviorOrm()
            if i == 0:
                behavior_orm.is_repeat = 1
                behavior_orm.repeat_type = 1
                behavior_orm.key_value = "参与人数"
                behavior_orm.key_name = key_name_prefix + "UserCount_" + str(task_key)
            elif i == 1:
                behavior_orm.is_repeat = 0
                behavior_orm.key_value = "完成次数"
                behavior_orm.key_name = key_name_prefix + "Count_" + str(task_key)
            else:
                behavior_orm.is_repeat = 0
                behavior_orm.key_value = "积分"
                behavior_orm.key_name = key_name_prefix + "RewardCount_" + str(task_key)
            behavior_orm.task_type = task_type
            behavior_orm.group_name = "销售数据"
            behavior_orm.group_sub_name = group_sub_name
            behavior_orm.value_type = 1
            behavior_orm.is_common = 0
            behavior_orm.sort_index = 10
            behavior_orm.app_id = app_id
            behavior_orm.act_id = act_id
            behavior_orm.act_type = act_type
            behavior_orm.create_date = self.get_now_datetime()
            orm_infos.append(behavior_orm)

        behavior_orm_model = BehaviorOrmModel()
        behavior_orm_model.add_list(orm_infos)
        behavior_orm_model.update_table("sort_index=id", "task_type=%s", task_type)


class TaskListHandler(SevenBaseHandler):
    """
    :description: 获取任务列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 获取任务列表
        :param act_id：活动id
        :return list
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", 0))

        if act_id <= 0:
            return self.reponse_json_error()

        dict_task_list = TaskInfoModel().get_dict_list("act_id=%s", params=act_id)

        for item_task in dict_task_list:
            if item_task["task_config"]:
                item_task["task_config"] = ast.literal_eval(item_task["task_config"])
            else:
                item_task["task_config"] = {}

        self.reponse_json_success(dict_task_list)