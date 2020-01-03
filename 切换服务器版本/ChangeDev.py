#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import re
import configparser
import subprocess
import time
from xml.dom import minidom

name = input("输入切换的版本(配置文件后缀 37,tw):")
# 读取预配置信息
config = configparser.ConfigParser()
# 读取预配置信息
configname = 'ConfigData_'+name+'.txt'
config.read(configname)
globalStr = 'global'
#目录
dirStr = config.get(globalStr, 'dirStr')
#开服时间
opentime = config.get(globalStr, 'opentime')
#平台
agent = config.get(globalStr, 'agent')
#语言
language = config.get(globalStr, 'language')
Game_Logic = config.get(globalStr, 'Game_Logic')
Game_Public = config.get(globalStr, 'Game_Public')
LogicDir = dirStr + '/' +Game_Logic +'/config/'
PublicDir = dirStr + '/' +Game_Public +'/config/'
gamename = config.get(globalStr, 'gamename')

#数据库配置
mysqlStr = 'mysql'
dbip = config.get(mysqlStr, 'dbip')
dbuser = config.get(mysqlStr, 'dbuser')
dbpass = config.get(mysqlStr, 'dbpass')
dbport = config.get(mysqlStr, 'dbport')
dbname = config.get(mysqlStr, 'dbname')
pdbname = config.get(mysqlStr, 'pdbname')
dataname = config.get(mysqlStr, 'dataname')
dbbackname = config.get(mysqlStr, 'dbbackname')
dballname = config.get(mysqlStr, 'dballname')
dbglobalname = config.get(mysqlStr, 'dbglobalname')
logname = config.get(mysqlStr, 'logname')

httpserverStr = 'httpserver'
httpserver_port = config.get(httpserverStr, 'serverport')

innerclientStr = 'innerclient'
innerclient_serverid = config.get(innerclientStr, 'serverid')
innerclient_serverip = config.get(innerclientStr, 'serverip')
innerclient_serverport = config.get(innerclientStr, 'serverport')
innerclient_servertype = config.get(innerclientStr, 'servertype')

innerserverStr = 'innerserver'
innerserver_connectport = config.get(innerserverStr, 'connectport')
innerserver_connectip = config.get(innerserverStr, 'connectip')

minaserverStr = 'minaserver'
minaserver_minaport = config.get(minaserverStr, 'minaport')

serverStr = 'server'
sconfig = config.get(serverStr, 'sconfig')
pconfig = config.get(serverStr, 'pconfig')
fconfig = config.get(serverStr, 'fconfig')

# 日志
log_config_file = LogicDir+'dbconfig/log-db-config1.properties'

# 数据库
db_config_files = {LogicDir + 'data-config.xml': dataname,
                    LogicDir + 'dbconfig/db-backup-config.xml':dbbackname,
                    LogicDir + 'dbconfig/db-global-config.xml':dbglobalname,
                    LogicDir + 'dbconfig/db-all-config.xml':dballname,
                    LogicDir + 'dbconfig/db-config.xml': dbname,
                    PublicDir + 'data-config.xml': dataname,
                    PublicDir + 'db-config.xml': pdbname
                  }
# 后台监听端口
http_server_config_files = {LogicDir + 'http-server-config.xml': httpserver_port,
                    LogicDir + 'http-server-config-public.xml': int(httpserver_port) + 2,
                    PublicDir + 'http-server-config.xml': int(httpserver_port) + 1
}

# 登录端口
mina_config_files = {LogicDir + 'mina-server-config.xml': minaserver_minaport,
                    LogicDir + 'mina-server-config-public.xml':int(minaserver_minaport) + 10000
}

# 服务器配置
server_config_files = {LogicDir + 'server-config.xml': sconfig,
                    LogicDir + 'server-config-public.xml':fconfig,
                    PublicDir + 'public-server-config.xml': pconfig
}



#更改语言
def modify_languager(filename):
    sub = 'language='+language
    file = open(filename, 'w')
    file.write(sub)
    file.close()

