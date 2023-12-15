-- auto-generated definition
create schema chat collate utf8mb4_0900_ai_ci;

use chat;

create table chat.conversation
(
    id         bigint auto_increment comment 'id'
        primary key,
    userId     bigint                             not null comment '创建人',
    title      varchar(256)                       not null comment '会话标题',
    createTime datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    updateTime datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    isDelete   tinyint  default 0                 not null comment '是否删除(0-未删,1-已删)'
)
    engine = InnoDB;

create table chat.message
(
    id             bigint auto_increment comment 'id'
        primary key,
    conversationId bigint                             not null comment '会话Id',
    content        text                               not null comment '消息内容',
    userId         bigint                             not null comment '创建人',
    createTime     datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    updateTime     datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    isDelete       tinyint  default 0                 not null comment '是否删除(0-未删,1-已删)'
)
    engine = InnoDB;

create table chat.user
(
    id           bigint auto_increment comment 'id'
        primary key,
    userAccount  varchar(256)                           not null comment '账号',
    userPassword varchar(512)                           not null comment '密码',
    userName     varchar(256)                           null comment '用户昵称',
    userAvatar   varchar(1024)                          null comment '用户头像',
    userProfile  varchar(512)                           null comment '用户简介',
    userRole     varchar(256) default 'user'            not null comment '用户角色：user/admin/ban',
    createTime   datetime     default CURRENT_TIMESTAMP not null comment '创建时间',
    updateTime   datetime     default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    isDelete     tinyint      default 0                 not null comment '是否删除'
)
    comment '用户' engine = InnoDB
                 collate = utf8mb4_unicode_ci;

