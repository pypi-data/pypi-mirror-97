# Rainbond Python

Python 云原生应用开发解决方案：

- rainbond-python：基于 Rainbond 平台和 Flask 框架的 Python 云原生开发基础库
- Flask：轻量级 Python Web 应用程序框架
- Rainbond：开源的企业级云原生平台，撑企业应用开发、架构、交付和运维的全流程

## 使用说明

快速开始创建一个 Python 云原生组件：

```python
rainbond -c demo-component
```

设置MongoDB的环境，以Windows为例：
```shell script
$ set MONGODB_HOST=127.0.0.1
$ set MONGODB_PORT=27017
```

### 异常处理

#### handle_abnormal

该方法用于抛出业务逻辑异常，简单示例如下：

```python
......
from rainbond_python.tools import handle_abnormal
......
@app.route('/api/1.0/demo', methods=['GET'])
def api_demo():
    parameter = Parameter(request)

    if parameter.method == 'GET':
        handle_abnormal(message='异常信息~~~', status=400)
......
```

这样，当用户请求时，响应内容如下：

```json
{
    "message": "异常信息~~~",
    "server_time": 20210220143830000,
    "host_name": "Z0jli2o0d2ymott0ggs6m",
    "host_ip": "128.19.80.115"
}
```

还可以通过 `header` 参数字典设置响应头字典，通过 `other` 参数添加附加信息字典，例如：

```python
handle_abnormal(message='2333~~~', status=400, other={'key1': 'value1', 'key2': {'a': 1}})
```

这样就可以将更详细的提示信息告知用户，响应内容如下：

```json
{
    "message": "2333~~~",
    "server_time": 20210220144625000,
    "host_name": "Z0jli2o0d2ymott0ggs6m",
    "host_ip": "128.19.80.115",
    "key1": "value1",
    "key2": {
        "a": 1
    }
}
```

#### error_handler

通过 `@app.errorhandler(xxx)` 重新定义常用的 *4xx* 和 *5xx* 状态码的异常响应。

```python
......
from flask import Flask, request, abort
from rainbond_python.error_handler import error_handler
......
app = Flask(__name__)
error_handler(app)
......
```

默认情况下，**Flask** 会自动捕获这些异常并返回响应，但是也可以通过 `abort()` 方法主动返回异常响应：

```python
abort(412)
```

对于 *200*、*4xx*、*5xx* 状态码，目前做出以下约定：

- *4xx*、*5xx* 的错误大部分交给 `error_handler` 封装方法处理
- 少数业务相关的 *4xx*、*5xx* 异常通过 `abort(xxx)` 方法主动处理
- 为了简单，忽略除 **200** 以外的其他 *2xx* 响应，且通过 `return data, 200, []` 返回，要注意的是 `data` 只有是必要参数，后面两个参数可以不写，`200, []` 就是默认值
- 业务代码通过 `return '错误信息XXX', 500` 返回自定义的异常响应

默认情况下 `error_handler()` 通过 `flask_cors` 库一键处理了服务端跨域问题，如果需要考虑安全问题，可以通过 `error_handler(app, simple_cors=False)` 取消跨域支持，同时，还可以重写跨域逻辑：

```python
......
error_handler(app, simple_cors=False)
from flask_cors import CORS
CORS(app, resources={r'/.*': {'origins': 'http://127.0.0.1:8888'}})
......
```

### Parameter

处理请求与响应参数的通用类。

```python
from rainbond_python.parameter import Parameter
```

#### 获取请求参数

通过 `Parameter` 类实例，可以获取以下信息：

- parameter.method: 请求类型
- parameter.headers: 请求头
- parameter.param_url: URL中传递的参数
- parameter.param_json: Json请求中的参数
- parameter.param_form: 表单请求中的参数

所有信息均为字典类型，通过 `json.dumps()` 可以直接作为响应返回：

```python
@app.route('/api/1.0/demo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_demo():
    parameter = Parameter(request)
    if parameter.method == 'GET':
        return json.dumps(parameter.param_url, ensure_ascii=False), 200, []
    elif parameter.method == 'POST':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []
    elif parameter.method == 'PUT':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []
    elif parameter.method == 'DELETE':
        return json.dumps(parameter.param_json, ensure_ascii=False), 200, []
```

