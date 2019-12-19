-- qa.db
create database if not exists qadb default character set utf8mb4 default collate utf8mb4_general_ci;

drop table if exists `qa_autotest_case`;
create table `qa_autotest_case` (
    `id`            bigint unsigned not null auto_increment,
    `department`    varchar(32) not null default '' comment '所属部门',
    `module`        varchar(32) not null default '' comment '所属模块，比如server, web',
    `project`       varchar(32) not null default '' comment '所属项目，比如hai-api, hai-admin',
    `service_name`  varchar(32) not null default '' comment '服务名字',
    `api_name`      varchar(32) not null default '' comment '接口名字',
    `author`        varchar(32) not null default '' comment '作者',
    `is_dpdn_call`  tinyint(1) not null default 0 comment '是否依赖接口调用',
    `not_run`       varchar(4) not null default '' comment '不执行该case',
    `description`   varchar(128) not null default '' comment 'case描述',
    `method`        varchar(16) not null default '' comment '请求方法比如post, get',
    `protocol`      varchar(16) not null default '' comment '请求协议，比如http, https, websocket',
    `url`           varchar(128) not null default '' comment '接口路径',
    `headers`       varchar(256) not null default '' comment '请求头信息',
    `apikey`        varchar(16) not null default '' comment '用于生成头信息里的X-Gd-Sign鉴权',
    `xgd_param`     varchar(128) not null default '' comment '用于生成头信息里base64编码的X-Gd-Param',
    `input_file`    varchar(64) not null default '' comment '指定测试输入文件名',
    `param`         varchar(500) not null default '' comment 'post请求的body参数',
    `init_mysql_bc` varchar(1000) not null default '' comment 'case前置sql执行语句',
    `contains_str`  varchar(128) not null default '' comment '校验包含字符串',
    `rep_status`    varchar(16) not null default '' comment '校验请求返回状态码',
    `verify`        varchar(1000) not null default '' comment '校验请求response指定字段',
    `mysql_verify`      varchar(1000) not null default '' comment '数据库校验',
    `recover_mysql_ac`  varchar(1000) not null default '' comment 'case后置sql执行语句',
    `save`          varchar(64) not null default '' comment '提取保存response指定字段，作为变量参数化',
    `pre_param`     varchar(64) not null default '' comment '自定义预设置变量，作为变量参数化',
    `sleep`         varchar(16) not null default '' comment '设置case执行前等待时间，单位秒',
    `created`       timestamp not null default CURRENT_TIMESTAMP,
    `updated`       timestamp not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    primary key  (`id`),
    key `idx_department`        (`department`),
    key `idx_module`            (`module`),
    key `idx_service_name`      (`service_name`),
    key `idx_api_name`          (`api_name`),
    key `idx_author`            (`author`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;