#更改日志配置
def modify_log_config(filename):
    file = open(filename)
    lines = file.read()
    sub = re.sub('jdbc:mysql:.*', 'jdbc:mysql://' + dbip + ':' +
                 str(dbport) + '/' + logname + '?autoReconnect=true', lines)
    sub = re.sub('user=.*', 'user=' + dbuser, sub)
    sub = re.sub('password=.*', 'password=' + dbpass, sub)
    file.close()
    file = open(filename, 'w')
    file.write(sub)
    file.close()

#更改数据库连接
def modify_dbinfo(filename, db):
    doc = minidom.parse(filename)
    root = doc.documentElement
    dataSource = root.getElementsByTagName('dataSource')
    for item in dataSource:
        for node in item.getElementsByTagName('property'):
            if node.getAttribute('name') == 'url' or node.getAttribute('name') == "jdbcUrl":
                if db == dballname:
                    node.setAttribute('value', 'jdbc:mysql://' + dbip +":" + str(dbport) + '/' + db)
                else:
                    node.setAttribute('value', 'jdbc:mysql://' + dbip + ":" + str(dbport) + '/' + db + '?autoReconnect=true')
            elif node.getAttribute('name') == 'username' or node.getAttribute('name') == "user":
                node.setAttribute('value', dbuser)
            elif node.getAttribute('name') == 'password':
                node.setAttribute('value', dbpass)
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="UTF-8"))
    file.close()

#更改http-server-config.xml
def modify_http_server_config(filename,port):
    doc = minidom.parse(filename)
    root = doc.documentElement
    connect_server = root.getElementsByTagName('server')
    for item in connect_server[0].childNodes:
        if item.nodeName == 'server-port':
            item.childNodes[0].data = port
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="UTF-8"))
    file.close()

#更改inner_client_config
def modify_inner_client_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    connect_server = root.getElementsByTagName('connect-server')
    for item in connect_server[0].childNodes:
        if item.nodeName == 'server-id':
            item.childNodes[0].data = innerclient_serverid
        elif item.nodeName == 'server-ip':
            item.childNodes[0].data = innerclient_serverip
        elif item.nodeName == 'server-port':
            item.childNodes[0].data = innerclient_serverport
        elif item.nodeName == 'server-type':
            item.childNodes[0].data = innerclient_servertype
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="UTF-8"))
    file.close()

#更改public_inner-server-config
def modify_public_inner_server_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    for item in root.childNodes:
        if item.nodeName == 'server-port':
            item.childNodes[0].data = innerclient_serverport
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="UTF-8"))
    file.close()

#更改inner-server-config
def modify_inner_server_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    for item in root.childNodes:
        if item.nodeName == 'server-connect-ip':
            item.childNodes[0].data = innerserver_connectip
        elif item.nodeName == 'server-connect-port':
            item.childNodes[0].data = innerserver_connectport
        elif item.nodeName == 'server-port':
            item.childNodes[0].data = innerserver_connectport
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="UTF-8"))
    file.close()

#更改mina配置
def modify_mina_server_config(filename,port):
    doc = minidom.parse(filename)
    root = doc.documentElement
    connect_server = root.getElementsByTagName('server')
    for item in connect_server[0].childNodes:
        if item.nodeName == 'server-mina-port':
            item.childNodes[0].data = port
        elif item.nodeName == 'server-mina-ssl-port':
            item.childNodes[0].data = int(port)+1
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="UTF-8"))
    file.close()

