import os
import time
import threading
from .redis_connect import RedisConnect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .tools import handle_abnormal
from .db_connect import DBConnect
import logging

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class VerifyToken:
    def __init__(self, per_defaults=[{}]):
        # 通过 per_defaults 添加权限数据，例如：[{'center_name': '组件名称', 'permission_name': '权限名称'},]
        threading.Thread(target=self.add_permission_db,
                         args=(per_defaults, )).start()
        self.uid = ''
        self.redis_db_permission = os.environ.get('REDIS_DB_PERMISSION', 6013)
        self.secret_key = os.environ.get(
            'SECRET_KEY', 'dsfsdfs@#$#@FDgfdgdg325423523525fsdfg*')  # 密钥
        self.expiration = os.environ.get('EXPIRATION', 3600)  # 超时时间
        self.redis_connect = RedisConnect(self.redis_db_permission)
        self.mongo_db_name = os.environ.get('MONGODB_DB_NAME', 'universal')
        self.mongo_permission = os.environ.get(
            'MONGODB_PERMISSION', 'permission')

    def verify_token(self, request):
        """验证token"""
        token = request.headers.get('token')  # 获取请求头中的Token
        s = Serializer(self.secret_key, self.expiration)
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            handle_abnormal(
                message='来自 {0} 的 Token 验证失败'.format(request.remote_addr),
                status=401,
            )
        toke_uid = data.get('id')  # token中传来的
        # redis中写入的
        redis_uid = self.redis_connect.get_(toke_uid.split('--')[0])
        if redis_uid == toke_uid:
            self.uid = toke_uid.split('--')[0]
            return toke_uid.split('--')[0]  # user_id
        handle_abnormal(
            message='来自 {0} 的账户已退出，需要重新登录'.format(request.remote_addr),
            status=401,
        )

    def add_permission_db(self, per_defaults):
        """添加默认权限中心/名称 到数据库"""
        time.sleep(10)
        # 添加权限中心/名称到权限管理
        try:
            for per in per_defaults:
                db = DBConnect(db=self.mongo_db_name,
                               collection=self.mongo_permission)
                # 查询是否已存在
                find_dict = {'center_name': str(per['center_name']),
                             'permission_name': str(per['permission_name'])}
                sear_permission = db.find_docu(
                    find_dict=find_dict, many=False)
                if not sear_permission:
                    db.write_one_docu(docu=find_dict)
        except Exception as e:
            logging.warning('添加权限中心/名称失败', str(e))

    def permission_verify(self, center_name_this, permission_name_this) -> int:
        """
        验证权限，通过所属 中心/权限名称 获取当前用户的权限
          center_name_this = '用户管理'  # 当前视图函数所属 中心
          permission_name_this = '用户列表'  # 当前视图函数所属 权限名称
          per_status_this = 0  # 默认无权限, 更具获取的权限控制请求方式
        """
        per_status_this = 0
        # 查询redis中当前用户的权限集合
        redis_key = self.uid + center_name_this + permission_name_this
        per_set_redis_info = self.redis_connect.get_(redis_key)
        if per_set_redis_info is None:
            handle_abnormal(
                message='认证中心 Redis 查询: "{0}"={1}'.format(
                    redis_key, per_set_redis_info),
                status=500,
            )
        if per_set_redis_info:
            per_status_this = int(per_set_redis_info)
        if per_status_this == 0:
            handle_abnormal(
                message='无 "{0}-{1}" 的访问权限({2})'.format(
                    center_name_this, permission_name_this, per_set_redis_info),
                status=401,
            )
        return per_status_this
