# seven_cloudapp

## 天志互联Python淘宝云应用框架库

### 1.0.191.2 更新内容
* seven_base增加get_app_key_secret，更新json_dumps
* 更新UserPrizeListHandler
* 修改TopBaseHandler获取app_key方式app_key, app_secret = self.get_app_key_secret()

### 1.0.187 更新内容
* SevenBaseHandler重写prepare

### 1.0.180.1 更新内容
* 实例化更新instantiate_new
* 更新LeftNavigationHandler的customer_service

### 1.0.180 更新内容
* app_info增加店铺图标字段
* NextProgressHandler修改app_info是否完成配置

### 1.0.175 更新内容
* 新增ip系列相关操作
* 更新ActTypeListHandler

### 1.0.171 更新内容
* 更新throw_s.py，活动实体获取改成字典类型

### 1.0.170 更新内容
* 更新价格挡位price_s.py，新增字段：关联类型

### 1.0.168 更新内容
* 更新task.py：TaskListHandler的邀请，收藏，关注添加新字段“completed_quantity”：完成数量
InviteRewardHandler、FollowHandler、JoinMemberRewardHandler、CollectGoodsHandler、BrowseGoodsHandler，添加判断抽奖货币类型

### 1.0.165 更新内容
* 新增refund_order_model

### 1.0.164 更新内容
* 更新save_orm_task

### 1.0.163 更新内容
* 代码整改

### 1.0.162 更新内容
* 更新LotteryValueHandler
* 更新send_lottery_value

### 1.0.161 更新内容
* 更新order_s.py
* 更新LotteryValueHandler

### 1.0.158 更新内容
* 更新report_s.py
* 更新user_s.py

### 1.0.155 更新内容
* 更新prize_roster_model.py
* 更新process_behavior
* 更新LoginHandler

### 1.0.151 更新内容
* 新增 UserBaseHandler
* 更新 LoginHandler和UserHandler

### 1.0.145 更新内容
* 更新 instantiate_new
* 新增任务和抽奖模块

### 1.0.141 更新内容
* 更新 init_throw_goods_list
* 更新 reponse_json_error

### 1.0.138 更新内容
* 更新SevenBaseHandler的get_now_datetime方法
* 更新init_throw_goods_list
* 更新BehaviorModel

### 1.0.136 更新内容
* 更新prize_order_tb新增error_desc更新order_status

### 1.0.134 更新内容
* 更新表act_info_tb增加release_date
* 更新NextProgressHandler

### 1.0.131 更新内容
* 修改json_loads
* 新增get_app_id
* 修改get_taobao_order

### 1.0.124 更新内容
* 修改ActTypeListHandler、SubmitPrizeOrderHandler
* 修改user.py

### 1.0.118 更新内容
* 修改PrizeOrderImportHandler、LotteryValueLogExportHandler

### 1.0.114 更新内容
* 投放修改
* 更新TopBaseHandler、SevenBaseHandler

### 1.0.111 更新内容
* 修改注释
* 更新UpdateInfoHandler

### 1.0.106 更新内容
* 更新json_dumps、json_loads

### 1.0.103 更新内容
* 增加底层saas_custom_model

### 1.0.102 更新内容
* 增加底层friend_link_model、course_info_model、course_type_model、material_info_model、message_info_model、product_price_model、version_info_model

### 1.0.101 更新内容
* 增加UserListExportHandler
* 修改UserListHandler

### 1.0.93 更新内容
* 更新ActTypeModel、LotteryValueLogModel

### 1.0.90 更新内容
* 更新lottery_value_log_model
* 新增LotteryValueLogHandler、LotteryValueLogExportHandler

### 1.0.83 更新内容
* 更新整合TopBaseHandler
* 用户表user_info_tb增加store_pay_price

### 1.0.79 更新内容
* 更新UserStatusByBlackHandler
* 更新LoginHandler

### 1.0.77 更新内容
* 新增OnlineLiveUrlHandler
* 新增DecorationPosterHandler

### 1.0.72 更新内容
* 更新invite_log_model

### 1.0.69 更新内容
* prize_s下PrizeListHandler增加强制概率算法

### 1.0.68 更新内容
* order_s下新增订单导出导入PrizeOrderExportHandler、PrizeOrderImportHandler、PrizeRosterExportHandler

### 1.0.60 更新内容
* user_s下新增加UserBlackListHandler
* goods增加RecommendGoodsHandler、RecommendGoodsListHandler

### 1.0.52 更新内容
* prize_s下PrizeListHandler
* db_models增加recommend、signin
* 黑名单管理

### 1.0.50 更新内容
* 代码整理
* prize_s增加PrizeListHandler

### 1.0.49 更新内容
* BehaviorModel下新增report_behavior_log
* ActTypeListHandler下新增字段skill_case

### 1.0.46 更新内容
* 新增UpdateInfoHandler

### 1.0.45 更新内容
* LeftNavigationHandler增加helper_info的is_remind_phone返回

### 1.0.44 更新内容
* 修复实例化方法  
* 增加方法注释

### 1.0.42 更新内容
* 增加一些新底层

### 1.0.39 更新内容
* 更新behavior_model.py方法report_behavior

### 1.0.38 更新内容
* behavior_orm_tb新增字段group_sub_name  
* user_info_tb新增字段is_member、is_favor  
* prize_roster_tb新增字段main_pay_order_no

### 1.0.36 更新内容
* 新增FriendLinkHandler

### 1.0.35 更新内容
* 新增FriendLinkHandler

### 1.0.34 更新内容
* 新增LeftNavigationHandler、RightExplainHandler

### 1.0.30 更新内容
* 修改reponse_json_error方法

### 1.0.29 更新内容
* 修改db_key为db_cloudapp

### 1.0.27 更新内容
* 代码注释完善
* 去除盲盒相关代码

### 1.0.25 更新内容
* 淘宝云应用框架库