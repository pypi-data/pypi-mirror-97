
# seven_framework

## 天志互联Python开发库

### 1.0.116 更新内容
* tornado handler自带monitor.py

### 1.0.115 更新内容
* log优化
* clickhouse帮助类

### 1.0.114 更新内容
* log日志配置修改,添加redis日志存储

### 1.0.113 更新内容
* 增加JsonHelper json_dumps()  常用格式的反序列化

### 1.0.112 更新内容
* 优化SignHelper公共加密类

### 1.0.111 更新内容
* 优化SignHelper公共加密类

### 1.0.110 更新内容
* 优化pymysql暗改转移方法

### 1.0.108 更新内容
* 添加腾讯云对象存储

### 1.0.107 更新内容
* 兼容base_model get_total时传groupby时报错的问题

### 1.0.106 更新内容
* 添加阿里oss2依赖

### 1.0.105 更新内容
* 添加阿里oss2帮助类

### 1.0.104 更新内容
* 优化file添加金山云(KS3)存储帮助类

### 1.0.102 更新内容
* file添加金山云(KS3)存储帮助类
* 调整filter_check_params 方法兼容application/json为空时自动再查找普通参数

### 1.0.101 更新内容
* http_log增加打印公共返回字段

### 1.0.100 更新内容
* 修复mysql update bug

### 1.0.99 更新内容
* 修复mysql bug

### 1.0.98 更新内容
* 优化Timehelper 关于本周/月/年 第一天及最后一天时间,以及指定日期的对比函数

### 1.0.96 更新内容
* 新增Timehelper 关于本周/月/年 第一天及最后一天时间,以及指定日期的对比函数
* 优化mysql 传参如果不为list的情况下,参数为0报错的bug

### 1.0.95 更新内容
* 新增CSVHelper

### 1.0.94 更新内容
* 优化base_model 解决get_entity_by_id id=0报错的BUG

### 1.0.93 更新内容
* 优化base_model

### 1.0.92 更新内容
* 修改base_model 更新数据库未影响行数时返回False

### 1.0.91 更新内容
* DBUtils 高版本写法变更,依赖版本调整

### 1.0.90 更新内容
* TimeHelper 增加时间差集计算

### 1.0.89 更新内容
* 优化企业微信帮助类

### 1.0.88 更新内容
* 优化企业微信帮助类

### 1.0.87 更新内容
* 添加企业微信帮助类
* 添加公共签名帮助类
* 兼容http post请求

### 1.0.86 更新内容
* 修改毫秒级时间戳

### 1.0.85 更新内容
* 添加毫秒级时间戳

### 1.0.84 更新内容
* 修复redis db=0是异常的bug

### 1.0.83 更新内容
* 修复http post json请求bug

### 1.0.82 更新内容
* 修复redis添加init参数bug

### 1.0.81 更新内容
* Redis添加init参数,可直接指定配置字典即可

### 1.0.80 更新内容
* 优化sha256加密方法

### 1.0.79 更新内容
* 添加sha256加密方法

### 1.0.78 更新内容
* TimeHelper添加更改格式化时间格式的方法

### 1.0.77 更新内容
* log入库时间戳格式调整

### 1.0.75 更新内容
* 事务添加导出sql语句方法

### 1.0.74 更新内容
* 优化mysql事务

### 1.0.73 更新内容
* base_model增加update_list方法

### 1.0.72 更新内容
* 优化DbTransaction 事务类

### 1.0.71 更新内容
* 优化DbTransaction 事务类

### 1.0.70 更新内容
* 增加DbTransaction 事务类

### 1.0.69 更新内容
* 修复base_model BUG

### 1.0.68 更新内容
* 修改企业微信通知添加项目产生的错误

### 1.0.67 更新内容
* base_model 增加事务处理

### 1.0.66 更新内容
* 添加框架依赖

### 1.0.65 更新内容
* 添加框架依赖

### 1.0.64 更新内容
* 增加excel帮助类
* 增加二维码帮助类

### 1.0.63 更新内容
* 修改file->ufile cdn前缀问题

### 1.0.62 更新内容
* base_model 修改page_list函数的count()字段

### 1.0.61 更新内容
* log记录数据库添加record_time字段
* base_handler->get_params 添加是否去除前后空格选填参数

### 1.0.60 更新内容
* base_model conver_type修改

### 1.0.59 更新内容
* 企业微信通知加项目名称

### 1.0.58 更新内容
* 修改host处理

### 1.0.57 更新内容
* 修改log写入数据库转义问题

### 1.0.56 更新内容
* 优化base_model 分页函数

### 1.0.55 更新内容
* 优化全局异常报错处理

### 1.0.54 更新内容
* 优化mysql连接

### 1.0.53 更新内容
* 添加DBUtils依赖

### 1.0.52 更新内容
* 优化mysqlhelper 连接池
* basemodel配合mysql修改

### 1.0.51 更新内容
* 修改urlencode bug

### 1.0.50 更新内容
* 优化log添加数据库记录

### 1.0.49 更新内容
* log添加数据库记录
* ufile.py 改名为 file.py
* file.py 添加ufile 下载文件方法

### 1.0.48 更新内容
* 优化filter_check_params

### 1.0.47 更新内容
* JsonEncoder 支持decimal类型

### 1.0.46 更新内容
* 修复ufile bug

### 1.0.45 更新内容
* 修复ufile包名冲突的问题

### 1.0.44 更新内容
* 增加ufile封装

### 1.0.43 更新内容
* 修复企业微信通知bug
* 修改prepare的http请求信息支持json参数

### 1.0.42 更新内容
* @filter_check_params支持接收json传参

### 1.0.41 更新内容
* 添加testing环境配置

### 1.0.40 更新内容
* 修复已知BUG

### 1.0.39 更新内容
* 添加企业微信报警(notice.py)
* 修改base_handler内filter_check_params装饰器无需输入可选参数

### 1.0.38 更新内容
* 修复引用

### 1.0.37 更新内容
* 修复json bytes转码BUG
* base_handler 添加body参数转dict函数

### 1.0.36 更新内容
* 修复http请求控制台日志bug

### 1.0.35 更新内容
* 添加http请求控制台日志

### 1.0.33 更新内容
* 添加base_tornado

### 1.0.31 更新内容
* 添加coding帮助类

### 1.0.30 更新内容
* 添加依赖源

### 1.0.29 更新内容
* 优化base_model 增加seven_framework架引用

### 1.0.27 更新内容
* 增加控制台基础引用 base_console

### 1.0.26 更新内容
* 优化CryptoHelper 编码问题
* 增加CryptoHelper 针对bytes的md5加密
* 优化BaseHandler body转实体方法

### 1.0.25 更新内容
* CryptoHelper增加sha1加密

### 1.0.24 更新内容
* base_handler增加request_body_to_entity方法

### 1.0.23 更新内容
* 优化base_handler get_param 空值也返回默认值

### 1.0.22 更新内容
* 优化base_handler filter_check_params 装饰器,允许不检查必填参数

### 1.0.20 更新内容
* 优化MysqlHelper

### 1.0.19 更新内容
* 将MysqlHelper 的condition参数 拆开为 where/group_by/order_by/limit 参数
* 将MysqlHelper及base_model 增加事务执行函数transaction_execute

### 1.0.18 更新内容
* 解决base_api_handler的初始化bug

### 1.0.17 更新内容
* 优化框架结构
* 修改CryptoHelper 的 AES加解密方法