import pymongo

# 数据库基本信息
db_configs = {
    'type': 'mongo',
    'host': '',
    'port': '27017',
    "user": "",
    "password": "",
    'db_name': ''
}


class Mongo():
    def __init__(self):
        self.db_name = db_configs.get("db_name")
        self.host = db_configs.get("host")
        self.port = db_configs.get("port")
        self.user = db_configs.get("user")
        self.password = db_configs.get("password")
        mongo_uri = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/'
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[self.db_name]


    def __del__(self):
        self.client.close()

    def update_many(self,table_name:str,data:dict,filter:dict):
        '''

        :param table_name: 表名
        :param data: 更新数据
        :param filter: 更新条件
        :return:
        '''
        return self.db[table_name].update_many(filter,data)

    def update(self,table_name:str,data:dict,filter:dict):
        '''
        更新单条记录
        :param table_name: 表名
        :param data: 更新数据
        :param filter: 更新条件
        :return:
        '''
        return self.db[table_name].update(filter,data)

    def find_one(self,table_name:str,filter:dict=None):
        '''
        查询单条
        :param table_name: 表名
        :param filter: 查询条件
        :return:
        '''
        return self.db[table_name].find_one(filter)

    def find(self,table_name:str,filter:dict=None):
        '''
        查询多条
        :param table_name: 表名
        :return:
        '''
        res = self.db[table_name].find(filter)
        return [i for i in res]

    def insert_one(self,table_name:str,data:dict):
        '''
        :param table_name: 表名
        :param data: 插入时的数据
        :return:str
        '''
        return self.db[table_name].insert_one(data)

    def insert_many(self,table_name:str,data:list):
        '''
        批量插入
        :param table_name: 表名
        :param data: 插入时的数据
        :return:
        '''
        return self.db[table_name].insert_many([i for i in data])

if __name__ == '__main__':
    m = Mongo()
    insert_data={
        "data":1
    }
    # res = m.insert_one("test",insert_data)
    # res = m.find_one("test",{"data":1})
    # res = m.find("test")
    # res = m.update("test", insert_data)
    res = m.update_many("test", {"$set":{"data":3}},insert_data)
    print(res)