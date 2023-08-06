
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class MiddlerProductModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None):
        super(MiddlerProductModel, self).__init__(MiddlerProduct, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class MiddlerProduct:

    def __init__(self):
        super(MiddlerProduct, self).__init__()
        self.id = 0  # id
        self.guid = ""  # guid
        self.product_name = ""  # 产品名称
        self.product_icon = ""  # 产品图标
        self.product_type = 0  # 产品类型：1云开发，2云应用
        self.db_key = ""  # 数据库key
        self.contains_name = ""  # 产品服务名称列表（如：一起来盖楼,互动游戏宝,互动PK宝盒）
        self.is_release = 0  # 是否发布（1是0否）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'guid', 'product_name', 'product_icon', 'product_type', 'db_key', 'contains_name', 'is_release', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "middler_product_tb"
    