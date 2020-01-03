#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import re
import configparser
import subprocess
import time
from xml.dom import minidom

# 读取预配置信息
config = configparser.ConfigParser()
config.read('gameconfig.txt')
#服务器类型
game_server_type = int(config.get('global', 'server_type'))
#区服配置
server_config_list = config.get('server', 'serverconfig')
#平台区服信息
game_agent = config.get('global', 'agent')
game_name = config.get('global', 'gamename')
language = config.get('global', 'language')
mina_port = config.get('mina', 'minaport')
connect_port = config.get('innerserver', 'connectport')
connect_ip = config.get('innerserver', 'connectip')

server_client_id = config.get('innerclient', 'serverid')
server_client_ip = config.get('innerclient', 'serverip')
server_client_port = config.get('innerclient', 'serverport')
server_client_type = config.get('innerclient', 'servertype')

http_server_port = config.get('httpserver', 'serverport')

#游戏服数据库配置
game_dbip = config.get('mysqlconfig', 'dbip')
game_dbuser = config.get('mysqlconfig', 'dbuser')
game_dbpass = config.get('mysqlconfig', 'dbpass')
game_dbport = config.get('mysqlconfig', 'dbport')
game_data_name = config.get('mysqlconfig', 'dataname')
game_db_name = config.get('mysqlconfig', 'dbname')
game_db_back_name = config.get('mysqlconfig', 'dbbackname')
game_db_all_name = config.get('mysqlconfig', 'dballname')
game_db_global_name = config.get('mysqlconfig', 'dbglobalname')
game_db_log_name = config.get('mysqlconfig', 'logname')
#public数据库配置
public_db_name = config.get('public', 'dbname')
public_data_name = config.get('public', 'dataname')
#开服时间
game_openservertime = config.get('global', 'openservertime')
timeArray = time.strptime(game_openservertime, "%Y-%m-%d %H:%M:%S")
new_openservertime = time.strftime("%Y-%m-%d 00:00:00", timeArray)

# 定义需要修改的配置文件
configDir = "./config/"
#游戏战斗服务器配置
server_config_file = configDir+'server-config.xml'
#公共服务器配置
public_server_config_file = configDir+'public-server-config.xml'
#mina配置
mina_server_config_file = configDir+'mina-server-config.xml'
#日志配置
server_log_config_file = configDir+'server-log-config.xml'
log_db_config_file = configDir+'dbconfig/log-db-config1.properties'
#inner-server-config
inner_server_config_file = configDir+'inner-server-config.xml'
inner_client_config_file = configDir+'inner-client-config.xml'
#后台连接端口
http_server_config_file = configDir+'http-server-config.xml'
#语言配置
language_config_file = configDir+'languageres/language-config.properties'

#数据库配置
#data
db_config_file = {configDir + 'data-config.xml': game_data_name,
                    configDir + 'dbconfig/db-backup-config.xml':game_db_back_name,
                    configDir + 'dbconfig/db-global-config.xml':game_db_global_name,
                    configDir + 'dbconfig/db-all-config.xml':game_db_all_name,
                    configDir + 'dbconfig/db-config.xml': game_db_name}

public_db_config_file = {configDir + 'data-config.xml': public_data_name,
                    configDir + 'db-config.xml': public_db_name}

#创建server-config.xml
def create_server_config(filename):
    doc = minidom.Document()
    servers = doc.createElement('servers')
    doc.appendChild(servers)
    print(eval(server_config_list))
    for server_config in eval(server_config_list):
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
        server_web_text = doc.createTextNode(str(temp_config.get("server-web",game_agent)))
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
        tempStr = ''
        if game_server_type != 2:
            tempStr ='s1.'
        server_url_text = doc.createTextNode(str(temp_config.get("server-url", tempStr)))
        server_url.appendChild(server_url_text)
        server.appendChild(server_url)
        #服务器类型
        server_type = doc.createElement('server-type')
        server_type_text = doc.createTextNode(str(temp_config.get("server-type", "1")))
        server_type.appendChild(server_type_text)
        server.appendChild(server_type)
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
        server_open_text = doc.createTextNode(temp_config.get("server-open",game_openservertime))
        server_open.appendChild(server_open_text)
        server.appendChild(server_open)
        #server-list
        server_list = doc.createElement('server-list')
        server_list_text = doc.createTextNode(temp_config.get("server-list", str(game_agent+':'+str(temp_config.get("server-id",1)))))
        server_list.appendChild(server_list_text)
        server.appendChild(server_list)
    #xml 代码美容
    xmlStr = doc.toprettyxml(encoding="utf-8")
    # repl = lambda x: ">%s</" % x.group(1).strip() if len(
    #     x.group(1).strip()) != 0 else x.group(0)
    # prettrStr = re.sub(r'>\n\s*([^<]+)</', repl, xmlStr)
    # prettrStr = prettrStr.replace("</server>", "</server>\n")
    #open(filename, 'w').write(prettrStr)
    open(filename, 'wb').write(xmlStr)

