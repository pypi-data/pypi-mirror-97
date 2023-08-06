#!/usr/bin/env python 
# coding=utf-8
# @Time : 2020/9/24 10:00 
# @Author : HL 
# @Site :  
# @File : DatabaseMogo.py 
# @Software: PyCharm
from pymongo import MongoClient


class Mongo_DB(object):

    def __init__(self, database, collection):
        self.client = MongoClient('192.168.0.139', 27017)
        self.db = self.client[database][collection]

    def add_one(self, post):
        '''新增数据'''
        return self.db.VehicleConfigParam.insert_one(post)

    def add_many(self, infos):
        '''新增多条数据'''
        # infos = [
        #     {'name': 'ben', 'age': 18, 'sex': "male", 'grade': 80, 'adress': "china"},
        #     {'name': 'sum', 'age': 19, 'sex': "male", 'grade': 75, 'adress': "china"}
        # ]
        return self.db.VehicleConfigParam.insert_many(infos)

    def get_one(self):
        '''查询一条数据'''
        return self.db.VehicleConfigParam.find_one()

    def get_more(self, condition):
        '''查询多条数据'''
        return self.db.find(condition)
    def get_mores(self):
        '''查询多条数据'''
        return self.db.find()

    def get_one_from_oid(self, obj):
        '''查询指定ID的数据'''
        # obj = ObjectId(oid)
        return self.db.VehicleConfigParam.find_one(obj)

    def save_no_repeat(self, condition, data):
        self.db.update_one(condition, {'$set': data}, True)

    def is_exist(self, obj):
        # python中mongodb判断某字段的值是否存在
        count = self.db.count_documents(obj)
        return count

    def update_one(self):
        '''修改一条数据'''
        return self.db.VehicleConfigParam.update_one({'age': 20}, {'$inc': {'x': 10}})

    def update_many(self):
        '''修改多条数据'''
        return self.db.VehicleConfigParam.update_many({}, {'$inc': {'age': 5}})

    def dalete_one(self, obj):
        '''删除一条数据'''
        return self.db.VehicleConfigParam.delete_one(obj)

    def delete_many(self, obj):
        '''删除多条数据'''
        return self.db.VehicleConfigParam.delete_many(obj)

    def crawl(self):
        # s = self.db.VehicleConfigParam.insert_many([{'name': '18', 'price': 100}])
        # print(s)
        data = {'name': '12', 'price': 245}
        self.db.update({'name': '12'}, {'$set': data}, True)

# if __name__ == '__main__':
#     # Mongo_DB('caximofan','VehicleConfigParam').crawl()
#     s = Mongo_DB('caximofan', 'Bidding').get_mores()
#     for x in s:
#         print(x)