#创建server-config.xml
def create_config(filename,configlist):
    doc = minidom.Document()
    servers = doc.createElement('servers')
    doc.appendChild(servers)
    isPublic = 1
    if str(filename).__contains__('public-server-config.xml'):
        isPublic = 2
    # print(eval(configlist))
    for server_config in eval(configlist):
        server = doc.createElement('server')
        servers.appendChild(server)
        temp_config = dict(server_config)
        #服务器名称
        server_name = doc.createElement('server-name')
        server_name_text = doc.createTextNode(str(temp_config.get("server-name","Game")))
        server_name.appendChild(server_name_text)
        server.appendChild(server_name)
        # 服务器id
        server_id = doc.createElement('server-id')
        server_id_text = doc.createTextNode(str(temp_config.get("server-id","1")))
        server_id.appendChild(server_id_text)
        server.appendChild(server_id)
        #服务器平台
        server_web = doc.createElement('server-web')
        server_web_text = doc.createTextNode(str(temp_config.get("server-web",agent)))
        server_web.appendChild(server_web_text)
        server.appendChild(server_web)
        #服务器平台ID
        server_web_id = doc.createElement('server-web-id')
        server_web_id_text = doc.createTextNode(str(temp_config.get("server-web-id","1")))
        server_web_id.appendChild(server_web_id_text)
        server.appendChild(server_web_id)
        #国家
        group_id = doc.createElement('group-id')
        group_id_text = doc.createTextNode(str(temp_config.get("group-id", "1")))
        group_id.appendChild(group_id_text)
        server.appendChild(group_id)
        #服务器前缀
        server_url = doc.createElement('server-url')
        tempStr = 's1.'
        server_url_text = doc.createTextNode(str(temp_config.get("server-url", tempStr)))
        server_url.appendChild(server_url_text)
        server.appendChild(server_url)
        #服务器类型
        server_type = doc.createElement('server-type')
        server_type_text = doc.createTextNode(str(temp_config.get("server-type", "1")))
        server_type.appendChild(server_type_text)
        server.appendChild(server_type)
        if isPublic == 1:
            #数据库连接地址
            server_db = doc.createElement('server-db')
            server_db_text = doc.createTextNode(temp_config.get("server-db", "db-config.xml"))
            server_db.appendChild(server_db_text)
            server.appendChild(server_db)
            #备份库地址
            server_dbbackup = doc.createElement('server-dbbackup')
            server_dbbackup_text = doc.createTextNode(temp_config.get("server-dbbackup", "db-backup-config.xml"))
            server_dbbackup.appendChild(server_dbbackup_text)
            server.appendChild(server_dbbackup)
        #开服时间
        server_open = doc.createElement('server-open')
        server_open_text = doc.createTextNode(temp_config.get("server-open",opentime))
        server_open.appendChild(server_open_text)
        server.appendChild(server_open)
        #server-list
        server_list = doc.createElement('server-list')
        server_list_text = doc.createTextNode(temp_config.get("server-list", str(agent+':'+str(temp_config.get("server-id",1)))))
        server_list.appendChild(server_list_text)
        server.appendChild(server_list)
    #xml 代码美容
    xmlStr = doc.toprettyxml(encoding="UTF-8")
    # repl = lambda x: ">%s</" % x.group(1).strip() if len(
    #     x.group(1).strip()) != 0 else x.group(0)

    # prettrStr = re.sub(r'>\n\s*([^<]+)</', repl, xmlStr)
    # prettrStr = prettrStr.replace("</server>", "</server>\n")
    # open(filename, 'w').write(prettrStr)
    open(filename, 'wb').write(xmlStr)

def main():
    # 更改语言
    modify_languager(LogicDir + 'languageres/language-config.properties')
    modify_languager(PublicDir+'languageres/language-config.properties')
    # 更改游戏服日志配置
    modify_log_config(log_config_file)
    # 更改数据库链接
    for file, dbname in db_config_files.items():
        modify_dbinfo(file, dbname)
    # 更改后台配置
    for file, port in http_server_config_files.items():
        modify_http_server_config(file, port)
    # 链接公共服配置
    modify_inner_client_config(LogicDir + 'inner-client-config.xml')
    # 战斗服监听端口
    modify_inner_server_config(LogicDir + 'inner-server-config.xml')
    # 公共服监听端口
    modify_public_inner_server_config(PublicDir + 'inner-server-config.xml')
    # 游戏登录端口
    for file, port in mina_config_files.items():
        modify_mina_server_config(file, port)
    # 区服配置
    for file, configlist in server_config_files.items():
        create_config(file, configlist)

if __name__ == '__main__':
    main()
    input("完成！！！！")





