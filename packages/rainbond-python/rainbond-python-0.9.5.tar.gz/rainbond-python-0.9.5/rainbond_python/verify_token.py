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
        self.redis_db = os.environ.get('REDIS_DB', 6013)
        self.secret_key = os.environ.get(
            'SECRET_KEY', 'dsfsdfs@#$#@FDgfdgdg325423523525fsdfg*')
        self.expiration = os.environ.get('EXPIRATION', 3600)
        self.redis_connect = RedisConnect(self.redis_db)

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
                db = DBConnect(db='universal', collection='permission')
                # 查询是否已存在
                find_dict = {'center_name': per['center_name'],
                             'permission_name': per['permission_name']}
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
        per_set_redis_info = self.redis_connect.get_(
            self.uid + center_name_this + permission_name_this)
        if per_set_redis_info:
            per_status_this = int(per_set_redis_info)
        if per_status_this == 0:
            handle_abnormal(
                message='无 "{0}-{1}" 的访问权限'.format(
                    center_name_this, permission_name_this),
                status=401,
            )
        return per_status_this