#创建public_server-config.xml
def create_public_server_config(filename):
    doc = minidom.Document()
    servers = doc.createElement('servers')
    doc.appendChild(servers)
    print(eval(server_config_list))
    for server_config in eval(server_config_list):
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
        server_web_text = doc.createTextNode(str(temp_config.get("server-web",game_agent)))
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
        # tempStr = ''
        # if game_server_type != 2:
        #     tempStr ='s1.'
        # server_url_text = doc.createTextNode(str(temp_config.get("server-url", tempStr)))
        # server_url.appendChild(server_url_text)
        server.appendChild(server_url)
        #服务器类型
        server_type = doc.createElement('server-type')
        server_type_text = doc.createTextNode(str(temp_config.get("server-type", "1")))
        server_type.appendChild(server_type_text)
        server.appendChild(server_type)
        #数据库连接地址
        # server_db = doc.createElement('server-db')
        # server_db_text = doc.createTextNode(temp_config.get("server-db", "db-config.xml"))
        # server_db.appendChild(server_db_text)
        # server.appendChild(server_db)
        # #备份库地址
        # server_dbbackup = doc.createElement('server-dbbackup')
        # server_dbbackup_text = doc.createTextNode(temp_config.get("server-dbbackup", "db-backup-config.xml"))
        # server_dbbackup.appendChild(server_dbbackup_text)
        # server.appendChild(server_dbbackup)
        #开服时间
        server_open = doc.createElement('server-open')
        server_open_text = doc.createTextNode(temp_config.get("server-open",game_openservertime))
        server_open.appendChild(server_open_text)
        server.appendChild(server_open)
        #server-list
        server_list = doc.createElement('server-list')
        server_list_text = doc.createTextNode(temp_config.get("server-list", str(game_agent+':'+str(temp_config.get("server-id",1)))))
        server_list.appendChild(server_list_text)
        server.appendChild(server_list)
    #xml 代码美容
    xmlStr = doc.toprettyxml(encoding="utf-8")
    # repl = lambda x: ">%s</" % x.group(1).strip() if len(
    #     x.group(1).strip()) != 0 else x.group(0)
    # prettrStr = re.sub(r'>\n\s*([^<]+)</', repl, xmlStr)
    # prettrStr = prettrStr.replace("</server>", "</server>\n")
    #open(filename, 'w').write(prettrStr)
    open(filename, 'wb').write(xmlStr)

#更改mina配置
def modify_mina_server_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    connect_server = root.getElementsByTagName('server')
    for item in connect_server[0].childNodes:
        if item.nodeName == 'server-mina-port':
            item.childNodes[0].data = mina_port
        elif item.nodeName == 'server-mina-ssl-port':
            item.childNodes[0].data = int(mina_port)+1
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="utf-8"))
    file.close()

#更改inner-server-config
def modify_inner_server_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    for item in root.childNodes:
        if item.nodeName == 'server-connect-ip':
            item.childNodes[0].data = connect_ip
        elif item.nodeName == 'server-connect-port':
            item.childNodes[0].data = connect_port
        elif item.nodeName == 'server-port':
            item.childNodes[0].data = connect_port
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="utf-8"))
    file.close()

#更改inner_client_config
def modify_inner_client_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    connect_server = root.getElementsByTagName('connect-server')
    for item in connect_server[0].childNodes:
        if item.nodeName == 'server-id':
            item.childNodes[0].data = server_client_id
        elif item.nodeName == 'server-ip':
            item.childNodes[0].data = server_client_ip
        elif item.nodeName == 'server-port':
            item.childNodes[0].data = server_client_port
        elif item.nodeName == 'server-type':
            item.childNodes[0].data = server_client_type
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="utf-8"))
    file.close()

#更改http-server-config.xml
def modify_http_server_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    connect_server = root.getElementsByTagName('server')
    for item in connect_server[0].childNodes:
        if item.nodeName == 'server-port':
            item.childNodes[0].data = http_server_port
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="utf-8"))
    file.close()