#### 校验参数内容

通过 `Parameter` 类的 `verification()` 方法，可以判断参数字典是否符合要求：

```python
    elif parameter.method == 'POST':
        param = parameter.verification(checking=parameter.param_json, verify={'name': str, 'age': int})
```

其中 `checking` 参数是需要校验的参数字典，通常传递 `parameter.param_url`、`parameter.param_json` 或 `parameter.param_form`。第二个 `verify` 参数则是校验内容字典，需要指定 *参数名* 和 *参数类型* 作为字典项。如果请求中包含可选参数，可以将该参数的名称及其默认值输入到 `optional` 参数中，例如可以设置 *age* 参数为空时，默认填充为 *18* 岁：

```python
parameter.verification(checking=parameter.param_json, verify={'name': str, 'age': int}, optional={'age': 18})
```

如果判断失败，则直接返回异常响应，响应体中包含明确的提示信息。默认情况下，`str` 类型的 必选参数不能为空字符串，如果需要为空，可以通过 `null_value=True` 进行设置，或者将其作为可选参数处理。

#### 校验文件表单

如果需要接收表单提交的文件对象，可以使用 `verification_file()` 方法对请求中的表单文件字段进行校验：

```python
    elif parameter.method == 'POST':
        param = parameter.verification(checking=parameter.param_form, verify={'id': str})
        param_file = parameter.verification_file(verify_field=['updata'])
```

如上面的代码，如果请求中没有名为 *updata* 的表单文件字段，会直接返回异常信息。该方法与 `verification()` 方法可以同时使用。如果还需要判断上传文件的后缀名，可以通过 `verify_suffix` 参数进行配置：

```python
param_file = parameter.verification_file(verify_field=['updata'], verify_suffix=['jpg'])
# 二者效果相同，但是列表类型可以同时指定多个后缀名称
param_file = parameter.verification_file(verify_field=['updata'], verify_suffix=[['jpg']])
```

该方法会返回 `werkzeug.datastructures.ImmutableMultiDict` 对象，即通过 `request.files` 获取到的对象，接下来就可以：

- 通过 `param_file.get('xxxx')` 获取到文件对象
- 通过 `param_file.get('xxxx').filename` 获取具体文件名称
- 通过 `param_file.get('xxxx').save('/xxx/xxx.jpg')` 保存文件到本地

### DBConnect

处理 MongoDB 读写行为的通用类。

```python
from rainbond_python.db_connect import DBConnect
db = DBConnect(db='db_name', collection='collection_name')
```

#### 分页查询

仅支持 **GET** 请求，使用非常简单，直接把 `Parameter` 类的实例传递给 `DBConnect` 类的 `find_paging()` 方法即可：

```python
@app.route('/api/1.0/demo', methods=['GET'])
def api_demo():
    parameter = Parameter(request)
    if parameter.method == 'GET':
        find_data = db.find_paging(parameter)
        return find_data, 200, []
```

内部组件或外部客户端通过 */api/1.0/demo?page_size=10&current=1&columns=["title"]&sort_order=[""]&filtered_value=["标题"]* 即可访问，请求参数如下：

- page_size: 每页条数，从1开始计算
- current: 当前页数，从1开始计算
- columns: 受控列
- sort_order: 排序顺序（对应受控列），必须与受控列长度一致，""=不排序、asc=升序、desc=降序
- filtered_value: 筛选值（对应受控列），必须与受控列长度一致
- start_date: 可选，开始日期（区间查询），支持日期（2020-10-1）格式和时间戳（601481600）格式
- end_date: 可选，结束日期（区间查询），同上，必须成对出现

由于技术原因，`filtered_value` 列表目前不支持 `int` 型数据的模糊查询。同时 `start_date` 和 `end_date` 如果传递的是时间戳格式，能精确到秒。

#### 写文档

##### 写入单个文档

