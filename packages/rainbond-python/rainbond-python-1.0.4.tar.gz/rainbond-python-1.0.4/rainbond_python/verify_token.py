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
        self.uid = ''
        # 认证中心的 Redis 库号码
        self.redis_db_permission = os.environ.get('REDIS_DB_PERMISSION', None)
        self.secret_key = os.environ.get(
            'SECRET_KEY', None)  # 密钥
        self.expiration = os.environ.get('EXPIRATION', None)  # 超时时间
        # 认证中心 MongoDB 的库和集合名称
        self.mongo_db_name = os.environ.get('MONGODB_DB_NAME', None)
        self.mongo_permission = os.environ.get(
            'MONGODB_PERMISSION', None)  # 权限集合名称
        if self.redis_db_permission:
            self.redis_connect = RedisConnect(self.redis_db_permission)
        else:
            self.redis_connect = None  # 如果认证组件未连接，连接为空值
        self.mongo_role = os.environ.get('MONGODB_ROLE', None)  # 角色集合名称
        # 连接角色集合数据
        if self.mongo_role and self.mongo_db_name:
            self.role_db = DBConnect(
                db=self.mongo_db_name, collection=self.mongo_role)
        else:
            self.role_db = None
        self.mongo_user = os.environ.get('MONGODB_USER', None)  # 用户集合名称
        # 连接用户集合数据
        if self.mongo_user and self.mongo_db_name:
            self.user_db = DBConnect(
                db=self.mongo_db_name, collection=self.mongo_user)
        else:
            self.user_db = None
        # 通过 per_defaults 添加权限数据，例如：[{'center_name': '组件名称', 'permission_name': '权限名称'},]
        threading.Thread(target=self.add_permission_db,
                         args=(per_defaults, )).start()

    def verify_token(self, request):
        """验证token"""
        if not self.redis_connect:
            handle_abnormal(
                message='计算组件未建立连接/依赖到认证中心，无法验证凭证',
                status=500,
            )
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
            tok = toke_uid.split('--')
            self.uid = tok[0]  # 用户ID
            user_name = tok[1]  # 用户名称，通常是英文
            real_name = tok[2]  # 真实姓名，通常是中文
            return {'token_id': self.uid, 'user_name': user_name, 'real_name': real_name}
        handle_abnormal(
            message='来自 {0} 的账户已退出，需要重新登录'.format(request.remote_addr),
            status=401,
        )

    def add_permission_db(self, per_defaults):
        """添加默认权限中心/名称 到数据库"""
        time.sleep(10)
        if self.mongo_db_name and self.mongo_permission:
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
                        purview_name_id = db.write_one_docu(docu=find_dict)
                    else:
                        purview_name_id = sear_permission[0]['id']
                    if self.role_db:
                        # 添加权限集合信息到角色集合
                        for status in (0, 1, 2, 3):
                            permissions_set = {
                                'permission_status': status}.update(find_dict)
                            if not self.role_db.does_it_exist(permissions_set):
                                permissions_set.update(
                                    {'permission_id': purview_name_id})
                                self.role_db.write_one_docu(
                                    docu=permissions_set)
                    else:
                        logging.error('计算组件未建立连接/依赖到认证中心，无法注册对应的角色')
            except Exception as e:
                logging.warning('添加权限中心/名称失败', str(e))
        else:
            logging.error('计算组件未建立连接/依赖到认证中心，无法注册权限')

    def permission_verify(self, center_name, permission_name) -> int:
        """
        验证权限，通过所属 中心/权限名称 获取当前用户的权限
          center_name = '用户管理'  # 当前视图函数所属 中心
          permission_name = '用户列表'  # 当前视图函数所属 权限名称
          permission_status = 0  # 默认无权限, 更具获取的权限控制请求方式
        """
        if not self.redis_connect:
            handle_abnormal(
                message='计算组件未建立连接/依赖到认证中心-Redis服务，无法验证权限',
                status=500,
            )
        elif not self.role_db:
            handle_abnormal(
                message='计算组件未建立连接/依赖到认证中心-角色集合({0})，无法验证权限'.format(
                    self.mongo_role),
                status=500,
            )
        elif not self.user_db:
            handle_abnormal(
                message='计算组件未建立连接/依赖到认证中心-用户集合({0})，无法验证权限'.format(
                    self.mongo_user),
                status=500,
            )
        permission_status = 0
        user = self.user_db.find_docu_by_id(id=self.uid)  # 查询用户对应的角色数据
        role_name_list = user['role_name']  # 用户包含的所有角色名称
        for role_name in role_name_list:
            # 查询角色包含的权限集合，role_name + center_name + permission_name 不重复
            roles = self.role_db.find_docu(find_dict={
                                           'role_name': role_name, 'center_name': center_name, 'permission_name': permission_name}, many=False)
            if roles:
                permission_status = int(roles[0]['permission_status'])
        if permission_status == 0:
            handle_abnormal(
                message='无 "{0}-{1}" 的访问权限'.format(
                    center_name, permission_name),
                status=401,
            )
        return permission_status