#更改语言
def modify_languager(filename):
    sub = 'language='+language
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
                if db == game_db_all_name:
                    node.setAttribute('value', 'jdbc:mysql://' + game_dbip +":" + str(game_dbport) + '/' + db)
                else:
                    node.setAttribute('value', 'jdbc:mysql://' + game_dbip + ":" + str(game_dbport) + '/' + db + '?autoReconnect=true')
                # node.setAttribute('value', 'jdbc:mysql://' + game_dbip +
                #                   ":" + str(game_dbport) + '/' + db + '?autoReconnect=true')
            elif node.getAttribute('name') == 'username' or node.getAttribute('name') == "user":
                node.setAttribute('value', game_dbuser)
            elif node.getAttribute('name') == 'password':
                node.setAttribute('value', game_dbpass)
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="utf-8"))
    file.close()

#更改public_inner-server-config
def modify_public_inner_server_config(filename):
    doc = minidom.parse(filename)
    root = doc.documentElement
    for item in root.childNodes:
        if item.nodeName == 'server-port':
            item.childNodes[0].data = server_client_port
    file = open(filename, 'wb')
    file.write(doc.toxml(encoding="utf-8"))
    file.close()

#更改server-log-config.xml
def create_server_log_config(filename):
    doc = minidom.Document()
    servers = doc.createElement('servers')
    doc.appendChild(servers)
    print(eval(server_config_list))
    for server_config in eval(server_config_list):
        server = doc.createElement('server')
        servers.appendChild(server)
        temp_config = dict(server_config)
        # 服务器id
        server_id = doc.createElement('server-id')
        server_id_text = doc.createTextNode(str(temp_config.get("server-id", "1")))
        server_id.appendChild(server_id_text)
        server.appendChild(server_id)
        # 服务器平台ID
        server_web_id = doc.createElement('server-web-id')
        server_web_id_text = doc.createTextNode(str(temp_config.get("server-web-id", "1")))
        server_web_id.appendChild(server_web_id_text)
        server.appendChild(server_web_id)
        # 国家
        server_log_db = doc.createElement('server-log-db')
        server_log_db_text = doc.createTextNode(str(temp_config.get("server-log-db", "log-db-config1.properties")))
        server_log_db.appendChild(server_log_db_text)
        server.appendChild(server_log_db)
    # xml 代码美容
    xmlStr = doc.toprettyxml(encoding="utf-8")
    # repl = lambda x: ">%s</" % x.group(1).strip() if len(
    #     x.group(1).strip()) != 0 else x.group(0)
    # prettrStr = re.sub(r'>\n\s*([^<]+)</', repl, xmlStr)
    # prettrStr = prettrStr.replace("</server>", "</server>\n")
    # open(filename, 'w').write(prettrStr)
    open(filename, 'wb').write(xmlStr)

#更改 log_db_config1.properties
def modify_log_db_config(filename):
    file = open(filename)
    lines = file.read()
    sub = re.sub('jdbc:mysql:.*', 'jdbc:mysql://' + game_dbip + ':' +
                 str(game_dbport) + '/' + game_db_log_name + '?autoReconnect=true', lines)
    sub = re.sub('user=.*', 'user=' + game_dbuser, sub)
    sub = re.sub('password=.*', 'password=' + game_dbpass, sub)
    file.close()
    file = open(filename, 'w')
    file.write(sub)
    file.close()

def test():
    for file, dbname in db_config_file.items():
        modify_dbinfo(file, dbname)
    modify_log_db_config(log_db_config_file)

def server():
    # 更改数据库连接
    # for file, dbname in db_config_file.iteritems():
    for file, dbname in db_config_file.items():
        modify_dbinfo(file, dbname)
    # 更新服务器配置
    create_server_config(server_config_file)
    # 更改服务器日志配置
    create_server_log_config(server_log_config_file)
    modify_log_db_config(log_db_config_file)
    # 更改mina配置
    modify_mina_server_config(mina_server_config_file)
    # 更改inner-server-config
    modify_inner_server_config(inner_server_config_file)
    # 更改inner_client_config
    modify_inner_client_config(inner_client_config_file)
    # 更改http-server-config.xml
    modify_http_server_config(http_server_config_file)

def public():
    for file, dbname in public_db_config_file.items():
        modify_dbinfo(file, dbname)
    # 更新服务器配置
    create_public_server_config(public_server_config_file)
    # 更改连接public端口
    modify_public_inner_server_config(inner_server_config_file)
    # 更改http-server-config.xml
    modify_http_server_config(http_server_config_file)

def main():
    # print("开始更新配置文件")
    if game_server_type == 2:
        public()
    else:
        server()
    # 更改语言
    modify_languager(language_config_file)

if __name__ == '__main__':
    main()
    # test()
