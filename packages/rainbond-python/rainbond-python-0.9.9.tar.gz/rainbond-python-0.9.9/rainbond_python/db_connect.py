import os
import json
import pymongo
import logging
import math
import copy
from datetime import datetime
from .parameter import Parameter
from .tools import handle_date, handle_db_to_list, handle_db_dict, handle_db_id, handle_db_remove, handle_abnormal
from flask import abort, Response
from bson import ObjectId

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class DBConnect:
    def __init__(self, db: str, collection: str, home_key='MONGODB_HOST', port_key='MONGODB_PORT'):
        self.mongo_home = os.environ.get(home_key, '127.0.0.1')
        self.mongo_port = os.environ.get(port_key, 27017)

        if not self.mongo_home or not self.mongo_port:
            logging.error('MongoDB(组件)的组件连接信息是不完整的')

        self.mongo_client = pymongo.MongoClient(
            host=self.mongo_home,
            port=int(self.mongo_port)
        )
        self.mongo_db = self.mongo_client[db]
        self.mongo_collection = self.mongo_db[collection]

    def write_one_docu(self, docu: dict) -> str:
        try:
            # 兼容直接指定ID的创建方式
            docu = handle_db_id(docu)
            # 添加创建时间和更新时间，日期格式
            if not docu.__contains__('creation_time'):
                docu['creation_time'] = datetime.today()
            if not docu.__contains__('update_time'):
                docu['update_time'] = datetime.today()
            new_data = self.mongo_collection.insert_one(docu)
            return str(new_data.inserted_id)
        except Exception as err:
            handle_abnormal(
                message='MongoDB(组件)出现写入错误: {0}'.format(json.dumps(docu)),
                status=500,
                other={'prompt': str(err)}
            )

    def write_many_docu(self, docu_list: list) -> list:
        try:
            new_docu_list = []
            for docu in docu_list:
                if isinstance(docu, dict):
                    # 添加创建时间和更新时间，日期格式
                    if not docu.__contains__('creation_time'):
                        docu['creation_time'] = datetime.today()
                    if not docu.__contains__('update_time'):
                        docu['update_time'] = datetime.today()
                    # 深渊巨坑，字段append()到列表中要用深拷贝
                    deep_docu = copy.deepcopy(docu)
                    new_docu_list.append(deep_docu)
                else:
                    handle_abnormal(
                        message='参数docu_list格式不正确，要求为：[{},{},{}...]',
                        status=500,
                        other={'prompt': {'docu_list': docu_list}}
                    )
            new_data_list = self.mongo_collection.insert_many(new_docu_list)
            new_id_list = [str(_id) for _id in new_data_list.inserted_ids]
            return new_id_list
        except Exception as err:
            handle_abnormal(
                message='MongoDB(组件)出现写入错误',
                status=500,
                other={'prompt': str(err)}
            )

    def does_it_exist(self, docu: dict) -> bool:
        count = self.mongo_collection.count_documents(docu)
        if count != 0:
            return True
        else:
            return False

    def update_docu(self, find_docu: dict, modify_docu: dict, many=False) -> dict:
        try:
            # 将参数id处理成符合mongo格式的_id对象
            find_docu = handle_db_id(find_docu)
            # 排除假删除数据
            find_docu = handle_db_remove(find_docu)
            # 重置更新时间
            if not modify_docu.__contains__('update_time'):
                modify_docu['update_time'] = datetime.today()
            # 将更新内容转化为mongo能识别的更新格式
            modify_docu = {'$set': modify_docu}
            if many:
                student = self.mongo_collection.update_many(
                    find_docu, modify_docu)
            else:
                student = self.mongo_collection.update_one(
                    find_docu, modify_docu)
            # 返回匹配条数、受影响条数
            return {'matched_count': student.matched_count, 'modified_count': student.modified_count}
        except Exception as err:
            handle_abnormal(
                message='MongoDB(组件)出现更新错误',
                status=500,
                other={'prompt': str(err)}
            )

    def delete_docu(self, find_docu: dict, many: bool = False, false_delete: bool = False) -> dict:
        try:
            if false_delete:
                # 假删除流程
                modify_dict = {'remove_time': datetime.today()}
                result = self.update_docu(
                    find_docu=find_docu, modify_docu=modify_dict, many=many)
                if not result['modified_count']:
                    logging.warning('MongoDB(组件)出现删除异常: 没有任何文档被假删除')
                return {'deleted_count': result['modified_count'], 'false_delete': false_delete}
            else:
                find_docu = handle_db_id(find_docu)
                find_docu = handle_db_remove(find_docu)
                # 真删除流程
                if many:
                    # 文档批量删除方式
                    result = self.mongo_collection.delete_many(find_docu)
                else:
                    # 文档精确删除方式
                    result = self.mongo_collection.delete_one(find_docu)
                if not result.deleted_count:
                    logging.error('MongoDB(组件)出现删除异常: 没有任何文档被真删除')
                # 返回删除成功条数
                return {'deleted_count': result.deleted_count, 'false_delete': false_delete}
        except Exception as err:
            handle_abnormal(
                message='MongoDB(组件)出现删除错误',
                status=500,
                other={'prompt': str(err)}
            )

    def find_docu(self, find_dict: dict, many: bool = True) -> list:
        try:
            deep_find_dict = copy.deepcopy(find_dict)  # 深拷贝
            deep_find_dict = handle_db_id(deep_find_dict)
            deep_find_dict = handle_db_remove(deep_find_dict)
            if many:
                # 多文档查询方式
                query_cursor = self.mongo_collection.find(deep_find_dict)
                return handle_db_to_list(query_cursor)
            else:
                # 单文档查询方式
                query_dict = self.mongo_collection.find_one(deep_find_dict)
                if not query_dict:
                    return []
                return [handle_db_dict(query_dict)]
        except Exception as err:
            handle_abnormal(
                message='MongoDB(组件)出现查询错误',
                status=500,
                other={'prompt': str(err)}
            )

    def find_docu_by_id(self, id: str, raise_err=True) -> dict:
        """
        根据id查找记录
        :param id:记录id
        :param raise_err:是否抛出异常（使用abort抛出），否则返回None
        :return: 将结果转换为字典
        """
        if not isinstance(id, str):
            handle_abnormal(
                message='类型错误, 预期 %s ,却得到 %s' % (str, type(id)),
                status=400,
            )
        entity = self.find_docu({'id': id}, many=False)
        if entity is None or len(entity) == 0:
            if raise_err:
                handle_abnormal(
                    message='找不到 id= %s 的记录' % (id,),
                    status=400,
                )
            else:
                return {}
        return entity[0]

    def find_docu_by_id_list(self, id_list: list) -> list:
        """
        根据id列表查找记录列表
        :param id_list:
        :return:
        """
        if not isinstance(id_list, list):
            handle_abnormal(
                message='类型错误, 预期 %s ,却得到 %s' % (list, type(id_list)),
                status=400,
            )
        id_search = []
        for id in id_list:
            id_search.append({'_id': ObjectId(id)})
        find_dict = {'$or': id_search}
        data = self.find_docu(find_dict)
        return data

    def find_paging(self, parameter: Parameter) -> dict:
        parameter.verification(
            checking=parameter.param_url,
            verify={
                'page_size': str, 'current': str, 'columns': str, 'sort_order': str,
                'filtered_value': str, 'start_date': str, 'end_date': str, 'date_type': str
            },
            optional={'start_date': '', 'end_date': '', 'date_type': 'update_time'})
        param = parameter.param_url
        try:
            page_size = int(param['page_size'])  # 每页条数
            current = int(param['current'])  # 当前页数
            if current < 1 or page_size < 1:
                raise Exception('当前页数和每页条数都从 1 开始计算')
            else:
                current -= 1
            columns = json.loads(param['columns'])  # 受控列
            # 排序顺序（对应受控列），asc=升序，desc=降序
            sort_order = json.loads(param['sort_order'])
            # 筛选值（对应受控列）
            filtered_value = json.loads(param['filtered_value'])
            start_date = handle_date(date=param['start_date'])  # 可选——开始日期
            # 可选——结束日期，与开始日期组成日期区间
            end_date = handle_date(date=param['end_date'], date_type='end')
            if len(columns) != len(sort_order) or len(columns) != len(filtered_value):
                raise Exception('三个控制列表的长度不一致')
            # 查找假删除数据的数据量
            remove_count = self.mongo_collection.find(
                {'remove_time': {'$exists': True}}).count()
            # 查找字典和排序列表，处理假删除数据
            find_dict = handle_db_remove({})
            sort_list = []
            if len(columns):
                for i in range(len(columns)):
                    # 整理请求参数中的筛选项字典
                    if type(filtered_value[i]) == int:
                        find_dict[columns[i]] = filtered_value[i]
                    elif columns[i] == 'id' or columns[i] == '_id':
                        find_dict['_id'] = ObjectId(str(filtered_value[i]))
                    else:
                        if filtered_value[i].strip() != '':
                            find_dict[columns[i]] = {
                                '$regex': filtered_value[i]}
                    # 整理请求参数中的筛排序列表
                    if type(sort_order[i]) != str:
                        abort(Response('计算组件分页参数异常: 排序参数不支持 int 类型', 400, {}))
                    sort_value = sort_order[i].strip()
                    if sort_value == 'asc':
                        sort_list.append((columns[i], pymongo.ASCENDING))
                    elif sort_value == 'desc':
                        sort_list.append((columns[i], pymongo.DESCENDING))
                    elif sort_value == '':
                        pass
                    else:
                        abort(Response('计算组件分页参数异常: 仅支持 asc 和 desc 两个值', 400, {}))
            # 仅存在日期查询区间参数时，进行额外的创建时间区间查询
            if start_date and end_date:
                find_dict[param['date_type']] = {
                    '$gte': start_date, '$lte': end_date}
            # 对排序规则处理
            if sort_list:
                find_data = self.mongo_collection.find(find_dict).sort(sort_list).limit(
                    page_size).skip(page_size * current)
            else:
                find_data = self.mongo_collection.find(find_dict).limit(
                    page_size).skip(page_size * current)
            # 处理返回数据
            records_filtered = find_data.count()
            # 判断数据是否为空
            if find_data.count():
                # 处理返回数据
                query_result = handle_db_to_list(find_data)
                return {
                    'records_total': self.mongo_collection.estimated_document_count() - remove_count,
                    'records_filtered': records_filtered,
                    'query_result': query_result,
                    'total_pages': math.ceil(records_filtered / page_size),
                    'remove_count': remove_count,
                }
            else:
                return {
                    'records_total': self.mongo_collection.estimated_document_count() - remove_count,
                    'records_filtered': 0,
                    'query_result': [],
                    'total_pages': 0,
                    'remove_count': remove_count,
                }
        except Exception as err:
            handle_abnormal(
                message='计算组件分页参数异常',
                status=400,
                other={'prompt': str(err)}
            )