```python
insert_dict = {'name': 'Xiao Ming', 'age': 23}
db.write_one_docu(docu=insert_dict)
```

如果写入失败，会直接返回异常响应，如果成功则会返回新数据的 `_id` 值。

##### 写入多个文档

```python
insert_dict_list = [{'name': 'Xiao Ming', 'age': 23},{'name': 'lao Yang', 'age': 35}]
db.write_many_docu(docu_list=insert_dict_list)
```

如果写入失败，会直接返回异常响应，如果成功则会返回新数据的 `_id`值的列表。

#### 文档是否存在

```python
examine_dict = {'name': 'Xiao Ming'}
if db.does_it_exist(docu=examine_dict):
    print('Docu already exists')
else:
    print('Docu does not exist')
```

#### 更新文档

同样的，如果更新失败，也会直接返回异常响应。

##### 更新单个匹配文档

```python
find_dict = {'name': 'Xiao Ming'}
modify_dict = {'name': 'Xiao Hong'}
db.update_docu(find_docu=find_dict, modify_docu=modify_dict)
```

##### 更新全部匹配文档

```python
find_dict = {'age': 23}
modify_dict = {'name': '23 year old'}
db.update_docu(find_docu=find_dict, modify_docu=modify_dict, many=True)
```

该方法会返回一个包含 `matched_count` 和 `modified_count` 即匹配/影响数据条数的字典。

#### 删除文档

删除文档分为 **真删除** 和 **假删除** 两种方式，通过 `delete_docu()` 方法实现，该方法会返回一个包含 `deleted_count` 和 `false_delete` 的字典。。

##### 真删除文档

```python
db.delete_docu(find_docu={'id': '60053fa139842d28d7563c6c'})
```

##### 假删除文档

```python
db.delete_docu(find_docu={'id': '60053fa139842d28d7563c6c'}, false_delete=True)
```

假删除操作会在对应的文档中添加一个 `remove_time` 字段，里面记录这个文档被移除的时间。

##### 批量删除文档

```python
db.delete_docu(find_docu={'id': {'$in': ['111', '222']}}, many=True)
```

#### 查询文档

通过 `find_docu()` 标准查询方法时，无论查询单个还是多个，返回均是 `list` 类型数据，没有匹配数据时返回空列表。

##### 查询单个匹配文档

```python
find_dict = {'title': {'$regex': '标题'}}
find_data_list = db.find_docu(find_dict=find_dict, many=False)
print(find_data_list[0])
```

##### 查询全部匹配文档

```python
find_dict = {'title': {'$regex': '标题'}}
find_data_list = db.find_docu(find_dict=find_dict)
for find_data in find_data_list:
    print(find_data)
```

##### 根据id查找文档

```python
from rainbond_python.db_connect import DBConnect
db = DBConnect('unitest_rainbond_python', 'test_db_connect')
id = db.write_one_docu({'name': 'LaoXu'})
docu = db.find_docu_by_id(str(id))

# 当id不存在时，默认会使用abort抛出异常
fail_docu = db.find_docu_by_id('6008daa19223551b00548ded')
# 可以将raise_err=False时，id不存在会返回None
fail_docu = db.find_docu_by_id('6008daa19223551b00548ded',raise_err=False)
```

该方法返回记录字典，且把'_id'转换为了str类型

##### 根据id列表查找文档

```python
from rainbond_python.db_connect import DBConnect
db = DBConnect('unitest_rainbond_python', 'test_db_connect')
docu_list = db.find_docu_by_id_list(['6008daa19223551b00548ded','6008daa29223551b00548dee'])
```

该方法返回记录字典列表，且把'_id'转换为了str类型。当所有id不存在时，返回[]

### 文件下载

在网络上传输文件，目前主要有下载和流式传输两种方案，分别 `rainbond_python.download` 包的对应 `download_file()` 和 `download_flow()` 方法。

#### 普通下载

通常用于文档文件（压缩包/PDF/TXT等文档），这种方式必须等全部内容传输完毕后，才能在本地机器打开：

