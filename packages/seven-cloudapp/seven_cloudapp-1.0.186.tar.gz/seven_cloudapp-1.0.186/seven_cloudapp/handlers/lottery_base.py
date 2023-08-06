# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-11-20 15:22:19
:LastEditTime: 2021-01-22 16:11:00
:LastEditors: HuangJingCan
:description: 
"""
import random
import datetime
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.coin.coin_order_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.lottery.lottery_value_log_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.lottery.lottery_log_model import *

from seven_cloudapp.models.behavior_model import *


class LotteryBaseHandler(SevenBaseHandler):
    """
    :description: 抽奖基础类
    """
    def start_turntable(self, app_id, open_id, act_id, login_token):
        """
        :description: 大转盘抽奖处理
        :param app_id:app_id
        :last_editors: HuangJianYi
        """
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        lottery_value_log_model = LotteryValueLogModel(db_transaction=db_transaction)
        prize_roster_model = PrizeRosterModel()
        act_info_model = ActInfoModel()
        act_prize_model = ActPrizeModel(db_transaction=db_transaction)
        coin_order_model = CoinOrderModel(db_transaction=db_transaction)
        lottery_valueLog_model = LotteryValueLogModel(db_transaction=db_transaction)
        now_date = self.get_now_datetime()

        log_info = {}
        #请求太频繁限制
        if self.check_post(f"Lottery_Post_{act_id}_{str(open_id)}") == False:
            log_info["code"] = "HintMessage"
            log_info["message"] = "对不起，请稍后再试"
            return log_info
        act_dict = act_info_model.get_dict("id=%s and is_release=1", params=act_id)
        if not act_dict:
            log_info["code"] = "NoAct"
            log_info["message"] = "对不起，活动不存在"
            return log_info
        last_content = self.get_currency_type_name(act_dict['currency_type'])
        if TimeHelper.format_time_to_datetime(now_date) < act_dict['start_date']:
            log_info["code"] = "NoAct"
            log_info["message"] = "活动将在" + act_dict['start_date'] + "开启"
            return log_info
        if TimeHelper.format_time_to_datetime(now_date) > act_dict['end_date']:
            log_info["code"] = "NoAct"
            log_info["message"] = "活动已结束"
            return log_info
        user_info = user_info_model.get_entity("app_id=%s and act_id=%s and open_id=%s", params=[app_id, act_id, open_id])
        if not user_info:
            log_info["code"] = "NoUser"
            log_info["message"] = "对不起，用户不存在"
            return log_info
        if user_info.user_nick == "":
            log_info["code"] = "NoUserNick"
            log_info["message"] = "对不起，请先授权"
            return log_info
        if act_dict['join_ways'] == 1:
            if user_info.is_favor != 1:
                log_info["code"] = "Error"
                log_info["message"] = "必须关注店铺才能抽奖"
                return log_info
        elif act_dict['join_ways'] == 2:
            if user_info.is_member != 1:
                log_info["code"] = "Error"
                log_info["message"] = "必须加入会员才能抽奖"
                return log_info
        if user_info.user_state == 1:
            log_info["code"] = "UserState"
            log_info["message"] = "对不起，你是黑名单用户,无法抽奖"
            return log_info
        if user_info.login_token != login_token:
            log_info["code"] = "ErrorToken"
            log_info["message"] = "对不起，已在另一台设备登录,当前无法抽奖"
            return log_info
        if user_info.lottery_value - act_dict['lottery_value'] < 0:
            log_info["code"] = "NoNum"
            log_info["message"] = "对不起,积分不足" if act_dict['currency_type'] == 2 else "对不起,次数不足"
            return log_info
        no_orderno_prize_roster = self.check_orderno_by_prize_roster(act_id, open_id)
        if no_orderno_prize_roster:
            log_info["code"] = "No_OrderNo"
            log_info["message"] = no_orderno_prize_roster
            return log_info
        lock_name = "act_id_" + str(act_id) + "_lottery"
        identifier = self.acquire_lock(lock_name)
        if isinstance(identifier, bool):
            log_info["code"] = "UserLimit"
            log_info["message"] = "当前人数过多,请稍后再试"
            return log_info

        #抽奖
        try:
            act_prize_list = act_prize_model.get_dict_list("act_id=%s and is_release=1 and surplus>0", params=act_id)
            if len(act_prize_list) == 0:
                self.release_lock(lock_name, identifier)
                log_info["code"] = "UserLimit"
                log_info["message"] = "对不起，奖品已无库存，暂时无法抽奖"
                return log_info

            prize_roster_list = prize_roster_model.get_list("open_id=%s and act_id=%s", params=[open_id, act_id])
            #中奖限制
            cur_prize_info_list = []
            for act_prize in act_prize_list:
                if act_prize["prize_limit"] > 0:
                    mat_prize_list = [i for i in prize_roster_list if i.prize_id == act_prize["id"]]
                    if len(mat_prize_list) < act_prize["prize_limit"]:
                        cur_prize_info_list.append(act_prize)
                else:
                    cur_prize_info_list.append(act_prize)

            if len(cur_prize_info_list) <= 0:
                self.release_lock(lock_name, identifier)
                log_info["code"] = "Error"
                log_info["message"] = "抱歉，您在本活动获得的奖品已达到上限，无法继续抽奖"
                return log_info

            #强制命中算法
            cur_prize_info_list = self.must_prize_algorithm(prize_roster_model, cur_prize_info_list, "act_id=%s", act_id)
            #抽奖
            result_prize = self.lottery_algorithm(cur_prize_info_list)

            history_value = user_info.lottery_value

            db_transaction.begin_transaction()
            #扣除用户次数
            user_info.lottery_value -= act_dict['lottery_value']
            user_info.lottery_sum += 1
            user_info_model.update_table(f"lottery_value=lottery_value-{act_dict['lottery_value']},lottery_sum=lottery_sum+1", "id=%s", params=user_info.id)

            #用户抽奖值使用记录
            lottery_value_log = LotteryValueLog()
            lottery_value_log.app_id = app_id
            lottery_value_log.act_id = act_id
            lottery_value_log.open_id = open_id
            lottery_value_log.user_nick = user_info.user_nick
            lottery_value_log.log_title = "大转盘抽奖-" + str(act_dict['lottery_value']) + last_content
            lottery_value_log.log_info = self.json_dumps({})
            lottery_value_log.source_type = 4  #抽奖
            lottery_value_log.change_type = 402
            lottery_value_log.operate_type = 1
            lottery_value_log.current_value = -1
            lottery_value_log.history_value = history_value
            lottery_value_log.create_date = now_date
            lottery_valueLog_model.add_entity(lottery_value_log)

            #同步奖品库存
            if int(result_prize["prize_type"]) == 4 or int(result_prize["prize_type"]) == 5:  #参与奖和谢谢参与不扣库存
                act_prize_model.update_table("hand_out=hand_out+1", "id=%s", result_prize["id"])
            else:
                act_prize_model.update_table("surplus=surplus-1,hand_out=hand_out+1", "id=%s", result_prize["id"])

            db_transaction.commit_transaction()

            #录入中奖记录
            prize_roster = PrizeRoster()
            prize_roster.app_id = app_id
            prize_roster.act_id = act_id
            prize_roster.open_id = open_id
            prize_roster.prize_id = result_prize["id"]
            prize_roster.prize_name = result_prize["prize_name"]
            prize_roster.prize_price = result_prize["prize_price"]
            prize_roster.prize_pic = result_prize["prize_pic"]
            prize_roster.prize_detail = result_prize["prize_detail"]
            prize_roster.prize_type = result_prize["prize_type"]
            prize_roster.award_name = result_prize["tag_name"] if result_prize["tag_name"] else ""
            prize_roster.goods_id = result_prize["goods_id"]
            prize_roster.is_sku = result_prize["is_sku"]
            prize_roster.goods_code = result_prize["goods_code"]
            prize_roster.goods_code_list = result_prize["goods_code_list"]
            prize_roster.sku_detail = result_prize["sku_detail"]
            prize_roster.user_nick = user_info.user_nick
            prize_roster.avatar = user_info.avatar  #抽奖时添加用户头像
            prize_roster.create_date = self.get_now_datetime()

            #添加商家对帐记录
            coin_order = self.get_coin_order(coin_order_model, open_id, act_id)
            if coin_order != None:
                coin_order_model.update_entity(coin_order)
                prize_roster.main_pay_order_no = coin_order.main_pay_order_no
                prize_roster.order_no = coin_order.pay_order_no
                if coin_order.pay_order_no != "":
                    prize_roster.frequency_source = 0
                else:
                    prize_roster.frequency_source = 1
            if int(result_prize["prize_type"]) != 5:  #谢谢参与不加入我的奖品
                prize_roster_id = prize_roster_model.add_entity(prize_roster)
                prize_roster.id = prize_roster_id

            self.release_lock(lock_name, identifier)
            log_info["code"] = "Success"
            log_info["message"] = prize_roster.__dict__
        except Exception as ex:
            self.logger_error.error(str(ex) + "【大转盘抽奖】")
            self.release_lock(lock_name, identifier)
            db_transaction.rollback_transaction()
            log_info["code"] = "Exception"
            log_info["message"] = ex
            return log_info
        if log_info["code"] == "Success":
            behavior_model = BehaviorModel()
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_dict['owner_open_id'], 'LotteryAddUserCount', 1)
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_dict['owner_open_id'], 'LotteryUserCount', 1)
            behavior_model.report_behavior_log(app_id, act_id, open_id, act_dict['owner_open_id'], 'LotteryCount', 1)

        return log_info

    def must_prize_algorithm(self, prize_roster_model, prize_list, condition, params):
        """
        :description: 强制命中算法
        :param prize_roster_model:中奖记录model
        :param prize_list:当前奖品列表
        :param condition:条件
        :param params:参数
        """
        must_prize_list = []
        prize_roster_total = prize_roster_model.get_total(condition, params=params)
        cur_prize_info_list2 = []
        for cur_prize_info in prize_list:
            if cur_prize_info["lottery_type"] == 2 and cur_prize_info["force_count"] > 0:
                page_total = int(prize_roster_total / cur_prize_info["force_count"])
                prize_roster_after_list = prize_roster_model.get_dict_list(condition, "", "id asc", str(page_total * cur_prize_info["force_count"]) + "," + str((page_total * cur_prize_info["force_count"]) + cur_prize_info["force_count"]), params=params)
                is_exist = [prize_roster_after for prize_roster_after in prize_roster_after_list if prize_roster_after["prize_id"] == cur_prize_info["id"]]
                if len(is_exist) == 0:
                    if (prize_roster_total + 1) % cur_prize_info["force_count"] == 0:
                        must_prize_list.append(cur_prize_info)
                    else:
                        cur_prize_info_list2.append(cur_prize_info)
            else:
                cur_prize_info_list2.append(cur_prize_info)
        if len(must_prize_list) > 0:
            prize_list = must_prize_list
        else:
            prize_list = cur_prize_info_list2
        return prize_list

    def lottery_algorithm(self, prize_list):
        """
        :description: 抽奖算法
        :param prize_list:奖品列表
        :return: 中奖的奖品
        :last_editors: HuangJianYi
        """
        init_value = 0
        probability_list = []
        for prize in prize_list:
            current_prize = prize
            current_prize["start_probability"] = init_value
            current_prize["end_probability"] = init_value + prize["probability"]
            probability_list.append(current_prize)
            init_value = init_value + prize["probability"]
        prize_index = random.randint(0, init_value - 1)
        for prize in probability_list:
            if (prize["start_probability"] <= prize_index and prize_index < prize["end_probability"]):
                return prize

    def add_lottery_log(self, app_id, act_id, open_id, log_info):
        """
        :description: 抽奖日志
        :param app_id：应用标识
        :param act_id：活动标识
        :param open_id：open_id
        :param log_info：日志信息
        :return: 
        :last_editors: HuangJianYi
        """
        lottery_log_model = LotteryLogModel()
        lottery_log = LotteryLog()
        lottery_log.app_id = app_id
        lottery_log.act_id = act_id
        lottery_log.open_id = open_id
        lottery_log.log_info = self.json_dumps(log_info)
        create_date = self.get_now_datetime()
        create_date = TimeHelper.format_time_to_datetime(create_date)
        lottery_log.create_date = create_date
        lottery_log.create_day = int(TimeHelper.datetime_to_format_time(create_date, "%Y%m%d"))
        lottery_log_model.add_entity(lottery_log)

    def get_coin_order(self, coin_order_model, open_id, act_id):
        """
        :description: 获取商家对帐记录
        :param coin_order_model：商家对帐实例化model
        :param open_id：open_id
        :param act_id：活动标识
        :return: 
        :last_editors: HuangJianYi
        """
        coin_order = None
        coin_order_set = coin_order_model.get_entity("surplus_count>0 and open_id=%s and act_id=%s and pay_order_id=0", "id asc", params=[open_id, act_id])
        if coin_order_set:
            coin_order_set.surplus_count = coin_order_set.surplus_count - 1
            coin_order = coin_order_set
        else:
            coin_order_pay = coin_order_model.get_entity("surplus_count>0 and open_id=%s and act_id=%s and pay_order_id>0", "id asc", params=[open_id, act_id])
            if coin_order_pay:
                coin_order_pay.surplus_count = coin_order_pay.surplus_count - 1
                coin_order = coin_order_pay
        return coin_order

    def get_currency_type_name(self, currency_type):
        """
        :description: 获取抽奖货币类型名称
        :param currency_type: 抽奖货币类型
        :return str
        :last_editors: HuangJianYi
        """
        if int(currency_type) == 2:
            return "积分"
        elif int(currency_type) == 4:
            return "抽奖码"
        else:
            return "抽奖次数"

    def check_orderno_by_prize_roster(self, act_id, open_id):
        """
        :description: 校验中奖名单是否包含实物奖品没有填写收货地址
        :param act_id: 活动id
        :param open_id: open_id
        :return dict
        :last_editors: HuangJianYi
        """
        prize_roster = PrizeRosterModel().get_dict("act_id=%s and open_id=%s and prize_type in (1,2) and prize_order_id=0", params=[act_id, open_id])
        return prize_roster