```python
......
from rainbond_python.download import download_file
......
    if parameter.method == 'GET':
        download_response = download_file(file_path='C:/Users/xxx/Desktop', file_name='新建文本文档.txt'])
        return download_response
......
```

#### 流式传输

通常用于多媒体文件（视频/音频/直播流等场景），文件信息由服务器向用户计算机连续实时地传送，不必等到整个文件全部下载完毕，通常经过几秒或十几秒的启动延时即可打开：

```python
......
from rainbond_python.download import download_flow
......
    if parameter.method == 'GET':
        download_response = download_flow(file_path='C:/Users/xxx/Desktop', file_name='微视频.mp4'])
        return download_response
......
```

#### 打包目录生成zip文件下载（在内存中打包）

通常用于将现有目录文件，打包成zip文件，提供用户下载。打包zip文件数据在内存中完成，完成后从内存中读取二进制数据，并且回收内存。
参数save_zip表示本地是否存储打包zip文件，默认值为 False，为True时,打包文件保存在打包目录同级

```python
from rainbond_python.download import download_directory

......
    if parameter.method == 'GET':
        download_response = download_directory(dir_path='C:/Users/xxx/project', zip_name='project.zip'],save_zip=False)
        return download_response
......
```

### RedisConnect

处理 Redis 读写行为的通用类。

```python
from rainbond_python.redis_connect import RedisConnect
redis_connect = RedisConnect(db=0)
```

### 通用方法

#### handle_date()

将 *2020-10-1* 或 *601481600* 即日期格式或时间戳格式的字符串，处理成 Python 的 `datetime.datetime` 数据：

```python
from rainbond_python.tools import handle_date
print(handle_date(date='2020-10-1'))
print(handle_date(date='2020-10-31', date_type='end'))
```

通过 `date_type` 可以设置是日期的开始（`start`）还是一天的结束（`end`）时间。

#### handle_db_dict()

将 MongoDB 字典数据中的 `_id` 转换为 `str` 类型、时间转换成时间戳：

```python
query_dict = self.mongo_collection.find_one({'title': {'$regex': '标题1'}})
handle_db_dict(query_dict)
```

#### handle_db_to_list()

将 MongoDB 的列表中的 `_id` 转换为 `str` 类型，并转换为字典列表（原db的id是ObjectId类型，转为json会报错）：

```python
from rainbond_python.tools import handle_db_to_list
from rainbond_python.db_connect import DBConnect

def test_handle_db_to_list():
    db = DBConnect('unitest_rainbond_python', 'test_parameter')
    old_list = db.mongo_collection.find({})
    new_list = handle_db_to_list(old_list)
    print('new_list is a list of dict',new_list)
```

#### handle_time_difference()

计算前端传递的两个时间戳之间，相差多少秒，返回 `float` 类型，解决前后端时间戳（前端的毫秒是整数位、Python的毫秒是小数位）差异问题：

```python
from rainbond_python.tools import handle_time_difference
handle_time_difference(start_timestamp=1614051008, end_timestamp=1614051008)
```

## 开发与测试

### 调试开发

基础调试代码的 `demo.py` 即 *rainbond -c demo-component* 命令创建项目中的 `app.py` 文件，是一个可以快速开始的基础代码项目。

在本地调试时，在 **demos** 目录下创建 `dev_xxxxx.py`，并复制 `demo.py` 文件里的代码，并在里面调试 *rainbond_python* 目录下的代码。（本地创建的 dev_*.py 文件会被忽略，不会被提交），同时要在开头处添加下面代码，以调用基础包中的代码：

```python
......
import sys
sys.path.append('..')
from rainbond_python.parameter import Parameter
from rainbond_python.error_handler import error_handler
from rainbond_python.db_connect import DBConnect
......
```

### 单元测试

单元测试在 /tests/* 目录下

* 执行单元测试
```shell script
$ pytest
```

## 参考

- [Restful API](https://www.runoob.com/w3cnote/restful-architecture.html) : 具体的组件API开发标准
- [12 Factor](https://12factor.net/zh_cn/) : 符合十二要素的才是云原生应用
- [RainBond](https://www.rainbond.com/docs/) : 一个开源的云原生平台
