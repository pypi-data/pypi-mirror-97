# _*_coding:utf-8_*_
# Author_name : by zcl
# Emial: zclmbf597854439@gmial.com
# Created at: 2020/4/16
import hashlib
import time
import oss2
import json
import re
import os
import csv
import random
import xlrd
import datetime
import chardet
import redis
import execjs
import arrow
import math
import pymysql
import pytesseract
import requests
import numpy as np
import jieba.posseg as pseg
import threading
from tqdm import tqdm
from os import listdir
from scrapy import Selector
from PIL import Image
from io import BytesIO
from selenium import webdriver
from multiprocessing import Pool, Process, Queue
from DBUtils.PooledDB import PooledDB
from multiprocessing.dummy import Pool as ThreadPool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# sudo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple           linux
# pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple                             windows

# 红色输出



def red_print(str):
    print('\033[31m{}\033[0m'.format(str))


class Auto_sinsert():
    def __init__(self, host='127.0.0.1', username='root', password='mysql', db='test',
                 drop_column=["id", "updated"], pool_db=False, pool_num=10):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.pool_db = pool_db
        self.drop_column = drop_column  # 表删除字段
        self.pool_num = pool_num
        if pool_db:
            self.sql_pool = PooledDB(pymysql, self.pool_num, host=self.host, user=self.username, passwd=self.password,
                                db=self.db,
                                port=3306,
                                charset='utf8', use_unicode=True)
            self.conn = self.sql_pool.connection()
            self.cursor = self.conn.cursor()
        else:
            self.conn = pymysql.connect(self.host, self.username, self.password, self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        self.table_name_list = self.get_db_name()
        self.column_list = self.get_columns()
        self.ping()

    def get_db_name(self):
        sql = "select table_name from information_schema.tables where table_schema='{}'".format(self.db)
        self.cursor.execute(sql)
        db_list = self.cursor.fetchall()
        db_list = [i[0] for i in db_list]
        return db_list

    def get_columns(self):
        item = {}
        for table_name in self.table_name_list:
            sql = "select column_name from information_schema.columns where table_name=%r and table_schema=%r" % (
                table_name, self.db)
            self.cursor.execute(sql)
            column_list = self.cursor.fetchall()
            column_list = [i[0] for i in column_list]
            insert_columns = [i for i in column_list if i not in self.drop_column]
            item[table_name] = insert_columns
        return item

    def ping(self):
        n = 0
        while True:
            try:
                if self.pool_db:
                    sql_conn = self.sql_pool.connection()
                    cursor = sql_conn.cursor()
                else:
                    sql_conn = pymysql.connect(self.host, self.username, self.password, self.db, charset='utf8')
                    cursor = sql_conn.cursor()
                return sql_conn,cursor
            except Exception as e:
                n += 1
                if n > 5:
                    print("数据库连接已断开: {} 正在尝试第 {} 次重新连接".format(self.host,n))
                    return None,None
                print("数据库连接已断开: {} 正在重新连接".format(self.host))
                try:
                    if self.pool_db:
                        self.sql_pool = PooledDB(pymysql, self.pool_num, host=self.host, user=self.username,
                                                 passwd=self.password,
                                                 db=self.db,
                                                 port=3306,
                                                 charset='utf8', use_unicode=True)
                        sql_conn = self.sql_pool.connection()
                        cursor = sql_conn.cursor()
                    else:
                        sql_conn = pymysql.connect(self.host, self.username, self.password, self.db, charset='utf8')
                        cursor = sql_conn.cursor()
                    return sql_conn, cursor
                except:
                    print("5S重试连接", e)
                    time.sleep(5)

    def insert_data(self, item, table_name):
        sql_conn, cursor = self.ping()
        if item and sql_conn and cursor:
            item_key = self.column_list.get(table_name)
            if item_key:
                item_values = [item.get(i) for i in item_key]
                sss = ''
                for i in range(len(item_key)):
                    sss += '%s,'
                insert = 'insert ignore into {}('.format(table_name) + ','.join(item_key) + ')' + 'values({})'.format(
                    sss[:-1])
                data = '(' + ','.join([pymysql.escape_string('%r') % str(i) for i in item_values]) + ')'
                data_list = []
                for i in eval(data):
                    if i == 'None':
                        i = None
                    data_list.append(i)
                data = tuple(data_list)
                cursor.execute(insert, data)
                sql_conn.commit()
                print("****************   {} 表  insert data success   ****************".format(table_name))
            else:
                raise ValueError("没有{}表".format(table_name))
        else:
            if not cursor and not sql_conn:
                with open('error_insert_data.txt','a',encoding='utf8')as f:
                    f.write(json.dumps(item,ensure_ascii=False)+'\n')
                print("数据库连接异常，未插入数据字段保存在 error_insert_data.txt")
            else:
                print("item is None")
        cursor.close()
        sql_conn.close()


# 使用说明:
# item = {'key':'none'}
# # drop_column 为所有表中不插入的字段
# auto_sinsert = Auto_sinsert(host='192.168.4.201',username='root',password='mysql',db='zhijianju',drop_column=["id","jid","update","entid"])
# auto_sinsert.insert_data(item,'aqsiq_biaozhun_basic')


class Auto_indb():
    def __init__(self,host='', username='', password='', db='', comment='', create_tables=True):
        print('''auto_indb = Auto_indb(host='192.168.4.201',username='root',password='mysql',db="storm",table_name='',comment='表注释',create_tables=True)''')
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.comment = comment  # 表注释
        self.create_tables = create_tables  # 是否创建表
        try:
            self.sql_pool = PooledDB(pymysql, 10, host=self.host, user=self.username, passwd=self.password,
                                db=self.db, port=3306,
                                charset='utf8', use_unicode=True)
            print(f"连接数据库 db={db} 成功")
        except:
            raise (f'连接数据库 db={db} 失败')
        self.table_name_dict = {}


    def table_exists(self,table_name,cursor):
        hassql = ' show tables where Tables_in_%s ="%s"' % (self.db, table_name)
        has = cursor.execute(hassql)
        if has:
            print("该{}表已经存在".format(table_name))
            return True
        else:
            return False

    def create_table(self,table_name,cursor,conn):
        newtab = '''
                   CREATE TABLE `%s` (
                   	`id` INT(11) NOT NULL AUTO_INCREMENT primary key ,
                   	`updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
                   )
                   COMMENT='%s'
                   ENGINE=INNODB;
                   ''' % (table_name, self.comment)
        cursor.execute(newtab)
        conn.commit()
        print("创建{}表成功".format(table_name))

    def get_columns(self,table_name,cursor):
        result = []
        sql = "select COLUMN_NAME from information_schema.columns where table_schema='%s' and table_name='%s'" % (self.db,table_name)
        cursor.execute(sql)
        for res in cursor.fetchall():
            res = res[0]
            result.append(res.lower())
        return result

    def insert_data(self, items,table_name):
        if 'ID' in items.keys():
            items['idindex'] = items['ID']
            del items['ID']
        conn = self.sql_pool.connection()
        cursor = conn.cursor()
        if table_name not in self.table_name_dict.keys() and not self.table_exists(table_name,cursor):
            self.create_table(table_name,cursor,conn)
        if table_name not in self.table_name_dict.keys():
            column_list = self.get_columns(table_name,cursor)
            self.table_name_dict[table_name] = column_list
        keys = ''
        vals = []
        s = ''
        for item in items.keys():
            if item.lower() not in self.get_columns(table_name,cursor):
                if item == 'eid':
                    sql = 'alter table %s add %s int' % (table_name, item)
                else:
                    sql = 'alter table %s add %s VARCHAR(200) DEFAULT NULL' % (table_name, item)
                cursor.execute(sql)
                conn.commit()
                self.table_name_dict[table_name].append(item)
            if item:
                keys += item + ','
                s += '%s,'
                vals.append(items.get(item))
        keys = keys[:-1]
        indbsrt = 'insert ignore into {}({}) VALUES ({})' .format(table_name, keys,s[:-1])
        cursor.execute(indbsrt,vals)
        conn.commit()
        cursor.close()
        conn.close()
        print("**************************  insert {} table success  **********************".format(table_name))

has_item = True
class Task_Allocation():
    def __init__(self,redis_db,mysql_db,new_company_task):
        redis_pool = redis.ConnectionPool(host=redis_db['host'], port=redis_db['port'], password=redis_db['password'],
                                          db=redis_db.get('db', 0))
        self.redis_conn = redis.StrictRedis(connection_pool=redis_pool)
        self.sql_pool = PooledDB(pymysql, mysql_db['pool_num'], host=mysql_db['host'], user=mysql_db['user'], passwd=mysql_db['passwd'], db=mysql_db['db'], port=3306,
                            charset='utf8', use_unicode=True)
        self.new_company_task = new_company_task

    def push_tasks(self,mode='master',query_cloumn=('id','entname')):
        global has_item
        has_item = True
        old_tasks_num = self.redis_conn.llen(f'{self.new_company_task}_items')
        if mode == 'slave':
            return old_tasks_num
        sql_conn = self.sql_pool.connection()
        cursor = sql_conn.cursor()
        cursor.execute(
            f"select {','.join(query_cloumn)} from {self.new_company_task} WHERE label =9 limit 10000")
        sql_conn.commit()
        result = cursor.fetchall()
        self.redis_conn.delete(f'{self.new_company_task}_items')
        for i in result:
            items = {}
            for index,key in enumerate(query_cloumn):
                items[key] = i[index]
            self.redis_conn.rpush(f'{self.new_company_task}_items', json.dumps(items, ensure_ascii=False))
        sql_conn.close()
        print('查询成功，共%s条' % len(result))
        return len(result)

    def get_select_item(self):
        result = self.redis_conn.lpop(f'{self.new_company_task}_items')
        if result:
            params = json.loads(result.decode())
            return params
        else:
            print('任务完成')
            global has_item
            has_item = False
            return None

class UPLOAD_FILE():
    def __init__(self,subfilename,key="",password="",net_address="",db=""):
        auth = oss2.Auth(key,password)
        self.bucket = oss2.Bucket(auth, net_address, db)
        self.subfilename = subfilename  +'/'+ datetime.datetime.now().strftime("%Y%m/") + '{}'.format(datetime.datetime.now().day)# oss 路径# oss 路径
        print(self.subfilename)

    def upload_file(self,path_list=None,path=None,type='content',content_file=None,content_name=None):
        if path_list:
            list_file = os.listdir(path_list)
            for file in list_file:
                local_file = path_list + "\\" + "{}".format(file)
                osspath = self.subfilename + '/' + file
                print(osspath)
                self.up_file(osspath, local_file)
        elif path:
            osspath = self.subfilename + '/' +path.split('/')[-1]
            local_file = path
            self.up_file(osspath,local_file)
            return osspath
        elif type=='content':
            osspath = self.subfilename + '/' + content_name
            exist = self.bucket.object_exists(osspath)
            if exist:
                print("oss have files with the same name, ignore oss upload")
                return osspath
            else:
                self.bucket.put_object(osspath, content_file)
                print(" {} 上传成功".format(osspath))
                return osspath
        else:
            print("未指定路径")

    def up_file(self,osspath,local_file):
        # 先检测oss上是否有该文件
        exist = self.bucket.object_exists(osspath)
        if exist:
            print("oss have files with the same name, ignore oss upload")
        else:
            # 上传文件
            with open(local_file, "rb") as fileobj:
                result1 = self.bucket.put_object(osspath, fileobj)
                print("{} 上传成功".format(osspath))
            if int(result1.status) != 200:
                print("oss upload faild %s" % osspath)


# ID增量更新，查询最大ID
class query_db():
    table_name = 'dataplus_b2b_update'

    def __init__(self):
        self.conn = pymysql.connect(host='192.168.4.205', port=3306, user='root', passwd='mysql', db='storm',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        print("连接数据库成功")

    def query_max_id(self, b2b_name):
        sql = 'select url from {}'.format('max_url') + ' where b2b=%r' % b2b_name
        print("正在查询max_url表中{}url最大ID。。。".format(b2b_name))
        self.cursor.execute(sql)
        urls = self.cursor.fetchall()
        id_list = []
        for url in urls:
            id_l = re.findall('\d+', str(url), re.S)
            for i in id_l:
                id_list.append(int(i))
                id_list.append(1)
                id_list.append(1)

        if id_list:
            key = max(id_list, key=id_list.count)
            id_list = set(id_list)
            id_list.remove(key)
            max_id = max(id_list)
            print(max_id)
            return max_id

        else:
            print("没有查询到最大id")
            return 1000000

    def insert_max_data(self, item, b2b_name):
        url = item.get('url')
        if url:
            insert_into = '''insert into max_url(url,b2b) values ('%s','%s') ''' % (url, b2b_name)
            self.cursor.execute(insert_into)
            self.conn.commit()
            print("存入{}最大id成功".format(b2b_name))
        else:
            print("木有发现最大url,无法存入")


# 执行sql语句
class Execute_sql():
    def __init__(self, host='', username='', password='', db=''):
        red_print("--------------------------------------------------------------------------------------------")
        print('''execute_sql = t.Execute_sql(host='192.168.4.201',username='root',password='mysql',db='zhijianju')''')
        red_print("--------------------------------------------------------------------------------------------")
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        try:
            self.conn = pymysql.connect(self.host, self.username, self.password, self.db, charset='utf8')
            self.cursor = self.conn.cursor()
            self.conn.commit()
            print("连接数据库 db={} 成功".format(db))
        except:
            raise ValueError('连接数据库 db={} 失败'.format(db))

    def select_sql(self, cloumns='*', table_name='', limit='10'):
        sql = 'select {} from {} limit {}'.format(cloumns, table_name, limit)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def get_scrapy_filed(self, table_name,custom="get_column(response,'')"):
        sql = '''
        select column_name,column_comment from information_schema.columns where table_name='{}' and table_schema='{}'
        '''.format(table_name, self.db)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            red_print('----------------------------------------------------------')
            for item in result:
                item = '{} = scrapy.Field() #{}'.format(item[0], item[1])
                print(item)
            red_print('----------------------------------------------------------')
            for item in result:
                item = "item['{}'] = {} #{}".format(item[0],custom,item[1])
                print(item)
            red_print('----------------------------------------------------------')
            os._exit(0)

        else:
            red_print('no result')
            return None

    def custom(self, sql, state='commit'):
        self.cursor.execute(sql)
        if state == 'commit':
            self.conn.commit()
        elif state == 'fetchall':
            result = self.cursor.fetchall()
            if result:
                return result
            else:
                red_print('no result')
                return None
        else:
            red_print("no practice way,please appoint commit or fetchall")


# execute_sql = Execute_sql(host='192.168.4.201',username='root',password='mysql',db='zhijianju')

class Debug_code():
    def __init__(self, url):
        self.url = url

    def get(self, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
            xpath=''):
        res = requests.get(url=self.url, headers=headers, timeout=5)
        try:
            text = res.json()
            print(text)
            result = get_column(text, xpath)
            print(result)
        except:
            text = res.text
            print(text)
            result = get_column(text, xpath)
            print(result)

    def post(self, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
             data={}, xpath=''):
        res = requests.post(url=self.url, headers=headers, data=data, timeout=5)
        try:
            text = res.json()
            print(text)
            result = get_column(text, xpath)
            print(result)
        except:
            text = res.text
            print(text)
            result = get_column(text, xpath)
            print(result)


class Redis_handle():
    def __init__(self, host='127.0.0.1', password='', db='1', decode_responses=True):
        self.db = db
        self.r = redis.Redis(host=host, port=6379, password=password, db=db, decode_responses=decode_responses)
        red_print("链接redis db= {} 成功".format(db))

    def push_queue(self, value):
        self.r.rpush(self.db, value)

    def get_out(self,exit=True):
        if self.r.llen(self.db) == 0:
            if exit:
                red_print("redis队列值为空,程序退出")
                os._exit(0)
            else:
                red_print("redis队列值为空,等待20s继续获取")
                time.sleep(20)
                return None
        else:
            get_value = self.r.lpop(self.db)
            return get_value

    def custom(self, operation):
        pass



# 自动解析  'title':  # 'description'# 'keyword'# 'content' 四个字段
class AutoHtmlParser(object):
    """智能网页文章解析类
    影响结果的参数：
        extract_title：标题仅由'_'分割，可以再添加
        extract_content：
            1. 抛弃置信度低于1000的行块（即使最大）
            2. 在上下搜索时，对于行块字符长度低于30的直接抛弃，不进行添加
        get_blocks：
            1. 当前行的正文长度不小于30才将改行设为行块起点
            2. 当前行的正文长度不小于30，且接下去两行行正文长度均小于30才将改行设为行块终点
    """

    def __init__(self):
        # re.I: 忽略大小写，re.S: '.'可以代表任意字符包括换行符
        self._title = re.compile(r'<title>(.*?)</title>', re.I | re.S)  # 匹配标题
        self._keyword = re.compile(r'<\s*meta\s*name="?Keywords"?\s+content="?(.*?)"?\s*[/]?>', re.I | re.S)  # 匹配关键词
        self._description = re.compile(r'<\s*meta\s*name="?Description"?\s+content="?(.*?)"?\s*[/]?>',
                                       re.I | re.S)  # 匹配描述
        self._link = re.compile(r'<a(.*?)>|</a>')  # 匹配<a>，</a>标签
        self._link_mark = '|ABC|'  # 标记<a>，</a>  【在extract_content中会删除改标记，所以这里修改，那也得改】
        self._space = re.compile(r'\s+')  # 匹配所有空白字符，包括\r, \n, \t, " "
        self._stopword = re.compile(
            r'备\d+号|Copyright\s*©|版权所有|all rights reserved|广告|推广|回复|评论|关于我们|链接|About|广告|下载|href=|本网|言论|内容合作|法律法规|原创|许可证|营业执照|合作伙伴|备案',
            re.I | re.S)
        self._punc = re.compile(r',|\?|!|:|;|。|，|？|！|：|；|《|》|%|、|“|”', re.I | re.S)
        self._special_list = [(re.compile(r'&quot;', re.I | re.S), '\"'),  # 还原特殊字符
                              (re.compile(r'&amp;', re.I | re.S), '&'),
                              (re.compile(r'&lt;', re.I | re.S), '<'),
                              (re.compile(r'&gt;', re.I | re.S), '>'),
                              (re.compile(r'&nbsp;', re.I | re.S), ' '),
                              (re.compile(r'&#34;', re.I | re.S), '\"'),
                              (re.compile(r'&#38;', re.I | re.S), '&'),
                              (re.compile(r'&#60;', re.I | re.S), '<'),
                              (re.compile(r'&#62;', re.I | re.S), '>'),
                              (re.compile(r'&#160;', re.I | re.S), ' '),
                              ]

    def extract_offline(self, html):
        """离线解析html页面"""
        title = self.extract_title(html)
        description = self.extract_description(html)
        keyword = self.extract_keywords(html)
        content = self.extract_content(html, title)
        return {
            'title': title,
            'description': description,
            'keyword': keyword,
            'content': content
        }

    def extract_online(self, url):
        """在线解析html页面"""
        r = requests.get(url)
        if r.status_code == 200:
            if r.encoding == 'ISO-8859-1':
                r.encoding = chardet.detect(r.content)['encoding']  # 确定网页编码
            html = r.text
            title = self.extract_title(html)
            description = self.extract_description(html)
            keyword = self.extract_keywords(html)
            content = self.extract_content(html, title)
            return {
                'title': title,
                'description': description,
                'keyword': keyword,
                'content': content
            }
        return {}

    def extract_title(self, html):
        """解析文章标题
        :param html: 未处理tag标记的html响应页面
        :return: 字符串，如果没有找到则返回空字符串
        """
        title = self._title.search(html)
        if title:
            title = title.groups()[0]
        else:
            return ''
        # 如果标题由'_'组合而成，如"习近平告诉主要负责人改革抓什么_新闻_腾讯网"，则取字数最长的字符串作为标题
        titleArr = re.split(r'_', title)
        newTitle = titleArr[0]
        for subTitle in titleArr:
            if len(subTitle) > len(newTitle):
                newTitle = subTitle
        return newTitle

    def extract_keywords(self, html):
        """解析文章关键词
        :param html: 未处理tag标记的html响应页面
        :return: 字符串，如果没有找到则返回空字符串
        """
        keyword = self._keyword.search(html)
        if keyword:
            keyword = keyword.groups()[0]
        else:
            return ''
        # 将\n, \t, \r都转为一个空白字符
        keyword = self._space.sub(' ', keyword)
        return keyword

    def extract_description(self, html):
        """解析文章描述
        :param html: 未处理tag标记的html响应页面
        :return: 字符串，如果没有找到则返回空字符串
        """
        description = self._description.search(html)
        if description:
            keyword = description.groups()[0]
        else:
            return ''
        # 将\n, \t, \r都转为一个空白字符
        keyword = self._space.sub(' ', keyword)
        return keyword

    def extract_content(self, html, title):
        """解析正文"""
        lines = self.remove_tag(html)
        blocks = self.get_blocks(lines)
        blockScores = self.block_scores(lines, blocks, title)
        res = ""
        if len(blockScores) != 0:
            maxScore = max(blockScores)
            if maxScore > 1000:  # 置信度低于1000的抛弃
                blockIndex = blockScores.index(maxScore)
                lineStart, lineEnd = blocks[blockIndex]

                # 搜索该行块的下一块，如果出现更大的置信度则加入，否则退出
                nextIndex = blockIndex + 1
                while nextIndex < len(blocks):
                    # 如果区块字符低于30个字符，直接抛弃【这个可以根据需要改变，如果希望尽可能的捕捉所有内容可以注释改行】
                    if self.detBlockLenght(lines, blocks, nextIndex) < 30: break
                    newBlock = (lineStart, blocks[nextIndex][1])
                    score = self.block_scores(lines, [newBlock], title)[0]
                    if score > maxScore:
                        lineEnd = blocks[nextIndex][1]
                        maxScore = score
                    else:
                        break

                # 搜索该行块的上一块，如果出现更大的置信度则加入，否则退出
                lastIndex = blockIndex - 1
                while lastIndex >= 0:
                    # 如果区块字符低于30个字符，直接抛弃【这个可以根据需要改变，如果希望尽可能的捕捉所有内容可以注释改行】
                    if self.detBlockLenght(lines, blocks, nextIndex) < 30: break
                    newBlock = (blocks[lastIndex][0], lineEnd)
                    score = self.block_scores(lines, [newBlock], title)[0]
                    if score > maxScore:
                        lineEnd = blocks[nextIndex][1]
                        maxScore = score
                    else:
                        break

                res += ''.join(lines[lineStart:lineEnd])
                res = re.sub('\|ABC\|(.*?)\|ABC\|', '', res, 0, re.I | re.S)  # 去除<a>内容
        return res

    def detBlockLenght(self, lines, blocks, index):
        """检测区块中字符长度"""
        if len(blocks) <= index: return 0  # 索引越界
        lineStart, lineEnd = blocks[index]
        block = ''.join(lines[lineStart:lineEnd])
        block = re.sub('\|ABC\|(.*?)\|ABC\|', '', block, 0, re.I | re.S)  # 去除<a>内容
        return len(block)

    def get_blocks(self, lines):
        """得到所有含有正文的区块
         - 区块起始点的确定：当前行的正文长度不小于30
         - 区块终点的缺点：当前行的正文长度不小于30，且接下去两行行正文长度均小于30
        :param lines: 输入一个列表，每一项为一行
        :return: 返回一个列表，每一项为一个区块
        """
        linesLen = [len(line) for line in lines]
        totalLen = len(lines)

        blocks = []
        indexStart = 0
        while indexStart < totalLen and linesLen[indexStart] < 30: indexStart += 1
        for indexEnd in range(totalLen):
            if indexEnd > indexStart and linesLen[indexEnd] == 0 and \
                    indexEnd + 1 < totalLen and linesLen[indexEnd + 1] <= 30 and \
                    indexEnd + 2 < totalLen and linesLen[indexEnd + 2] <= 30:
                blocks.append((indexStart, indexEnd))
                indexStart = indexEnd + 3
                while indexStart < totalLen and linesLen[indexStart] <= 30: indexStart += 1
        '''
        for s, e in blocks:
            print(''.join(lines[s:e]))
        '''
        return blocks

    def block_scores(self, lines, blocks, title):
        """计算区块的置信度
         - A： 当前区块<a> 标记占区块总行数比例  （标记越多，比例越高）【0.01 - 5】
         - B： 起始位置占总行数的比例 （起始位置越前面越有可能是正文）【0 - 1】
         - C： 诸如广告，版权所有，推广等词汇数占区块总行数比例 【比较大】
         - D： 当前区块中与标题重复的字占标题的比例 【0 - 1】
         - E： 当前区块标点符号占区块总行数比例 【比较大】
         - F:  当前区块去除<a>标签后的正文占区块总行数比例 【比较大】
         - G:  当前区块中文比例 【0 - 1】
         公式： scores = G * F * B * pow(E) * （1 + D） / A / pow(C)
        :param lines: 列表，每一项为一行
        :param blocks: 列表，每一项为一个区块
        :param title: 字符串
        :return: 列表，每一项为一个区块的置信度
        """
        blockScores = []
        for indexStart, indexEnd in blocks:
            blockLinesLen = indexEnd - indexStart + 1.0
            block = ''.join(lines[indexStart:indexEnd])
            cleanBlock = block.replace(self._link_mark, '')

            linkScale = (block.count(self._link_mark) + 1.0) / blockLinesLen
            lineScale = (len(lines) - indexStart + 1.0) / (len(lines) + 1.0)
            stopScale = (len(self._stopword.findall(block)) + 1.0) / blockLinesLen
            titleMatchScale = len(set(title) & set(cleanBlock)) / (len(title) + 1.0)
            puncScale = (len(self._punc.findall(block)) + 1.0) / blockLinesLen
            textScale = (len(cleanBlock) + 1.0) / blockLinesLen
            chineseScale = len(re.findall("[\u4e00-\u9fa5]", block)) / len(block)

            score = chineseScale * textScale * lineScale * puncScale * (1.0 + titleMatchScale) / linkScale / math.pow(
                stopScale, 0.5)
            blockScores.append(score)
        ''' 输出当前最大置信度的行块
        index = blockScores.index(max(blockScores))
        start, end = blocks[index]
        print(''.join(lines[start:end]))
        print(blockScores)
        '''
        return blockScores

    def remove_tag(self, html):
        """去除html的tag标签
        :param html: 未处理tag标记的html响应页面
        :return: 返回列表，每一项为一行
        """
        for r, c in self._special_list: text = r.sub(c, html)  # 还原特殊字符
        text = re.sub(r'<script(.*?)>(.*?)</script>', '', text, 0, re.I | re.S)  # 去除javascript
        text = re.sub(r'<!--(.*?)-->', '', text, 0, re.I | re.S)  # 去除注释
        text = re.sub(r'<style(.*?)>(.*?)</style>', '', text, 0, re.I | re.S)  # 去除css
        text = re.sub(r"&.{2,6};|&#.{2,5};", '', text)  # 去除如&nbsp等特殊字符
        # text = re.sub(r"<a(.*?)>(.*?)</a>", '', text, 0, re.S)  # 去除链接标记
        text = re.sub(r'<a(.*?)>|</a>', self._link_mark, text, 0, re.I | re.S)  # 将<a>, </a>标记换为|ATAG|
        text = re.sub(r'<[^>]*?>', '', text, 0, re.I | re.S)  # 去除tag标记
        lines = text.split('\n')
        for lineIndex in range(len(lines)):  # 去除所有空白字符，包括\r, \n, \t, " "
            lines[lineIndex] = re.sub(r'\s+', '', lines[lineIndex])
        return lines


def dict_get_value(data, key):
    '''
    取字典key对应的值，没有返回''
    :param data:
    :param key:
    :return:
    '''
    if isinstance(data,dict):
        result = data.get(key)
        if result:
            return str(result)
        else:
            return ''

def Thread_Grab(func,task_list,thread_num=4):
    '''
    :param func: 多线程并发函数地址
    :param num: 抓取次数
    :return:
    '''
    Lock = threading.Lock()
    start = time.time()
    pool = ThreadPool(thread_num)
    for i in tqdm(range(len(task_list)),desc=f'执行函数：{func.__name__} 任务列表:[{str(task_list[0])+",...,"+str(task_list[-1])}]'):
        Lock.acquire()
        args = task_list.pop()
        Lock.release()
        pool.apply_async(func,args=(args,))
    pool.close()
    pool.join()
    print(f'{func.__name__} 任务: success！耗时：{time.time()-start} S')

def str2dict(headers_raw):
    if headers_raw is None:
        return None
    headers = headers_raw.splitlines()
    headers_tuples = [header.split(':', 1) for header in headers]
    result_dict = {}
    for header_item in headers_tuples:
        if not len(header_item) == 2:
            continue
        item_key = header_item[0].strip()
        item_value = header_item[1].strip()
        result_dict[item_key] = item_value
    return result_dict


# 列表分组
def list_of_groups(init_list, children_list_len):
    list_of_groups = zip(*(iter(init_list),) * children_list_len)
    end_list = [list(i) for i in list_of_groups]
    count = len(init_list) % children_list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


def get_column(response, xpath, str_add_head='', str_add_tail='', Auto_wash=True,digit_wash=False):
    if xpath:
        if isinstance(response, dict):
            return response.get(xpath)
        if isinstance(response, str):
            response = Selector(text=response)
        if isinstance(xpath, list):
            value = ''.join(xpath).replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace(
                '\t', '')
            return value
        value_list = response.xpath(xpath).getall()
        if Auto_wash:
            result = []
            for value in value_list:
                value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t',
                                                                                                               '').replace(
                    '\u3000', '')
                result.append(value)
            result_result = str_add_head + ''.join(set(result)) + str_add_tail
            if digit_wash:
                result_result = ''.join(re.findall('\d+',result_result,re.S))
                return int(result_result)
            else:
                return result_result
        else:
            return str_add_head + ''.join(set(value_list)) + str_add_tail
    else:
        return None


def get_column_div_list(response, xpath):
    if isinstance(response, str):
        response = Selector(text=response)
    value_list = response.xpath(xpath)
    return value_list


def get_column_list(response, xpath, str_add_head='', str_add_tail='', Auto_wash=True):
    if isinstance(response, str):
        response = Selector(text=response)
    value_list = response.xpath(xpath).getall()
    if Auto_wash:
        value_new_list = []
        for value in value_list:
            value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t', '')
            value_new_list.append(str_add_head + value + str_add_tail)
        return list(set(value_new_list))
    else:
        return value_list


def get_column_re_list(rule, text, str_add_head='', str_add_tail='', Auto_wash=True):
    value_list = re.findall(rule, text, re.S)
    print(value_list)
    if Auto_wash:
        value_new_list = []
        for value in value_list:
            value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t', '')
            value_new_list.append(str_add_head + value + str_add_tail)
        return list(set(value_new_list))
    else:
        value_new_list = []
        for value in value_list:
            value_new_list.append(str_add_head + value + str_add_tail)
        return list(set(value_new_list))


def get_column_re(rule, text, str_add_head='', str_add_tail='', Auto_wash=True):
    value_list = re.findall(rule, text, re.S)
    if Auto_wash:
        value_new_list = []
        for value in value_list:
            value = value.replace(' ', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('\t', '')
            value_new_list.append(str_add_head + value + str_add_tail)
        return ''.join(list(set(value_new_list)))
    else:
        value_new_list = []
        for value in value_list:
            value_new_list.append(str_add_head + value + str_add_tail)
        return ''.join(list(set(value_new_list)))


def getYesterday(day=0):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=day)
    yesterday = today + oneday
    return yesterday

def get_md5_sz(url):
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# url去重MD5
def get_md5(url):
    if isinstance(url, list) or isinstance(url, tuple) or isinstance(url, str):
        url = str(url)
    m = hashlib.md5()
    if isinstance(url, str):
        url = url.encode('utf-8')
    m.update(url)
    return m.hexdigest()

def get_md5_by_sql(sql, cursor, key):
    # key 代表sql中 字段名。
    try:
        cursor.execute(sql)
        rst = cursor.fetchone()
        md55 = rst[key]
        return md55
    except Exception as ex:
        raise Exception(ex)

# 字符串转元组
def str2tuple(str):
    return tuple(eval(str.split('(')[-1].split(')')[0]))

def cn2en(url):
    md = get_md5(url)[8:24].replace('0', 'g').replace('1', 'h').replace('2', 'i').replace('3', 'j').replace('4',
                                                                                                            'k').replace(
        '5', 'l').replace('6', 'm').replace('7', 'n').replace('8', 'o').replace('9', 'p')
    return md

def get_dict_key(dict, value):
    for i, j in dict.items():
        if j == value:
            return i

def collect_filename(path):
    filenames = listdir(path)
    return filenames


def running_days(amount=10, unit=3):
    """
    此for循环表示：往前推amount个三天;
    :param amount:
    :param unit:
    :return:
    """
    unit = unit - 1
    temp = 0
    for i in range(1, amount + 1):
        h = temp
        q = h + unit
        temp = q + 1
        searchDate = datetime.datetime.now() - datetime.timedelta(days=q)
        startdate = searchDate.strftime("%Y-%m-%d")
        enddate = datetime.datetime.now() - datetime.timedelta(days=h)
        if searchDate > enddate:
            raise Exception('12333')
        enddate = enddate.strftime("%Y-%m-%d")
        yield [startdate, enddate]

def dateRange(beginDate ='2018-02-01',endDate=None):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def partition_days(TimeStart=None, TimeEnd=None, number=None):
    # TimeStart='2018-08-16'
    # TimeEnd='2018-08-16'
    # number=2
    """
      方法含义：在时间区间划分多少分;

      :param amount:
      :param unit:
      :return:
      """
    TimeStart = arrow.get(TimeStart).datetime
    TimeEnd = arrow.get(TimeEnd).datetime
    days = TimeEnd - TimeStart
    days = days.days
    unit = int(math.ceil(days / float(number)))
    temp = 0
    for i in range(number):
        q = temp
        w = (i + 1) * unit
        temp = w + 1
        searchDate = TimeEnd - datetime.timedelta(days=0 + w)
        startdate = searchDate.strftime("%Y-%m-%d")
        enddate_ = TimeEnd - datetime.timedelta(days=0 + q)
        if searchDate > enddate_:
            raise Exception('12333')
        enddate = enddate_.strftime("%Y-%m-%d")
        if searchDate < TimeStart:
            startdate = TimeStart.strftime("%Y-%m-%d")
        yield [startdate, enddate]

def getAllName(messageContent):
    words = pseg.cut(messageContent)
    names = []
    for word, flag in words:
        # print('%s,%s' % (word, flag))
        if flag == 'nr':  # 人名词性为nr
            print(word, '*' * 50)
            names.append(word)
    return names

#分割图像
def FindImageBBox(img):
    v_sum = np.sum(img, axis=0)
    start_i = None
    end_i = None
    minimun_range = 10
    maximun_range = 20
    min_val = 10
    peek_ranges = []
    ser_val = 0
    # 从左往右扫描，遇到非零像素点就以此为字体的左边界
    for i, val in enumerate(v_sum):
        #定位第一个字体的起始位置
        if val > min_val and start_i is None:
            start_i = i
            ser_val = 0
        #继续扫描到字体，继续往右扫描
        elif val > min_val and start_i is not None:
            ser_val = 0
        #扫描到背景，判断空白长度
        elif val <= min_val  and start_i is not None:
            ser_val  = ser_val + 1
            if (i - start_i >= minimun_range and ser_val > 2) or (i - start_i >= maximun_range):
                # print(i)
                end_i = i
                #print(end_i - start_i)
                if start_i> 5:
                    start_i = start_i-5
                peek_ranges.append((start_i, end_i+2))
                start_i = None
                end_i = None
        #扫描到背景，继续扫描下一个字体
        elif val <= min_val and start_i is None:
            ser_val = ser_val+1
        else:
            raise ValueError("cannot parse this case...")
    return peek_ranges

#调用方式
# image = cv2.imread('')
# ret, image1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
# box = FindImageBBox(image1)
# for l,i in enumerate(box):
#     cropped2 = cropped1[0:39, i[0]:i[1]]  # 裁剪坐标为[y0:y1, x0:x1]
#     cv2.imwrite(os.path.join(path1,f"{name_1}_small{l}.jpg"), cropped2)

# 识别验证码或者电话号码
def image_recognize_url(url, max_lenth=None, max_try=10, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'}):
    n = 0
    while n < max_try:
        res = requests.get(url, headers=headers, timeout=5)
        image = BytesIO(res.content)
        image = Image.open(image)
        im = image.convert('L')
        text = pytesseract.image_to_string(im)
        if max_lenth and len(text) == max_lenth:
            return text
        elif not max_lenth:
            if text:
                return text
            else:
                print("识别失败")
        else:
            print("识别失败")
            n += 1
    if n == max_try:
        print("无法识别该验证码")
        return None

def image_recognize_path(image_path):
    im = Image.open('{}'.format(image_path))
    auth = pytesseract.image_to_string(im)
    return auth

def get_photo(url, image_path,
              headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'}):
    path = '/'.join(image_path.split('\\')[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
        red_print("创建{}文件夹".format(path))
    res = requests.get(url, headers=headers, timeout=5)
    with open(image_path, 'wb')as f:
        f.write(res.content)
    red_print("{}download_success".format(image_path))


def get_pdf(url, image_path,
            headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'}, data={},
            proxies={}, type_way="get"):
    path = '/'.join(image_path.split('\\')[:-1])
    if not os.path.exists(path):
        os.makedirs(path)
        red_print("创建{}文件夹".format(path))
    if type_way == "post":
        res = requests.post(url, data=data, headers=headers, proxies=proxies, timeout=5)
    else:
        res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
    with open(image_path, 'wb')as f:
        red_print("{} downloading...".format(image_path))
        for i in res.iter_content():
            f.write(i)
    red_print("{}download_success".format(image_path))
    return True

def get_item_field(items):
    red_print("复制item字段列表值")
    red_print('----------------------------------------------------------')
    for item in items.keys():
        item = '{} = scrapy.Field()'.format(item)
        print(item)
    red_print('----------------------------------------------------------')
    os._exit(0)


def save_csv(keyword_list, path, item):
    """
    保存csv方法
    :param keyword_list: 保存文件的字段或者说是表头
    :param path: 保存文件路径和名字
    :param item: 要保存的字典对象
    :return:
    """
    try:
        # 第一次打开文件时，第一行写入表头
        if not os.path.exists(path):
            with open(path, "w", newline='', encoding='utf-8') as csvfile:  # newline='' 去除空白行
                writer = csv.DictWriter(csvfile, fieldnames=keyword_list)  # 写字典的方法
                writer.writeheader()  # 写表头的方法

        # 接下来追加写入内容
        with open(path, "a", newline='', encoding='utf-8') as csvfile:  # newline='' 一定要写，否则写入数据有空白行
            writer = csv.DictWriter(csvfile, fieldnames=keyword_list)
            writer.writerow(item)  # 按行写入数据
            print("^_^ write success")
    except:
        pass


def get_cookies(url, executable_path="E:\chrome download\chromedriver.exe", type="str", Evasion_detection=True):
    desired_capabilities = DesiredCapabilities.CHROME  # 设置这个选项，加载更快。
    desired_capabilities["pageLoadStrategy"] = "none"
    chrome_options = webdriver.ChromeOptions()  # 无界面模式的选项设置
    if Evasion_detection:
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 实现了规避监测
    else:
        chrome_options.add_argument('--headless')  # 用规避检测无法使用无头模式
    chrome_options.add_argument(
        'User-Agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"')
    browser = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    browser.get(url)
    if Evasion_detection:
        time.sleep(5)
    else:
        time.sleep(1)
    if type == "page":
        return browser.page_source
    result_list = browser.get_cookies()
    if type == "str":
        cookie = ""
        for i in result_list:
            cookie = cookie + i["name"] + "=" + i["value"] + ";"
        return cookie[:-1]
    elif type == "dict":
        cookie_dict = {}
        for i in result_list:
            cookie_dict[i["name"]] = i["value"]
        return cookie_dict
    else:
        raise ValueError("please choice a type 'str' or 'dict'")


def excute_js(js_code_path, func, args):
    with open(js_code_path, 'r')as f:
        js_code = f.read()
    js_code = execjs.compile(js_code)
    result = js_code.call(func, args)
    return result


def write_file(path, value):
    with open(path, 'a')as f:
        if isinstance(value, dict):
            result = json.dumps(value, ensure_ascii=False)
            f.write(result)
        else:
            f.write(value)


def convert_removing_interference(image_path, value_px=130, image_show=True, save_image=False):
    # np.set_printoptions(threshold=np.inf) #全显示图片数组
    img = Image.open(image_path)
    img = img.convert("L")
    array_list = np.array(img)
    shape = array_list.shape
    array_list = array_list.tolist()
    new_list = []
    for list in array_list:
        for i in list:
            new_list.append(i)
    for i, value in enumerate(new_list):
        if value < value_px:
            new_list[i] = 0
    # print(new_list)
    result = np.reshape(new_list, shape)
    new_im = Image.fromarray(result)
    if image_show:
        new_im.show()
    if save_image:
        new_im.save(image_path.split('.')[0] + "_new." + image_path.split('.')[-1])

def dict2str(cookie):
    str = ''
    for k,v in cookie.items():
        str += k +'=' +v+';'
    return str.replace('\n','').replace(' ','')[:-1]



def more_process(num, func):
    for i in range(num):
        p = Process(target=func)
        p.start()


ip_list = []
start = time.time()


def get_ip():
    ip = requests.get(url='http://119.3.187.233:8005/ip').json()
    return ip

def my_request(url,conn=requests, proxy=None, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
               , allow_status=[200], timeout=(5, 8), method='get', data=None, retry=5,
               timesleep=0, show_result=False, allow_redirects=False, verify=False,change_ip_times=5):
    request_count = 0
    status_code_not_allow = 0
    while True:
        if proxy and status_code_not_allow > change_ip_times:
            proxy = get_ip()
        try:
            if method.lower() == 'get':
                response = conn.get(url=url, headers=headers, data=data, timeout=timeout,
                                    allow_redirects=allow_redirects,
                                    proxies=proxy, verify=verify)
                print("响应状态：{} 访问url：{}".format(response.status_code, url))
                if response.status_code in allow_status:
                    return {'res':response,'conn':conn,'proxy':proxy}
                if response.status_code not in allow_status:
                    status_code_not_allow += 1
                if proxy and response.status_code == 403:
                    proxy = get_ip()
                if show_result:
                    print(response.text)

            elif method.lower() == 'post':
                response = conn.post(url=url, headers=headers, data=data, timeout=timeout,
                                     allow_redirects=allow_redirects,
                                     proxies=proxy, verify=verify)
                print("响应状态：{} 访问url：{} 请求参数：{}".format(response.status_code, url, data))
                if response.status_code in allow_status:
                    return {'res': response, 'conn': conn, 'proxy': proxy}
                if response.status_code not in allow_status:
                    status_code_not_allow += 1
                if proxy and response.status_code == 403:
                    proxy = get_ip()
                if show_result:
                    print(response.text)
        except:
            print("本次请求失败,重试次数剩余：{}".format(retry-request_count))
            proxy = get_ip()
        request_count += 1
        time.sleep(timesleep)
        if request_count > retry - 1:
            red_print("请求失败 request_way：{} URL：{} data：{} retry_times：{}".format(method,url,data,retry))
            return

# 特征提取，获取图像二值化数学值
def getBinaryPix(im):
    im = Image.open(im)
    img = np.array(im)
    rows, cols = img.shape
    for i in range(rows):
        for j in range(cols):
            if (img[i, j] <= 128):
                img[i, j] = 0
            else:
                img[i, j] = 1
    binpix = np.ravel(img)
    return binpix


# ''' 根据该像素周围点为黑色的像素数（包括本身）来判断是否把它归属于噪声，如果是噪声就将其变为白色'''
# '''
# 	input:  img:二值化图
# 			number：周围像素数为黑色的小于number个，就算为噪声，并将其去掉，如number=6，
# 			就是一个像素周围9个点（包括本身）中小于6个的就将这个像素归为噪声
# 	output：返回去噪声的图像
# '''
def noise_removal(img_dir, save_dir=''):
    img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
    for i in range(len(img_name)):
        _name = img_name[i]
        path = os.path.join(img_dir, _name)
        im = Image.open(path)
        pix = im.load()
        width = im.size[0]
        height = im.size[1]
        for x in range(width):
            for y in range(height):
                r, g, b = pix[x, y]
                r0, r1, r2 = r, g, b
                if r0 + r1 + r2 >= 400 or r0 >= 250 or r1 >= 250 or r2 >= 250:
                    im.putpixel((x, y), (255, 255, 255))
                elif x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    im.putpixel((x, y), (255, 255, 255))
                else:
                    im.putpixel((x, y), (0, 0, 0))
        if save_dir:
            if not os._exists(save_dir):
                os.mkdir(save_dir)
            im.save(r'{}\new_{}'.format(save_dir, _name))
        else:
            im.save(r'{}\new_{}'.format(img_dir, _name))
            print(path)
    print("图片预处理完成！")


def get_xls_data(file_path, nrow=1, ncol=1, value="all_row", sheet='Sheet1'):
    # 文件路径的中文转码，如果路径非中文可以跳过
    # file_path = file_path.decode('utf-8')
    # 获取数据
    data = xlrd.open_workbook(file_path)
    # 获取sheet 此处有图注释（见图1）
    table = data.sheet_by_name(sheet)
    red_print("当前获取{}表格内容数据\n".format(sheet))
    # 获取总行数
    nrows = table.nrows
    # 获取总列数
    ncols = table.ncols
    if value == "nrow":
        rowvalue = table.row_values(nrow)
        return rowvalue
    # 获取一列的数值，例如第6列
    elif value == "ncol":
        col_values = table.col_values(ncol)
        return col_values
    # 获取一个单元格的数值，例如第5行第6列
    elif value == "cell":
        cell_value = table.cell(nrow, ncol).value
        return cell_value
    # 获取所有行
    elif value == "all_row":
        result_list_nrow = []
        for i in range(nrows):
            rowvalue = table.row_values(i)
            result_list_nrow.append(rowvalue)
        return result_list_nrow
    # 获取所有列
    elif value == "all_col":
        result_list_ncol = []
        for i in range(ncols):
            col_values = table.col_values(i)
            result_list_ncol.append(col_values)
        return result_list_ncol
    else:
        red_print(
            "请选择value值模式:{\n'all_row':'取出全部行',\n'all_col':'取出全部列',\n'nrow':'取出指定行',\n'n_col':'取出指定列',\n'cell':'取出指定单元格'}")
        return None


province = [
    '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南',
    '四川', '贵州', '云南', '陕西', '甘肃', '青海', '北京', '天津', '上海', '重庆', '内蒙古', '广西', '宁夏', '新疆', '西藏',
]
city0 = ['北京', '上海', '广州', '深圳']
city1 = ['成都', '杭州', '重庆', '武汉', '苏州', '西安', '天津', '南京', '郑州', '长沙', '沈阳', '青岛', '宁波', '东莞', '无锡']
city2 = [
    '昆明', '大连', '厦门', '合肥', '佛山', '福州', '哈尔滨', '济南', '温州', '长春', '石家庄', '常州', '泉州', '南宁', '贵阳', '南昌', '南通', '金华', '徐州',
    '太原', '嘉兴', '烟台', '惠州', '保定', '台州', '中山', '绍兴', '乌鲁木齐', '潍坊', '兰州',
]
city3 = [
    '珠海', '镇江', '海口', '扬州', '临沂', '洛阳', '唐山', '呼和浩特', '盐城', '汕头', '廊坊', '泰州', '济宁', '湖州', '江门', '银川', '淄博', '邯郸', '芜湖',
    '漳州', '绵阳', '桂林', '三亚', '遵义', '咸阳', '上饶', '莆田', '宜昌', '赣州', '淮安', '揭阳', '沧州', '商丘', '连云港', '柳州', '岳阳', '信阳', '株洲',
    '衡阳', '襄阳', '南阳', '威海', '湛江', '包头', '鞍山', '九江', '大庆', '许昌', '新乡', '宁德', '西宁', '宿迁', '菏泽', '蚌埠', '邢台', '铜陵', '阜阳',
    '荆州', '驻马店', '湘潭', '滁州', '肇庆', '德阳', '曲靖', '秦皇岛', '潮州', '吉林', '常德', '宜春', '黄冈',
]
city4 = [
    '舟山市', '泰安市', '孝感市', '鄂尔多斯市', '开封市', '南平市', '齐齐哈尔市', '德州市', '宝鸡市', '马鞍山市', '郴州市', '安阳市', '龙岩市', '聊城市', '渭南市', '宿州市',
    '衢州市', '梅州市', '宣城市', '周口市', '丽水市', '安庆市', '三明市', '枣庄市', '南充市', '淮南市', '平顶山市', '东营市', '呼伦贝尔市', '乐山市', '张家口市', '清远市',
    '焦作市', '河源市', '运城市', '锦州市', '赤峰市', '六安市', '盘锦市', '宜宾市', '榆林市', '日照市', '晋中市', '怀化市', '承德市', '遂宁市', '毕节市', '佳木斯市',
    '滨州市', '益阳市', '汕尾市', '邵阳市', '玉林市', '衡水市', '韶关市', '吉安市', '北海市', '茂名市', '延边朝鲜族自治州', '黄山市', '阳江市', '抚州市', '娄底市', '营口市',
    '牡丹江市', '大理白族自治州', '咸宁市', '黔东南苗族侗族自治州', '安顺市', '黔南布依族苗族自治州', '泸州市', '玉溪市', '通辽市', '丹东市', '临汾市', '眉山市', '十堰市', '黄石市',
    '濮阳市', '亳州市', '抚顺市', '永州市', '丽江市', '漯河市', '铜仁市', '大同市', '松原市', '通化市', '红河哈尼族彝族自治州', '内江市', '新余市',
]
city5 = [
    '长治市', '荆门市', '梧州市', '拉萨市', '汉中市', '四平市', '鹰潭市', '广元市', '云浮市', '葫芦岛市', '本溪市', '景德镇市', '六盘水市', '达州市', '铁岭市', '钦州市',
    '广安市', '保山市', '自贡市', '辽阳市', '百色市', '乌兰察布市', '普洱市', '黔西南布依族苗族自治州', '贵港市', '萍乡市', '酒泉市', '忻州市', '天水市', '防城港市', '鄂州市',
    '锡林郭勒盟', '白山市', '黑河市', '克拉玛依市', '临沧市', '三门峡市', '伊春市', '鹤壁市', '随州市', '晋城市', '文山壮族苗族自治州', '巴彦淖尔市', '河池市', '凉山彝族自治州',
    '乌海市', '楚雄彝族自治州', '恩施土家族苗族自治州', '吕梁市', '池州市', '西双版纳傣族自治州', '延安市', '雅安市', '巴中市', '双鸭山市', '攀枝花市', '阜新市', '兴安盟',
    '张家界市', '昭通市', '海东市', '安康市', '白城市', '朝阳市', '绥化市', '淮北市', '辽源市', '定西市', '吴忠市', '鸡西市', '张掖市', '鹤岗市', '崇左市',
    '湘西土家族苗族自治州', '林芝市', '来宾市', '贺州市', '德宏傣族景颇族自治州', '资阳市', '阳泉市', '商洛市', '陇南市', '平凉市', '庆阳市', '甘孜藏族自治州', '大兴安岭地区',
    '迪庆藏族自治州', '阿坝藏族羌族自治州', '伊犁哈萨克自治州', '中卫市', '朔州市', '儋州市', '铜川市', '白银市', '石嘴山市', '莱芜市', '武威市', '固原市', '昌吉回族自治州',
    '巴音郭楞蒙古自治州', '嘉峪关市', '阿拉善盟', '阿勒泰地区', '七台河市', '海西蒙古族藏族自治州', '塔城地区', '日喀则市', '昌都市', '海南藏族自治州', '金昌市', '哈密市',
    '怒江傈僳族自治州', '吐鲁番市', '那曲地区', '阿里地区', '喀什地区', '阿克苏地区', '甘南藏族自治州', '海北藏族自治州', '山南市', '临夏回族自治州', '博尔塔拉蒙古自治州', '玉树藏族自治州',
    '黄南藏族自治州', '和田地区', '三沙市', '克孜勒苏柯尔克孜自治州', '果洛藏族自治州',
]
department = [
    '外交部', '国防部', '国家发展和改革委员会', '教育部', '科学技术部', '工业和信息化部', '国家民族事务委员会', '公安部', '国家安全部', '民政部', '司法部', '财政部',
    '人力资源和社会保障部', '自然资源部', '生态环境部', '住房和城乡建设部', '交通运输部', '水利部', '农业农村部', '商务部', '文化和旅游部', '国家卫生健康委员会', '退役军人事务部',
    '应急管理部', '人民银行', '审计署', '国家语言文字工作委员会', '国家外国专家局', '国家航天局', '国家原子能机构', '国家海洋局', '国家核安全局', '国务院国有资产监督管理委员会', '海关总署',
    '国家税务总局', '国家市场监督管理总局', '国家广播电视总局', '国家体育总局', '国家统计局', '国家国际发展合作署', '国家医疗保障局', '国务院参事室', '国家机关事务管理局',
    '国家认证认可监督管理委员会', '国家标准化管理委员会', '国家新闻出版署（国家版权局）', '国家宗教事务局', '国务院港澳事务办公室', '国务院研究室', '国务院侨务办公室', '国务院台湾事务办公室',
    '国家互联网信息办公室', '国务院新闻办公室', '新华通讯社', '中国科学院', '中国社会科学院', '中国工程院', '国务院发展研究中心', '中央广播电视总台', '中国气象局', '中国银行保险监督管理委员会',
    '中国证券监督管理委员会', '国家行政学院', '国家信访局', '国家粮食和物资储备局', '国家能源局', '国家国防科技工业局', '国家烟草专卖局', '国家移民管理局', '国家林业和草原局', '国家铁路局',
    '中国民用航空局', '国家邮政局', '国家文物局', '国家中医药管理局', '国家煤矿安全监察局', '国家外汇管理局', '国家药品监督管理局', '国家知识产权局', '出入境管理局', '国家公园管理局',
    '国家公务员局', '国家档案局', '国家保密局', '国家密码管理局',
]
Over_the_Third_tier_Cities = city0 + city1 + city2
Over_the_Third_tier_Cities_and_province = list(set(province + city0 + city1 + city2))

number = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
number_string = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']
Punctuation = ["`", "·", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "（", "）", "-", "—", "_", "=", "+", "{",
               "}", "[", "]", "【", "】", "\\", "、", "|", "；", ";", "：", ":", "'", '"', "‘", "’", '“', "”", ",", "，", ".",
               "。", "<", ">", "《", "》", "/", "？", "?"]
ZhEnLetterTable = [
    ("(", "（",), (")", "）"), ("０", "0"), ("１", "1"), ("２", "2"),
    ("３", "3"), ("４", "4"), ("５", "5"), ("６", "6"), ("７", "7"), ("８", "8"), ("９", "9"), ("ａ", "a"),
    ("ｂ", "b"), ("ｃ", "c"), ("ｄ", "d"), ("ｅ", "e"), ("ｆ", "f"), ("ｇ", "g"), ("ｈ", "h"), ("ｉ", "i"),
    ("ｊ", "j"), ("ｋ", "k"), ("ｌ", "l"), ("ｍ", "m"), ("ｎ", "n"), ("ｏ", "o"), ("ｐ", "p"), ("ｑ", "q"),
    ("ｒ", "r"), ("ｓ", "s"), ("ｔ", "t"), ("ｕ", "u"), ("ｖ", "v"), ("ｗ", "w"), ("ｘ", "x"), ("ｙ", "y"),
    ("ｚ", "z"), ("Ａ", "A"), ("Ｂ", "B"), ("Ｃ", "C"), ("Ｄ", "D"), ("Ｅ", "E"), ("Ｆ", "F"), ("Ｇ", "G"),
    ("Ｈ", "H"), ("Ｉ", "I"), ("Ｊ", "J"), ("Ｋ", "K"), ("Ｌ", "L"), ("Ｍ", "M"), ("Ｎ", "N"), ("Ｏ", "O"),
    ("Ｐ", "P"), ("Ｑ", "Q"), ("Ｒ", "R"), ("Ｓ", "S"), ("Ｔ", "T"), ("Ｕ", "U"), ("Ｖ", "V"), ("Ｗ", "W"),
    ("Ｘ", "X"), ("Ｙ", "Y"), ("Ｚ", "Z")
]

#行政区划
xz_list = {'北京市': '110000', '市辖区': '650201', '东城区': '110101', '西城区': '110102', '崇文区': '110103', '宣武区': '110104',
           '朝阳区': '220104', '丰台区': '110106', '石景山区': '110107', '海淀区': '110108', '门头沟区': '110109', '燕山区': '110110',
           '房山区': '110111', '通州区': '110112', '顺义区': '110113', '昌平区': '110114', '大兴区': '110115', '怀柔区': '110116',
           '平谷区': '110117', '县': '500200', '密云县': '110228', '延庆县': '110229', '天津市': '120000', '天津市直属': '120001',
           '和平区': '210102', '河东区': '371312', '河西区': '120103', '南开区': '120104', '河北区': '120105', '红桥区': '120106',
           '塘沽区': '120107', '汉沽区': '120108', '大港区': '120109', '东丽区': '120110', '西青区': '120111', '津南区': '120112',
           '北辰区': '120113', '武清区': '120114', '宝坻区': '120115', '宁河县': '120221', '静海县': '120223', '蓟县': '120225',
           '河北省': '130000', '石家庄市': '130100', '长安区': '610116', '桥东区': '130702', '桥西区': '130703', '新华区': '410402',
           '井陉矿区': '130107', '裕华区': '130108', '井陉县': '130121', '正定县': '130123', '栾城县': '130124', '行唐县': '130125',
           '灵寿县': '130126', '高邑县': '130127', '深泽县': '130128', '赞皇县': '130129', '无极县': '130130', '平山县': '130131',
           '元氏县': '130132', '赵县': '130133', '辛集市': '130181', '藁城市': '130182', '晋州市': '130183', '新乐市': '130184',
           '鹿泉市': '130185', '唐山市': '130200', '路南区': '130202', '路北区': '130203', '古冶区': '130204', '开平区': '130205',
           '丰南区': '130207', '丰润区': '130208', '芦台经济开发区': '130210', '汉沽管理区': '130211', '滦县': '130223', '滦南县': '130224',
           '乐亭县': '130225', '迁西县': '130227', '玉田县': '130229', '唐海县': '130230', '遵化市': '130281', '迁安市': '130283',
           '秦皇岛市': '130300', '海港区': '130302', '山海关区': '130303', '北戴河区': '130304', '秦皇岛市开发区': '130305',
           '青龙满族自治县': '130321', '昌黎县': '130322', '抚宁县': '130323', '卢龙县': '130324', '邯郸市': '130400', '邯山区': '130402',
           '丛台区': '130403', '复兴区': '130404', '峰峰矿区': '130406', '邯郸市开发区': '130407', '邯郸市马头生态工业城': '130408',
           '邯郸县': '130421', '临漳县': '130423', '成安县': '130424', '大名县': '130425', '涉县': '130426', '磁县': '130427',
           '肥乡县': '130428', '永年县': '130429', '邱县': '130430', '鸡泽县': '130431', '广平县': '130432', '馆陶县': '130433',
           '魏县': '130434', '曲周县': '130435', '武安市': '130481', '邢台市': '130500', '邢台市开发区': '130504', '邢台县': '130521',
           '临城县': '130522', '内丘县': '130523', '柏乡县': '130524', '隆尧县': '130525', '任县': '130526', '南和县': '130527',
           '宁晋县': '130528', '巨鹿县': '130529', '新河县': '130530', '广宗县': '130531', '平乡县': '130532', '威县': '130533',
           '清河县': '130534', '临西县': '130535', '大曹庄管理区': '130536', '南宫市': '130581', '沙河市': '130582', '保定市': '130600',
           '新市区': '650104', '北市区': '130603', '南市区': '130604', '满城县': '130621', '清苑县': '130622', '涞水县': '130623',
           '阜平县': '130624', '徐水县': '130625', '定兴县': '130626', '唐县': '130627', '高阳县': '130628', '容城县': '130629',
           '涞源县': '130630', '望都县': '130631', '安新县': '130632', '易县': '130633', '曲阳县': '130634', '蠡县': '130635',
           '顺平县': '130636', '博野县': '130637', '雄县': '130638', '涿州市': '130681', '定州市': '130682', '安国市': '130683',
           '高碑店市': '130684', '保定白沟白洋淀温泉城管委会': '130698', '保定市高新区': '130699', '张家口市': '130700', '宣化区': '130705',
           '下花园区': '130706', '察北管理区': '130707', '塞北管理区': '130708', '张家口市高新区': '130709', '宣化县': '130721',
           '张北县': '130722', '康保县': '130723', '沽源县': '130724', '尚义县': '130725', '蔚县': '130726', '阳原县': '130727',
           '怀安县': '130728', '万全县': '130729', '怀来县': '130730', '涿鹿县': '130731', '赤城县': '130732', '崇礼县': '130733',
           '承德市': '130800', '双桥区': '500111', '双滦区': '130803', '鹰手营子矿区': '130804', '承德市开发区': '130805', '承德县': '130821',
           '兴隆县': '130822', '平泉县': '130823', '滦平县': '130824', '隆化县': '130825', '丰宁满族自治县': '130826', '宽城满族自治县': '130827',
           '围场满族蒙古族自治县': '130828', '沧州市': '130900', '运河区': '130903', '沧州市开发区': '130904', '沧县': '130921', '青县': '130922',
           '东光县': '130923', '海兴县': '130924', '盐山县': '130925', '肃宁县': '130926', '南皮县': '130927', '吴桥县': '130928',
           '献县': '130929', '孟村回族自治县': '130930', '渤海新区中捷产业园区': '130931', '沧州市南大港': '130932', '渤海新区黄骅港开发区': '130934',
           '泊头市': '130981', '任丘市': '130982', '黄骅市': '130983', '河间市': '130984', '廊坊市': '131000', '安次区': '131002',
           '广阳区': '131003', '廊坊经济技术开发区': '131005', '固安县': '131022', '永清县': '131023', '香河县': '131024', '大城县': '131025',
           '文安县': '131026', '大厂回族自治县': '131028', '霸州市': '131081', '三河市': '131082', '衡水市': '131100', '桃城区': '131102',
           '衡水市高新区': '131105', '衡水湖开发区': '131106', '枣强县': '131121', '武邑县': '131122', '武强县': '131123', '饶阳县': '131124',
           '安平县': '131125', '故城县': '131126', '景县': '131127', '阜城县': '131128', '冀州市': '131181', '深州市': '131182',
           '山西省': '140000', '省直': '349901', '太原市': '140100', '小店区': '140105', '迎泽区': '140106', '杏花岭区': '140107',
           '尖草坪区': '140108', '万柏林区': '140109', '晋源区': '140110', '清徐县': '140121', '阳曲县': '140122', '娄烦县': '140123',
           '古交市': '140181', '大同市': '140200', '城区': '441502', '矿区': '140303', '南郊区': '140211', '新荣区': '140212',
           '阳高县': '140221', '天镇县': '140222', '广灵县': '140223', '灵丘县': '140224', '浑源县': '140225', '左云县': '140226',
           '大同县': '140227', '阳泉市': '140300', '郊区': '340711', '平定县': '140321', '盂县': '140322', '长治市': '140400',
           '长治县': '140421', '襄垣县': '140423', '屯留县': '140424', '平顺县': '140425', '黎城县': '140426', '壶关县': '140427',
           '长子县': '140428', '武乡县': '140429', '沁县': '140430', '沁源县': '140431', '潞城市': '140481', '晋城市': '140500',
           '沁水县': '140521', '阳城县': '140522', '陵川县': '140524', '泽州县': '140525', '高平市': '140581', '朔州市': '140600',
           '朔城区': '140602', '平鲁区': '140603', '山阴县': '140621', '应县': '140622', '右玉县': '140623', '怀仁县': '140624',
           '晋中市': '140700', '榆次区': '140702', '榆社县': '140721', '左权县': '140722', '和顺县': '140723', '昔阳县': '140724',
           '寿阳县': '140725', '太谷县': '140726', '祁县': '140727', '平遥县': '140728', '灵石县': '140729', '介休市': '140781',
           '运城市': '140800', '盐湖区': '140802', '临猗县': '140821', '万荣县': '140822', '闻喜县': '140823', '稷山县': '140824',
           '新绛县': '140825', '绛县': '140826', '垣曲县': '140827', '夏县': '140828', '平陆县': '140829', '芮城县': '140830',
           '永济市': '140881', '河津市': '140882', '忻州市': '140900', '忻府区': '140902', '定襄县': '140921', '五台县': '140922',
           '代县': '140923', '繁峙县': '140924', '宁武县': '140925', '静乐县': '140926', '神池县': '140927', '五寨县': '140928',
           '岢岚县': '140929', '河曲县': '140930', '保德县': '140931', '偏关县': '140932', '原平市': '140981', '临汾市': '141000',
           '尧都区': '141002', '曲沃县': '141021', '翼城县': '141022', '襄汾县': '141023', '洪洞县': '141024', '古县': '141025',
           '安泽县': '141026', '浮山县': '141027', '吉县': '141028', '乡宁县': '141029', '大宁县': '141030', '隰县': '141031',
           '永和县': '141032', '蒲县': '141033', '汾西县': '141034', '侯马市': '141081', '霍州市': '141082', '吕梁市': '141100',
           '离石区': '141102', '文水县': '141121', '交城县': '141122', '兴县': '141123', '临县': '141124', '柳林县': '141125',
           '石楼县': '141126', '岚县': '141127', '方山县': '141128', '中阳县': '141129', '交口县': '141130', '孝义市': '141181',
           '汾阳市': '141182', '内蒙古自治区': '150000', '呼和浩特市': '150100', '新城区': '610102', '回民区': '150103', '玉泉区': '150104',
           '赛罕区': '150105', '土默特左旗': '150121', '托克托县': '150122', '和林格尔县': '150123', '清水河县': '150124', '武川县': '150125',
           '包头市': '150200', '东河区': '150202', '昆都仑区': '150203', '青山区': '420107', '石拐区': '150205', '白云鄂博矿区': '150206',
           '九原区': '150207', '土默特右旗': '150221', '固阳县': '150222', '达尔罕茂明安联合旗': '150223', '乌海市': '150300',
           '海勃湾区': '150302', '海南区': '150303', '乌达区': '150304', '赤峰市': '150400', '红山区': '150402', '元宝山区': '150403',
           '松山区': '150404', '阿鲁科尔沁旗': '150421', '巴林左旗': '150422', '巴林右旗': '150423', '林西县': '150424', '克什克腾旗': '150425',
           '翁牛特旗': '150426', '喀喇沁旗': '150428', '宁城县': '150429', '敖汉旗': '150430', '通辽市': '150500', '科尔沁区': '150502',
           '科尔沁左翼中旗': '150521', '科尔沁左翼后旗': '150522', '开鲁县': '150523', '库伦旗': '150524', '奈曼旗': '150525',
           '扎鲁特旗': '150526', '霍林郭勒市': '150581', '鄂尔多斯市': '150600', '东胜区': '150602', '达拉特旗': '150621', '准格尔旗': '150622',
           '鄂托克前旗': '150623', '鄂托克旗': '150624', '杭锦旗': '150625', '乌审旗': '150626', '伊金霍洛旗': '150627', '呼伦贝尔市': '150700',
           '海拉尔区': '150702', '阿荣旗': '150721', '莫力达瓦达斡尔族自治旗': '150722', '鄂伦春自治旗': '150723', '鄂温克族自治旗': '150724',
           '陈巴尔虎旗': '150725', '新巴尔虎左旗': '150726', '新巴尔虎右旗': '150727', '满洲里市': '150781', '牙克石市': '150782',
           '扎兰屯市': '150783', '额尔古纳市': '150784', '根河市': '150785', '巴彦淖尔市': '150800', '临河区': '150802', '五原县': '150821',
           '磴口县': '150822', '乌拉特前旗': '150823', '乌拉特中旗': '150824', '乌拉特后旗': '150825', '杭锦后旗': '150826',
           '乌兰察布市': '150900', '集宁区': '150902', '卓资县': '150921', '化德县': '150922', '商都县': '150923', '兴和县': '150924',
           '凉城县': '150925', '察哈尔右翼前旗': '150926', '察哈尔右翼中旗': '150927', '察哈尔右翼后旗': '150928', '四子王旗': '150929',
           '丰镇市': '150981', '兴安盟': '152200', '乌兰浩特市': '152201', '阿尔山市': '152202', '科尔沁右翼前旗': '152221',
           '科尔沁右翼中旗': '152222', '扎赉特旗': '152223', '突泉县': '152224', '锡林郭勒盟': '152500', '二连浩特市': '152501',
           '锡林浩特市': '152502', '阿巴嘎旗': '152522', '苏尼特左旗': '152523', '苏尼特右旗': '152524', '东乌珠穆沁旗': '152525',
           '西乌珠穆沁旗': '152526', '太仆寺旗': '152527', '镶黄旗': '152528', '正镶白旗': '152529', '正蓝旗': '152530', '多伦县': '152531',
           '阿拉善盟': '152900', '阿拉善左旗': '152921', '阿拉善右旗': '152922', '额济纳旗': '152923', '辽宁省': '210000', '沈阳市': '210100',
           '沈河区': '210103', '大东区': '210104', '皇姑区': '210105', '铁西区': '220302', '苏家屯区': '210111', '东陵区': '210112',
           '沈北新区': '210113', '于洪区': '210114', '浑南新区': '210115', '棋盘山区': '210116', '辽中县': '210122', '康平县': '210123',
           '法库县': '210124', '新民市': '210181', '大连市': '210200', '中山区': '210202', '西岗区': '210203', '沙河口区': '210204',
           '甘井子区': '210211', '旅顺口区': '210212', '金州新区': '210213', '保税区': '210214', '长兴岛临港工业区': '210215',
           '大连市高新园区': '210216', '大连市花园口经济区': '210217', '长海县': '210224', '瓦房店市': '210281', '普兰店市': '210282',
           '庄河市': '210283', '鞍山市': '210300', '铁东区': '220303', '立山区': '210304', '千山区': '210311', '台安县': '210321',
           '岫岩满族自治县': '210323', '海城市': '210381', '抚顺市': '210400', '新抚区': '210402', '东洲区': '210403', '望花区': '210404',
           '顺城区': '210411', '经济开发区': '210413', '抚顺县': '210421', '新宾满族自治县': '210422', '清原满族自治县': '210423',
           '本溪市': '210500', '平山区': '210502', '溪湖区': '210503', '明山区': '210504', '南芬区': '210505', '石桥子开发区': '210515',
           '本溪满族自治县': '210521', '桓仁满族自治县': '210522', '丹东市': '210600', '元宝区': '210602', '振兴区': '210603', '振安区': '210604',
           '开发区': '440806', '宽甸满族自治县': '210624', '东港市': '210681', '凤城市': '210682', '锦州市': '210700', '古塔区': '210702',
           '凌河区': '210703', '太和区': '210711', '松山新区': '210714', '黑山县': '210726', '义县': '210727', '凌海市': '210781',
           '北镇市': '210782', '营口市': '210800', '站前区': '210802', '西市区': '210803', '鲅鱼圈区': '210804', '老边区': '210811',
           '盖州市': '210881', '大石桥市': '210882', '阜新市': '210900', '海州区': '320706', '新邱区': '210903', '太平区': '210904',
           '清河门区': '210905', '细河区': '210911', '阜新蒙古族自治县': '210921', '彰武县': '210922', '辽阳市': '211000', '白塔区': '211002',
           '文圣区': '211003', '宏伟区': '211004', '弓长岭区': '211005', '太子河区': '211011', '辽阳县': '211021', '灯塔市': '211081',
           '盘锦市': '211100', '双台子区': '211102', '兴隆台区': '211103', '大洼县': '211121', '盘山县': '211122', '辽河油田': '211199',
           '铁岭市': '211200', '银州区': '211202', '清河区': '320802', '铁岭县': '211221', '西丰县': '211223', '昌图县': '211224',
           '调兵山市': '211281', '开原市': '211282', '朝阳市': '211300', '双塔区': '211302', '龙城区': '211303', '朝阳县': '211321',
           '建平县': '211322', '喀喇沁左翼蒙古族自治县': '211324', '北票市': '211381', '凌源市': '211382', '葫芦岛市': '211400',
           '连山区': '211402', '龙港区': '211403', '南票区': '211404', '绥中县': '211421', '建昌县': '211422', '兴城市': '211481',
           '吉林省': '220000', '长春市': '220100', '南关区': '220102', '宽城区': '220103', '二道区': '220105', '绿园区': '220106',
           '双阳区': '220112', '农安县': '220122', '九台市': '220181', '榆树市': '220182', '德惠市': '220183', '吉林市': '220200',
           '昌邑区': '220202', '龙潭区': '220203', '船营区': '220204', '丰满区': '220211', '永吉县': '220221', '蛟河市': '220281',
           '桦甸市': '220282', '舒兰市': '220283', '磐石市': '220284', '四平市': '220300', '梨树县': '220322', '伊通满族自治县': '220323',
           '公主岭市': '220381', '双辽市': '220382', '辽源市': '220400', '龙山区': '220402', '西安区': '231005', '东丰县': '220421',
           '东辽县': '220422', '通化市': '220500', '东昌区': '220502', '二道江区': '220503', '通化县': '220521', '辉南县': '220523',
           '柳河县': '220524', '梅河口市': '220581', '集安市': '220582', '白山市': '220600', '八道江区': '220602', '江源区': '220605',
           '抚松县': '220621', '靖宇县': '220622', '长白朝鲜族自治县': '220623', '临江市': '220681', '松原市': '220700', '宁江区': '220702',
           '前郭尔罗斯蒙古族自治县': '220721', '长岭县': '220722', '乾安县': '220723', '扶余县': '220724', '白城市': '220800', '洮北区': '220802',
           '镇赉县': '220821', '通榆县': '220822', '洮南市': '220881', '大安市': '220882', '延边朝鲜族自治州': '222400', '延吉市': '222401',
           '图们市': '222402', '敦化市': '222403', '珲春市': '222404', '龙井市': '222405', '和龙市': '222406', '汪清县': '222424',
           '安图县': '222426', '黑龙江省': '230000', '黑龙江省省本级': '230001', '哈尔滨市': '230100', '道里区': '230102', '南岗区': '230103',
           '道外区': '230104', '香坊区': '230106', '平房区': '230108', '松北区': '230109', '呼兰区': '230111', '阿城区': '230112',
           '依兰县': '230123', '方正县': '230124', '宾县': '230125', '巴彦县': '230126', '木兰县': '230127', '通河县': '230128',
           '延寿县': '230129', '双城市': '230182', '尚志市': '230183', '五常市': '230184', '齐齐哈尔市': '230200', '龙沙区': '230202',
           '建华区': '230203', '铁锋区': '230204', '昂昂溪区': '230205', '富拉尔基区': '230206', '碾子山区': '230207',
           '梅里斯达斡尔族区': '230208', '龙江县': '230221', '依安县': '230223', '泰来县': '230224', '甘南县': '230225', '富裕县': '230227',
           '克山县': '230229', '克东县': '230230', '拜泉县': '230231', '讷河市': '230281', '鸡西市': '230300', '鸡冠区': '230302',
           '恒山区': '230303', '滴道区': '230304', '梨树区': '230305', '城子河区': '230306', '麻山区': '230307', '鸡东县': '230321',
           '虎林市': '230381', '密山市': '230382', '鹤岗市': '230400', '向阳区': '230803', '工农区': '230403', '南山区': '440305',
           '兴安区': '230405', '东山区': '230406', '兴山区': '230407', '萝北县': '230421', '绥滨县': '230422', '双鸭山市': '230500',
           '尖山区': '230502', '岭东区': '230503', '四方台区': '230505', '宝山区': '310113', '集贤县': '230521', '友谊县': '230522',
           '宝清县': '230523', '饶河县': '230524', '大庆市': '230600', '萨尔图区': '230602', '龙凤区': '230603', '让胡路区': '230604',
           '红岗区': '230605', '大同区': '230606', '肇州县': '230621', '肇源县': '230622', '林甸县': '230623', '杜尔伯特蒙古族自治县': '230624',
           '伊春市': '230700', '伊春区': '230702', '南岔区': '230703', '友好区': '230704', '西林区': '230705', '翠峦区': '230706',
           '新青区': '230707', '美溪区': '230708', '金山屯区': '230709', '五营区': '230710', '乌马河区': '230711', '汤旺河区': '230712',
           '带岭区': '230713', '乌伊岭区': '230714', '红星区': '230715', '上甘岭区': '230716', '嘉荫县': '230722', '铁力市': '230781',
           '铁力林业局': '230791', '双丰林业局': '230792', '桃山林业局': '230793', '郎乡林业局': '230794', '佳木斯市': '230800',
           '前进区': '230804', '东风区': '420306', '桦南县': '230822', '桦川县': '230826', '汤原县': '230828', '抚远县': '230833',
           '同江市': '230881', '富锦市': '230882', '七台河市': '230900', '新兴区': '230902', '桃山区': '230903', '茄子河区': '230904',
           '勃利县': '230921', '牡丹江市': '231000', '东安区': '231002', '阳明区': '231003', '爱民区': '231004', '东宁县': '231024',
           '林口县': '231025', '绥芬河市': '231081', '海林市': '231083', '宁安市': '231084', '穆棱市': '231085', '黑河市': '231100',
           '爱辉区': '231102', '嫩江县': '231121', '逊克县': '231123', '孙吴县': '231124', '北安市': '231181', '五大连池': '231182',
           '五大连池风景区': '231183', '绥化市': '231200', '北林区': '231202', '望奎县': '231221', '兰西县': '231222', '青冈县': '231223',
           '庆安县': '231224', '明水县': '231225', '绥棱县': '231226', '安达市': '231281', '肇东市': '231282', '海伦市': '231283',
           '大兴安岭地区': '232700', '加格达奇区': '232701', '松岭区': '232702', '新林区': '232703', '呼中区': '232704',
           '大兴安岭地区本级': '232705', '呼玛县': '232721', '塔河县': '232722', '漠河县': '232723', '牡丹江林管局': '233100',
           '穆棱林业局': '233102', '大海林林业局': '233103', '海林林业局': '233104', '柴河林业局': '233105', '东京城林业局': '233106',
           '林口林业局': '233107', '绥阳林业局': '233108', '八面通林业局': '233109', '松花江林管局': '233200', '山河屯林业局': '233202',
           '通北林业局': '233203', '兴隆林业局': '233204', '苇河林业局': '233205', '亚布力林业局': '233206', '方正林业局': '233207',
           '沾河林业局': '233208', '绥棱林业局': '233209', '合江林管局': '233400', '双鸭山林业局': '233402', '鹤立林业局': '233403',
           '桦南林业局': '233404', '鹤北林业局': '233405', '东方红林业局': '233406', '迎春林业局': '233407', '清河林业局': '233408',
           '黑龙江省农垦总局': '235100', '黑龙江省农垦总局延军农场': '235101', '黑龙江省农垦总局梧桐河农场': '235102', '黑龙江省农垦总局双鸭山农场': '235103',
           '黑龙江省农垦总局前哨农场': '235104', '黑龙江省农垦总局前锋农场': '235105', '黑龙江省农垦总局鸭绿河农场': '235106', '黑龙江省农垦总局海伦农场': '235107',
           '黑龙江省农垦总局红旗农场': '235108', '黑龙江省农垦总局引龙河农场': '235109', '黑龙江省农垦总局长水河农场': '235110', '黑龙江省农垦总局建设农场': '235111',
           '黑龙江省农垦总局锦河农场': '235112', '黑龙江省农垦总局跃进农场': '235113', '黑龙江省农垦总局泰来农场': '235114', '黑龙江省农垦总局富裕牧场': '235115',
           '黑龙江省农垦总局五九七农场': '235116', '黑龙江省农垦总局红五月农场': '235117', '黑龙江省农垦总局建边农场': '235118', '黑龙江省农垦总局和平牧场': '235119',
           '黑龙江省农垦总局岔林河农场': '235120', '黑龙江省农垦总局八五一零农场': '235121', '黑龙江省农垦总局红色边疆农场': '235122', '黑龙江省农垦总局龙镇农场': '235123',
           '黑龙江省农垦总局襄河农场': '235124', '黑龙江省农垦总局逊克农场': '235125', '黑龙江省农垦总局鹤山农场': '235126', '黑龙江省农垦总局嫩江农场': '235127',
           '黑龙江省农垦总局宝泉岭农场': '235128', '黑龙江省农垦总局二九零农场': '235129', '黑龙江省农垦总局新华农场': '235130', '黑龙江省农垦总局军川农场': '235131',
           '黑龙江省农垦总局共青农场': '235132', '黑龙江省农垦总局绥滨农场': '235133', '黑龙江省农垦总局江滨农场\u3000': '235134', '黑龙江省农垦总局普阳农场': '235135',
           '黑龙江省农垦总局名山农场': '235136', '黑龙江省农垦总局汤原农场': '235137', '黑龙江省农垦总局依兰农场': '235138', '黑龙江省农垦总局八五二农场': '235139',
           '黑龙江省农垦总局八五三农场': '235140', '黑龙江省农垦总局饶河农场': '235141', '黑龙江省农垦总局宝山农场': '235142', '黑龙江省农垦总局北兴农场': '235143',
           '黑龙江省农垦总局老柞山金矿': '235144', '黑龙江省农垦总局红旗岭农场': '235145', '黑龙江省农垦总局江川农场': '235146', '黑龙江省农垦总局曙光农场': '235147',
           '黑龙江省农垦总局二九一农场': '235148', '黑龙江省农垦总局七星农场': '235149', '黑龙江省农垦总局八五九农场': '235150', '黑龙江省农垦总局创业农场': '235151',
           '黑龙江省农垦总局大兴农场': '235152', '黑龙江省农垦总局二道河农场': '235153', '黑龙江省农垦总局浓江农场': '235154', '黑龙江省农垦总局红卫农场': '235155',
           '黑龙江省农垦总局洪河农场': '235156', '黑龙江省农垦总局青龙山农场': '235157', '黑龙江省农垦总局前进农场\u3000': '235158',
           '黑龙江省农垦总局勤得利农场\u3000': '235159', '黑龙江省农垦总局胜利农场': '235160', '黑龙江省农垦总局八五零农场\u3000': '235161',
           '黑龙江省农垦总局八五四农场': '235162', '黑龙江省农垦总局八五五农场': '235163', '黑龙江省农垦总局八五六农场': '235164', '黑龙江省农垦总局八五七农场': '235165',
           '黑龙江省农垦总局八五八农场': '235166', '黑龙江省农垦总局八五一一农场': '235167', '黑龙江省农垦总局庆丰农场': '235168', '黑龙江省农垦总局云山农场': '235169',
           '黑龙江省农垦总局兴凯湖农场': '235170', '黑龙江省农垦总局海林农场': '235171', '黑龙江省农垦总局宁安农场': '235172', '黑龙江省农垦总局龙门农场': '235173',
           '黑龙江省农垦总局二龙山农场': '235174', '黑龙江省农垦总局尾山农场': '235175', '黑龙江省农垦总局格球山农场\u3000': '235176',
           '黑龙江省农垦总局赵光农场': '235177', '黑龙江省农垦总局红星农场': '235178', '黑龙江省农垦总局大西江农场': '235179', '黑龙江省农垦总局尖山农场': '235180',
           '黑龙江省农垦总局山河农场': '235181', '黑龙江省农垦总局嫩北农场': '235182', '黑龙江省农垦总局哈拉海农场': '235183', '黑龙江省农垦总局七星泡农场': '235184',
           '黑龙江省农垦总局荣军农场': '235185', '黑龙江省农垦总局查哈阳农场': '235186', '黑龙江省农垦总局克山农场\u3000': '235187',
           '黑龙江省农垦总局绿色草原牧场': '235188', '黑龙江省农垦总局依安农场': '235189', '黑龙江省农垦总局巨浪牧场\u3000': '235190',
           '黑龙江省农垦总局铁力农场': '235191', '黑龙江省农垦总局嘉荫农场': '235192', '黑龙江省农垦总局安达畜牧场': '235193', '黑龙江省农垦总局肇源农场': '235194',
           '黑龙江省农垦总局红光农场': '235195', '黑龙江省农垦总局绥棱农场': '235196', '黑龙江省农垦总局柳河农场\u3000': '235197',
           '黑龙江省农垦总局香坊实验农场': '235198', '黑龙江省农垦总局闫家岗农场': '235199', '黑龙江省农垦总局庆阳农场': '2351A1', '黑龙江省农垦总局沙河农场': '2351A2',
           '黑龙江省农垦总局青年农场': '2351A3', '黑龙江省农垦总局四方山农场': '2351A4', '黑龙江省农垦总局松花江农场': '2351A5', '黑龙江省农垦总局小岭水泥厂': '2351A6',
           '黑龙江省农垦总局浩良河化肥厂': '2351A7', '黑龙江省农垦总局局直': '2351A8', '黑龙江省农垦总局宝泉岭分局局直': '2351A9', '黑龙江省农垦总局红兴隆分局局直': '2351B1',
           '黑龙江省农垦总局建三江分局局直': '2351B2', '黑龙江省农垦总局牡丹江分局局直': '2351B3', '黑龙江省农垦总局北安分局局直': '2351B4',
           '黑龙江省农垦总局九三分局局直': '2351B5', '黑龙江省农垦总局齐齐哈尔分局局直': '2351B6', '黑龙江省农垦总局绥化分局局直': '2351B7',
           '黑龙江省农垦总局哈尔滨分局局直': '2351B8', '上海市': '310000', '黄浦区': '310101', '卢湾区': '310103', '徐汇区': '310104',
           '长宁区': '310105', '静安区': '310106', '普陀区': '330903', '闸北区': '310108', '虹口区': '310109', '杨浦区': '310110',
           '闵行区': '310112', '嘉定区': '310114', '浦东新区': '310115', '金山区': '310116', '松江区': '310117', '青浦区': '310118',
           '南汇区': '310119', '奉贤区': '310120', '崇明县': '310230', '江苏省': '320000', '南京市': '320100', '玄武区': '320102',
           '白下区': '320103', '秦淮区': '320104', '建邺区': '320105', '鼓楼区': '410204', '下关区': '320107', '浦口区': '320111',
           '栖霞区': '320113', '雨花台区': '320114', '江宁区': '320115', '六合区': '320116', '溧水县': '320124', '高淳县': '320125',
           '无锡市': '320200', '崇安区': '320202', '南长区': '320203', '北塘区': '320204', '锡山区': '320205', '惠山区': '320206',
           '滨湖区': '320211', '无锡市新区': '320233', '江阴市': '320281', '宜兴市': '320282', '徐州市': '320300', '云龙区': '320303',
           '九里区': '320304', '贾汪区': '320305', '徐州市经济开发区': '320307', '泉山区': '320311', '丰县': '320321', '沛县': '320322',
           '铜山县': '320323', '睢宁县': '320324', '新沂市': '320381', '邳州市': '320382', '常州市': '320400', '天宁区': '320402',
           '钟楼区': '320404', '戚墅堰区': '320405', '新北区': '320411', '武进区': '320412', '溧阳市': '320481', '金坛市': '320482',
           '苏州市': '320500', '沧浪区': '320502', '平江区': '320503', '金阊区': '320504', '虎丘区': '320505', '吴中区': '320506',
           '相城区': '320507', '苏州市工业园区': '320508', '常熟市': '320581', '张家港市': '320582', '昆山市': '320583', '吴江市': '320584',
           '太仓市': '320585', '南通市': '320600', '崇川区': '320602', '港闸区': '320611', '南通市开发区': '320618', '海安县': '320621',
           '如东县': '320623', '启东市': '320681', '如皋市': '320682', '通州市': '320683', '海门市': '320684', '连云港市': '320700',
           '连云区': '320703', '新浦区': '320705', '连云港市开发区': '320707', '赣榆县': '320721', '东海县': '320722', '灌云县': '320723',
           '灌南县': '320724', '淮安市': '320800', '楚州区': '320803', '淮阴区': '320804', '淮安市开发区': '320805', '清浦区': '320811',
           '涟水县': '320826', '洪泽县': '320829', '盱眙县': '320830', '金湖县': '320831', '盐城市': '320900', '亭湖区': '320902',
           '盐都区': '320903', '响水县': '320921', '滨海县': '320922', '阜宁县': '320923', '射阳县': '320924', '建湖县': '320925',
           '东台市': '320981', '大丰市': '320982', '扬州市': '321000', '广陵区': '321002', '邗江区': '321003', '维扬区': '321011',
           '宝应县': '321023', '仪征市': '321081', '高邮市': '321084', '江都市': '321088', '镇江市': '321100', '京口区': '321102',
           '镇江市新区': '321103', '润州区': '321111', '丹徒区': '321112', '丹阳市': '321181', '扬中市': '321182', '句容市': '321183',
           '泰州市': '321200', '海陵区': '321202', '高港区': '321203', '市直': '321205', '兴化市': '321281', '靖江市': '321282',
           '泰兴市': '321283', '姜堰市': '321284', '宿迁市': '321300', '宿城区': '321302', '宿豫区': '321311', '沭阳县': '321322',
           '泗阳县': '321323', '泗洪县': '321324', '浙江省': '330000', '杭州市': '330100', '上城区': '330102', '下城区': '330103',
           '江干区': '330104', '拱墅区': '330105', '西湖区': '360103', '滨江区': '330108', '萧山区': '330109', '余杭区': '330110',
           '桐庐县': '330122', '淳安县': '330127', '建德市': '330182', '富阳市': '330183', '临安市': '330185', '宁波市': '330200',
           '海曙区': '330203', '江东区': '330204', '江北区': '500105', '北仑区': '330206', '镇海区': '330211', '鄞州区': '330212',
           '象山县': '330225', '宁海县': '330226', '余姚市': '330281', '慈溪市': '330282', '奉化市': '330283', '温州市': '330300',
           '鹿城区': '330302', '龙湾区': '330303', '瓯海区': '330304', '洞头县': '330322', '永嘉县': '330324', '平阳县': '330326',
           '苍南县': '330327', '文成县': '330328', '泰顺县': '330329', '瑞安市': '330381', '乐清市': '330382', '嘉兴市': '330400',
           '南湖区': '330402', '秀洲区': '330411', '嘉善县': '330421', '海盐县': '330424', '海宁市': '330481', '平湖市': '330482',
           '桐乡市': '330483', '湖州市': '330500', '吴兴区': '330502', '南浔区': '330503', '德清县': '330521', '长兴县': '330522',
           '安吉县': '330523', '绍兴市': '330600', '越城区': '330602', '绍兴县': '330621', '新昌县': '330624', '诸暨市': '330681',
           '上虞市': '330682', '嵊州市': '330683', '金华市': '330700', '婺城区': '330702', '金东区': '330703', '武义县': '330723',
           '浦江县': '330726', '磐安县': '330727', '兰溪市': '330781', '义乌市': '330782', '东阳市': '330783', '永康市': '330784',
           '衢州市': '330800', '柯城区': '330802', '衢江区': '330803', '常山县': '330822', '开化县': '330824', '龙游县': '330825',
           '江山市': '330881', '舟山市': '330900', '定海区': '330902', '岱山县': '330921', '嵊泗县': '330922', '台州市': '331000',
           '椒江区': '331002', '黄岩区': '331003', '路桥区': '331004', '玉环县': '331021', '三门县': '331022', '天台县': '331023',
           '仙居县': '331024', '温岭市': '331081', '临海市': '331082', '丽水市': '331100', '莲都区': '331102', '青田县': '331121',
           '缙云县': '331122', '遂昌县': '331123', '松阳县': '331124', '云和县': '331125', '庆元县': '331126', '景宁畲族自治县': '331127',
           '龙泉市': '331181', '安徽省': '340000', '合肥市': '340100', '瑶海区': '340102', '庐阳区': '340103', '蜀山区': '340104',
           '包河区': '340111', '长丰县': '340121', '肥东县': '340122', '肥西县': '340123', '芜湖市': '340200', '镜湖区': '340202',
           '弋江区': '340203', '鸠江区': '340207', '三山区': '340208', '芜湖县': '340221', '繁昌县': '340222', '南陵县': '340223',
           '蚌埠市': '340300', '龙子湖区': '340302', '蚌山区': '340303', '禹会区': '340304', '淮上区': '340311', '怀远县': '340321',
           '五河县': '340322', '固镇县': '340323', '淮南市': '340400', '大通区': '340402', '田家庵区': '340403', '谢家集区': '340404',
           '八公山区': '340405', '潘集区': '340406', '凤台县': '340421', '毛集实验区': '340481', '马鞍山市': '340500', '金家庄区': '340502',
           '花山区': '340503', '雨山区': '340504', '当涂县': '340521', '淮北市': '340600', '杜集区': '340602', '相山区': '340603',
           '烈山区': '340604', '濉溪县': '340621', '铜陵市': '340700', '铜官山区': '340702', '狮子山区': '340703', '铜陵县': '340721',
           '安庆市': '340800', '迎江区': '340802', '大观区': '340803', '宜秀区': '340811', '怀宁县': '340822', '枞阳县': '340823',
           '潜山县': '340824', '太湖县': '340825', '宿松县': '340826', '望江县': '340827', '岳西县': '340828', '桐城市': '340881',
           '黄山市': '341000', '屯溪区': '341002', '黄山区': '341003', '徽州区': '341004', '歙县': '341021', '休宁县': '341022',
           '黟县': '341023', '祁门县': '341024', '滁州市': '341100', '琅琊区': '341102', '南谯区': '341103', '来安县': '341122',
           '全椒县': '341124', '定远县': '341125', '凤阳县': '341126', '天长市': '341181', '明光市': '341182', '阜阳市': '341200',
           '颍州区': '341202', '颍东区': '341203', '颍泉区': '341204', '临泉县': '341221', '太和县': '341222', '阜南县': '341225',
           '颍上县': '341226', '界首市': '341282', '宿州市': '341300', '埇桥区': '341302', '砀山县': '341321', '萧县': '341322',
           '灵璧县': '341323', '泗县': '341324', '巢湖市': '341402', '庐江县': '341421', '无为县': '341422', '含山县': '341423',
           '和县': '341424', '六安市': '341500', '金安区': '341502', '裕安区': '341503', '寿县': '341521', '霍邱县': '341522',
           '舒城县': '341523', '金寨县': '341524', '霍山县': '341525', '叶集区': '341581', '亳州市': '341600', '谯城区': '341602',
           '涡阳县': '341621', '蒙城县': '341622', '利辛县': '341623', '池州市': '341700', '贵池区': '341702', '东至县': '341721',
           '石台县': '341722', '青阳县': '341723', '九华山风景区': '341781', '宣城市': '341800', '宣州区': '341802', '郎溪县': '341821',
           '广德县': '341822', '泾县': '341823', '绩溪县': '341824', '旌德县': '341825', '宁国市': '341881', '福建省': '350000',
           '福建省直属': '350001', '福州市': '350100', '台江区': '350103', '仓山区': '350104', '马尾区': '350105', '琅岐开发区': '350106',
           '晋安区': '350111', '闽侯县': '350121', '连江县': '350122', '罗源县': '350123', '闽清县': '350124', '永泰县': '350125',
           '平潭综合实验区': '350128', '福清市': '350181', '长乐市': '350182', '厦门市': '350200', '思明区': '350203', '海沧区': '350205',
           '湖里区': '350206', '集美区': '350211', '同安区': '350212', '翔安区': '350213', '莆田市': '350300', '城厢区': '350302',
           '涵江区': '350303', '荔城区': '350304', '秀屿区': '350305', '湄州岛': '350306', '北岸': '350307', '仙游县': '350322',
           '三明市': '350400', '梅列区': '350402', '三元区': '350403', '明溪县': '350421', '清流县': '350423', '宁化县': '350424',
           '大田县': '350425', '尤溪县': '350426', '沙县': '350427', '将乐县': '350428', '泰宁县': '350429', '建宁县': '350430',
           '永安市': '350481', '泉州市': '350500', '鲤城区': '350502', '丰泽区': '350503', '洛江区': '350504', '泉港区': '350505',
           '惠安县': '350521', '安溪县': '350524', '永春县': '350525', '德化县': '350526', '金门县': '350527', '石狮市': '350581',
           '晋江市': '350582', '南安市': '350583', '漳州市': '350600', '芗城区': '350602', '龙文区': '350603', '云霄县': '350622',
           '漳浦县': '350623', '诏安县': '350624', '长泰县': '350625', '东山县': '350626', '南靖县': '350627', '平和县': '350628',
           '华安县': '350629', '龙海市': '350681', '常山开发区': '350682', '南平市': '350700', '延平区': '350702', '顺昌县': '350721',
           '浦城县': '350722', '光泽县': '350723', '松溪县': '350724', '政和县': '350725', '邵武市': '350781', '武夷山市': '350782',
           '建瓯市': '350783', '建阳市': '350784', '龙岩市': '350800', '新罗区': '350802', '长汀县': '350821', '永定县': '350822',
           '上杭县': '350823', '武平县': '350824', '连城县': '350825', '漳平市': '350881', '宁德市': '350900', '蕉城区': '350902',
           '霞浦县': '350921', '古田县': '350922', '屏南县': '350923', '寿宁县': '350924', '周宁县': '350925', '柘荣县': '350926',
           '福安市': '350981', '福鼎市': '350982', '江西省': '360000', '南昌市': '360100', '东湖区': '360102', '青云谱区': '360104',
           '湾里区': '360105', '南昌经济技术开发区': '360106', '红谷滩新区': '360108', '南昌高新区': '360109', '青山湖区': '360111',
           '南昌县': '360121', '新建县': '360122', '安义县': '360123', '进贤县': '360124', '厂办学校': '360125', '英雄开发区': '360132',
           '桑海经济技术开发区': '360142', '景德镇市': '360200', '昌江区': '360202', '珠山区': '360203', '陶瓷工业园区': '360204',
           '景德镇市高新区': '360205', '浮梁县': '360222', '乐平市': '360281', '萍乡市': '360300', '安源区': '360302', '萍乡市开发区': '360303',
           '湘东区': '360313', '莲花县': '360321', '上栗县': '360322', '芦溪县': '360323', '九江市': '360400', '庐山区': '360402',
           '浔阳区': '360403', '九江经济开发区': '360404', '九江县': '360421', '庐山管理局': '360422', '武宁县': '360423', '修水县': '360424',
           '永修县': '360425', '德安县': '360426', '星子县': '360427', '都昌县': '360428', '湖口县': '360429', '彭泽县': '360430',
           '瑞昌市': '360481', '共青城': '360491', '新余市': '360500', '渝水区': '360502', '仙女湖区': '360503', '新余经济开发区': '360505',
           '分宜县': '360521', '鹰潭市': '360600', '月湖区': '360602', '鹰潭经济技术开发区': '360603', '余江县': '360622',
           '龙虎风景旅游区': '360623', '贵溪市': '360681', '赣州市': '360700', '章贡区': '360702', '赣州经济技术开发区': '360703',
           '赣县': '360721', '信丰县': '360722', '大余县': '360723', '上犹县': '360724', '崇义县': '360725', '安远县': '360726',
           '龙南县': '360727', '定南县': '360728', '全南县': '360729', '宁都县': '360730', '于都县': '360731', '兴国县': '360732',
           '会昌县': '360733', '寻乌县': '360734', '石城县': '360735', '瑞金市': '360781', '南康市': '360782', '吉安市': '360800',
           '吉州区': '360802', '青原区': '360803', '吉安县': '360821', '吉水县': '360822', '峡江县': '360823', '新干县': '360824',
           '永丰县': '360825', '泰和县': '360826', '遂川县': '360827', '万安县': '360828', '安福县': '360829', '永新县': '360830',
           '井冈山市': '360881', '宜春市': '360900', '袁州区': '360902', '奉新县': '360921', '万载县': '360922', '上高县': '360923',
           '宜丰县': '360924', '靖安县': '360925', '铜鼓县': '360926', '丰城市': '360981', '樟树市': '360982', '高安市': '360983',
           '抚州市': '361000', '临川区': '361002', '抚州金巢经济开发区': '361003', '南城县': '361021', '黎川县': '361022', '南丰县': '361023',
           '崇仁县': '361024', '乐安县': '361025', '宜黄县': '361026', '金溪县': '361027', '资溪县': '361028', '东乡县': '361029',
           '广昌县': '361030', '上饶市': '361100', '信州区': '361102', '三管会': '361103', '上饶市经济开发区': '361104', '上饶县': '361121',
           '广丰县': '361122', '玉山县': '361123', '铅山县': '361124', '横峰县': '361125', '弋阳县': '361126', '余干县': '361127',
           '鄱阳县': '361128', '万年县': '361129', '婺源县': '361130', '德兴市': '361181', '山东省': '370000', '山东省直属': '370001',
           '济南市': '370100', '历下区': '370102', '市中区': '511102', '槐荫区': '370104', '天桥区': '370105', '济南市高新区': '370106',
           '历城区': '370112', '长清区': '370113', '平阴县': '370124', '济阳县': '370125', '商河县': '370126', '章丘市': '370181',
           '青岛市': '370200', '市南区': '370202', '市北区': '370203', '四方区': '370205', '黄岛区': '370211', '崂山区': '370212',
           '李沧区': '370213', '城阳区': '370214', '胶州市': '370281', '即墨市': '370282', '平度市': '370283', '胶南市': '370284',
           '莱西市': '370285', '淄博市': '370300', '淄川区': '370302', '张店区': '370303', '博山区': '370304', '临淄区': '370305',
           '周村区': '370306', '淄博市高新区': '370307', '桓台县': '370321', '高青县': '370322', '沂源县': '370323', '枣庄市': '370400',
           '薛城区': '370403', '峄城区': '370404', '台儿庄区': '370405', '山亭区': '370406', '枣庄市高新开发区': '370407', '滕州市': '370481',
           '东营市': '370500', '东营区': '370502', '河口区': '370503', '胜利石油教管中心': '370505', '垦利县': '370521', '利津县': '370522',
           '广饶县': '370523', '烟台市': '370600', '芝罘区': '370602', '烟台市开发区': '370603', '烟强市高新区': '370604', '福山区': '370611',
           '牟平区': '370612', '莱山区': '370613', '长岛县': '370634', '龙口市': '370681', '莱阳市': '370682', '莱州市': '370683',
           '蓬莱市': '370684', '招远市': '370685', '栖霞市': '370686', '海阳市': '370687', '潍坊市': '370700', '潍城区': '370702',
           '寒亭区': '370703', '坊子区': '370704', '奎文区': '370705', '潍坊市高新区': '370706', '潍坊市滨海区': '370707',
           '潍坊市经济区': '370708', '潍坊市峡山区': '370709', '临朐县': '370724', '昌乐县': '370725', '青州市': '370781', '诸城市': '370782',
           '寿光市': '370783', '安丘市': '370784', '高密市': '370785', '昌邑市': '370786', '济宁市': '370800', '济宁市高新区': '370803',
           '济宁市北湖区': '370804', '任城区': '370811', '微山县': '370826', '鱼台县': '370827', '金乡县': '370828', '嘉祥县': '370829',
           '汶上县': '370830', '泗水县': '370831', '梁山县': '370832', '曲阜市': '370881', '兖州市': '370882', '邹城市': '370883',
           '泰安市': '370900', '泰山区': '370902', '泰安市高新区': '370904', '泰安市泰山管委': '370905', '岱岳区': '370911', '宁阳县': '370921',
           '东平县': '370923', '新泰市': '370982', '肥城市': '370983', '威海市': '371000', '环翠区': '371002', '威海市高新开发区': '371003',
           '威海市经济开发区': '371004', '威海市工业新区': '371005', '文登市': '371081', '荣成市': '371082', '乳山市': '371083',
           '日照市': '371100', '东港区': '371102', '岚山区': '371103', '日照市开发区': '371104', '五莲县': '371121', '莒县': '371122',
           '莱芜市': '371200', '莱城区': '371202', '钢城区': '371203', '莱芜市高新开发区': '371204', '莱芜市泰钢工业园': '371205',
           '莱芜市雪野旅游区': '371206', '临沂市': '371300', '兰山区': '371302', '临沂市高新开发区': '371303', '临沂市经济开发区': '371304',
           '临沂市临港产业区': '371305', '罗庄区': '371311', '沂南县': '371321', '郯城县': '371322', '沂水县': '371323', '苍山县': '371324',
           '费县': '371325', '平邑县': '371326', '莒南县': '371327', '蒙阴县': '371328', '临沭县': '371329', '德州市': '371400',
           '德城区': '371402', '德州市经济开发区': '371403', '德州市运河开发区': '371404', '陵县': '371421', '宁津县': '371422',
           '庆云县': '371423', '临邑县': '371424', '齐河县': '371425', '平原县': '371426', '夏津县': '371427', '武城县': '371428',
           '乐陵市': '371481', '禹城市': '371482', '聊城市': '371500', '东昌府区': '371502', '聊城市开发区': '371503', '阳谷县': '371521',
           '莘县': '371522', '茌平县': '371523', '东阿县': '371524', '冠县': '371525', '高唐县': '371526', '临清市': '371581',
           '滨州市': '371600', '滨城区': '371602', '滨州市开发区': '371604', '惠民县': '371621', '阳信县': '371622', '无棣县': '371623',
           '沾化县': '371624', '博兴县': '371625', '邹平县': '371626', '菏泽市': '371700', '牡丹区': '371702', '菏泽市开发区': '371703',
           '曹县': '371721', '单县': '371722', '成武县': '371723', '巨野县': '371724', '郓城县': '371725', '鄄城县': '371726',
           '定陶县': '371727', '东明县': '371728', '河南省': '410000', '郑州市': '410100', '中原区': '410102', '二七区': '410103',
           '管城回族区': '410104', '金水区': '410105', '上街区': '410106', '惠济区': '410108', '郑州市高新技术开发区': '410109',
           '中牟县': '410122', '巩义市': '410181', '荥阳市': '410182', '新密市': '410183', '新郑市': '410184', '登封市': '410185',
           '开封市': '410200', '龙亭区': '410202', '顺河回族区': '410203', '禹王台区': '410205', '金明区': '410211', '开封市开发区': '410212',
           '杞县': '410221', '通许县': '410222', '尉氏县': '410223', '开封县': '410224', '兰考县': '410225', '洛阳市': '410300',
           '老城区': '410302', '西工区': '410303', '瀍河回族区': '410304', '涧西区': '410305', '吉利区': '410306', '洛龙区': '410311',
           '孟津县': '410322', '新安县': '410323', '栾川县': '410324', '嵩县': '410325', '汝阳县': '410326', '宜阳县': '410327',
           '洛宁县': '410328', '伊川县': '410329', '高新技术产业开发区': '410331', '龙门文化旅游园区': '410332', '伊洛工业园区': '410333',
           '偃师市': '410381', '平顶山市': '410400', '卫东区': '410403', '石龙区': '410404', '湛河区': '410411', '宝丰县': '410421',
           '叶县': '410422', '鲁山县': '410423', '郏县': '410425', '舞钢市': '410481', '汝州市': '410482', '安阳市': '410500',
           '文峰区': '410502', '北关区': '410503', '殷都区': '410505', '龙安区': '410506', '安阳县': '410522', '汤阴县': '410523',
           '滑县': '410526', '内黄县': '410527', '林州市': '410581', '鹤壁市': '410600', '鹤山区': '410602', '山城区': '410603',
           '淇滨区': '410611', '浚县': '410621', '淇县': '410622', '新乡市': '410700', '红旗区': '410702', '卫滨区': '410703',
           '凤泉区': '410704', '牧野区': '410711', '新乡县': '410721', '获嘉县': '410724', '原阳县': '410725', '延津县': '410726',
           '封丘县': '410727', '长垣县': '410728', '卫辉市': '410781', '辉县市': '410782', '焦作市': '410800', '解放区': '410802',
           '中站区': '410803', '马村区': '410804', '焦作市高新区': '410806', '山阳区': '410811', '修武县': '410821', '博爱县': '410822',
           '武陟县': '410823', '温县': '410825', '济源市': '419001', '沁阳市': '410882', '孟州市': '410883', '濮阳市': '410900',
           '华龙区': '410902', '濮阳市高新区': '410903', '清丰县': '410922', '南乐县': '410923', '范县': '410926', '台前县': '410927',
           '濮阳县': '410928', '许昌市': '411000', '魏都区': '411002', '许昌县': '411023', '鄢陵县': '411024', '襄城县': '411025',
           '禹州市': '411081', '长葛市': '411082', '漯河市': '411100', '源汇区': '411102', '郾城区': '411103', '召陵区': '411104',
           '舞阳县': '411121', '临颍县': '411122', '三门峡市': '411200', '湖滨区': '411202', '渑池县': '411221', '陕县': '411222',
           '卢氏县': '411224', '义马市': '411281', '灵宝市': '411282', '南阳市': '411300', '宛城区': '411302', '卧龙区': '411303',
           '南召县': '411321', '方城县': '411322', '西峡县': '411323', '镇平县': '411324', '内乡县': '411325', '淅川县': '411326',
           '社旗县': '411327', '唐河县': '411328', '新野县': '411329', '桐柏县': '411330', '邓州市': '411381', '商丘市': '411400',
           '梁园区': '411402', '睢阳区': '411403', '经济技术开发区': '421183', '民权县': '411421', '睢县': '411422', '宁陵县': '411423',
           '柘城县': '411424', '虞城县': '411425', '夏邑县': '411426', '永城市': '411481', '信阳市': '411500', '浉河区': '411502',
           '平桥区': '411503', '南湾管理区': '411511', '鸡公山管理区': '411512', '信阳市工业城': '411513', '上天梯管理区': '411514',
           '羊山新区': '411515', '罗山县': '411521', '光山县': '411522', '新县': '411523', '商城县': '411524', '固始县': '411525',
           '潢川县': '411526', '淮滨县': '411527', '息县': '411528', '周口市': '411600', '川汇区': '411602', '扶沟县': '411621',
           '西华县': '411622', '商水县': '411623', '沈丘县': '411624', '郸城县': '411625', '淮阳县': '411626', '太康县': '411627',
           '鹿邑县': '411628', '项城市': '411681', '驻马店市': '411700', '驿城区': '411702', '西平县': '411721', '上蔡县': '411722',
           '平舆县': '411723', '正阳县': '411724', '确山县': '411725', '泌阳县': '411726', '汝南县': '411727', '遂平县': '411728',
           '新蔡县': '411729', '省直辖县级行政区划': '469000', '湖北省': '420000', '武汉市': '420100', '江岸区': '420102', '江汉区': '420103',
           '硚口区': '420104', '汉阳区': '420105', '武昌区': '420106', '武汉市经济技术开发区': '420108', '武汉市东湖新技术开发区': '420109',
           '洪山区': '420111', '东西湖区': '420112', '汉南区': '420113', '蔡甸区': '420114', '江夏区': '420115', '黄陂区': '420116',
           '新洲区': '420117', '黄石市': '420200', '黄石港区': '420202', '西塞山区': '420203', '下陆区': '420204', '铁山区': '420205',
           '阳新县': '420222', '大冶市': '420281', '十堰市': '420300', '茅箭区': '420302', '张湾区': '420303', '十堰经济开发区': '420304',
           '武当山': '420305', '郧县': '420321', '郧西县': '420322', '竹山县': '420323', '竹溪县': '420324', '房县': '420325',
           '丹江口市': '420381', '宜昌市': '420500', '西陵区': '420502', '伍家岗区': '420503', '点军区': '420504', '猇亭区': '420505',
           '夷陵区': '420506', '远安县': '420525', '兴山县': '420526', '秭归县': '420527', '长阳土家族自治县': '420528',
           '五峰土家族自治县': '420529', '宜都市': '420581', '当阳市': '420582', '枝江市': '420583', '襄樊市': '420600', '襄城区': '420602',
           '高新区': '441227', '樊城区': '420606', '襄阳区': '420607', '南漳县': '420624', '谷城县': '420625', '保康县': '420626',
           '老河口市': '420682', '枣阳市': '420683', '宜城市': '420684', '鄂州市': '420700', '梁子湖区': '420702', '华容区': '420703',
           '鄂城区': '420704', '荆门市': '420800', '东宝区': '420802', '荆门屈家岭管理区': '420803', '掇刀区': '420804', '京山县': '420821',
           '沙洋县': '420822', '钟祥市': '420881', '孝感市': '420900', '孝南区': '420902', '孝昌县': '420921', '大悟县': '420922',
           '云梦县': '420923', '应城市': '420981', '安陆市': '420982', '汉川市': '420984', '双峰山旅游度假区': '420985',
           '高新技术开发区': '420986', '荆州市': '421000', '沙市区': '421002', '荆州区': '421003', '荆州开发区': '421004', '公安县': '421022',
           '监利县': '421023', '江陵县': '421024', '沙洋监狱管理局': '421025', '石首市': '421081', '洪湖市': '421083', '松滋市': '421087',
           '黄冈市': '421100', '黄州区': '421102', '团风县': '421121', '红安县': '421122', '罗田县': '421123', '英山县': '421124',
           '浠水县': '421125', '蕲春县': '421126', '黄梅县': '421127', '龙感湖管理区': '421129', '麻城市': '421181', '武穴市': '421182',
           '咸宁市': '421200', '咸安区': '421202', '嘉鱼县': '421221', '通城县': '421222', '崇阳县': '421223', '通山县': '421224',
           '赤壁市': '421281', '随州市': '421300', '曾都区': '421302', '随县': '421321', '广水市': '421381', '恩施土家族苗族自治州': '422800',
           '恩施市': '422801', '利川市': '422802', '建始县': '422822', '巴东县': '422823', '宣恩县': '422825', '咸丰县': '422826',
           '来凤县': '422827', '鹤峰县': '422828', '恩施州州直': '422891', '仙桃市': '429004', '潜江市': '429005', '天门市': '429006',
           '神农架林区': '429021', '江汉油田': '429022', '湖南省': '430000', '长沙市': '430100', '芙蓉区': '430102', '天心区': '430103',
           '岳麓区': '430104', '开福区': '430105', '雨花区': '430111', '长沙县': '430121', '望城县': '430122', '宁乡县': '430124',
           '浏阳市': '430181', '株洲市': '430200', '荷塘区': '430202', '芦淞区': '430203', '石峰区': '430204', '天元区': '430211',
           '株洲县': '430221', '攸县': '430223', '茶陵县': '430224', '炎陵县': '430225', '醴陵市': '430281', '湘潭市': '430300',
           '雨湖区': '430302', '岳塘区': '430304', '湘潭县': '430321', '湘乡市': '430381', '韶山市': '430382', '衡阳市': '430400',
           '珠晖区': '430405', '雁峰区': '430406', '石鼓区': '430407', '蒸湘区': '430408', '南岳区': '430412', '衡阳县': '430421',
           '衡南县': '430422', '衡山县': '430423', '衡东县': '430424', '祁东县': '430426', '耒阳市': '430481', '常宁市': '430482',
           '邵阳市': '430500', '双清区': '430502', '大祥区': '430503', '北塔区': '430511', '邵东县': '430521', '新邵县': '430522',
           '邵阳县': '430523', '隆回县': '430524', '洞口县': '430525', '绥宁县': '430527', '新宁县': '430528', '城步苗族自治县': '430529',
           '武冈市': '430581', '岳阳市': '430600', '岳阳楼区': '430602', '云溪区': '430603', '君山区': '430611', '岳阳县': '430621',
           '华容县': '430623', '湘阴县': '430624', '平江县': '430626', '汨罗市': '430681', '临湘市': '430682', '常德市': '430700',
           '武陵区': '430702', '鼎城区': '430703', '安乡县': '430721', '汉寿县': '430722', '澧县': '430723', '临澧县': '430724',
           '桃源县': '430725', '石门县': '430726', '津市市': '430781', '张家界市': '430800', '永定区': '430802', '武陵源区': '430811',
           '慈利县': '430821', '桑植县': '430822', '益阳市': '430900', '资阳区': '430902', '赫山区': '430903', '南县': '430921',
           '桃江县': '430922', '安化县': '430923', '沅江市': '430981', '郴州市': '431000', '北湖区': '431002', '苏仙区': '431003',
           '桂阳县': '431021', '宜章县': '431022', '永兴县': '431023', '嘉禾县': '431024', '临武县': '431025', '汝城县': '431026',
           '桂东县': '431027', '安仁县': '431028', '资兴市': '431081', '永州市': '431100', '零陵区': '431102', '冷水滩区': '431103',
           '祁阳县': '431121', '东安县': '431122', '双牌县': '431123', '道县': '431124', '江永县': '431125', '宁远县': '431126',
           '蓝山县': '431127', '新田县': '431128', '江华瑶族自治县': '431129', '怀化市': '431200', '鹤城区': '431202', '中方县': '431221',
           '沅陵县': '431222', '辰溪县': '431223', '溆浦县': '431224', '会同县': '431225', '麻阳苗族自治县': '431226', '新晃侗族自治县': '431227',
           '芷江侗族自治县': '431228', '靖州苗族侗族自治县': '431229', '通道侗族自治县': '431230', '洪江市': '431281', '娄底市': '431300',
           '娄星区': '431302', '双峰县': '431321', '新化县': '431322', '冷水江市': '431381', '涟源市': '431382', '湘西土家族苗族自治州': '433100',
           '吉首市': '433101', '泸溪县': '433122', '凤凰县': '433123', '花垣县': '433124', '保靖县': '433125', '古丈县': '433126',
           '永顺县': '433127', '龙山县': '433130', '广东省': '440000', '广州市': '440100', '荔湾区': '440103', '越秀区': '440104',
           '海珠区': '440105', '天河区': '440106', '白云区': '520113', '黄埔区': '440112', '番禺区': '440113', '花都区': '440114',
           '南沙区': '440115', '萝岗区': '440116', '增城市': '440183', '从化市': '440184', '韶关市': '440200', '武江区': '440203',
           '浈江区': '440204', '曲江区': '440205', '始兴县': '440222', '仁化县': '440224', '翁源县': '440229', '乳源瑶族自治县': '440232',
           '新丰县': '440233', '乐昌市': '440281', '南雄市': '440282', '深圳市': '440300', '深圳市市本级': '440302', '罗湖区': '440303',
           '福田区': '440304', '宝安区': '440306', '龙岗区': '440307', '盐田区': '440308', '光明新区': '440309', '深圳市坪山新区': '440310',
           '珠海市': '440400', '香洲区': '440402', '斗门区': '440403', '金湾区': '440404', '汕头市': '440500', '龙湖区': '440507',
           '金平区': '440511', '濠江区': '440512', '潮阳区': '440513', '潮南区': '440514', '澄海区': '440515', '南澳县': '440523',
           '佛山市': '440600', '禅城区': '440604', '南海区': '440605', '顺德区': '440606', '三水区': '440607', '高明区': '440608',
           '江门市': '440700', '蓬江区': '440703', '江海区': '440704', '新会区': '440705', '台山市': '440781', '开平市': '440783',
           '鹤山市': '440784', '恩平市': '440785', '湛江市': '440800', '赤坎区': '440802', '霞山区': '440803', '坡头区': '440804',
           '东海区': '440805', '麻章区': '440811', '遂溪县': '440823', '徐闻县': '440825', '湛江农垦': '440830', '廉江市': '440881',
           '雷州市': '440882', '吴川市': '440883', '茂名市': '440900', '茂南区': '440902', '茂港区': '440903', '电白县': '440923',
           '高州市': '440981', '化州市': '440982', '信宜市': '440983', '肇庆市': '441200', '端州区': '441202', '鼎湖区': '441203',
           '广宁县': '441223', '怀集县': '441224', '封开县': '441225', '德庆县': '441226', '高要市': '441283', '四会市': '441284',
           '惠州市': '441300', '大亚湾区': '441301', '惠城区': '441302', '惠阳区': '441303', '博罗县': '441322', '惠东县': '441323',
           '龙门县': '441324', '梅州市': '441400', '梅江区': '441402', '梅县': '441421', '大埔县': '441422', '丰顺县': '441423',
           '五华县': '441424', '平远县': '441426', '蕉岭县': '441427', '兴宁市': '441481', '汕尾市': '441500', '红海湾区': '441503',
           '海丰县': '441521', '陆河县': '441523', '陆丰市': '441581', '河源市': '441600', '源城区': '441602', '紫金县': '441621',
           '龙川县': '441622', '连平县': '441623', '和平县': '441624', '东源县': '441625', '阳江市': '441700', '江城区': '441702',
           '海陵岛试验区': '441703', '阳江农垦局': '441705', '阳江高新区': '441706', '阳西县': '441721', '阳东县': '441723', '阳春市': '441781',
           '清远市': '441800', '清城区': '441802', '佛冈县': '441821', '阳山县': '441823', '连山壮族瑶族自治县': '441825',
           '连南瑶族自治县': '441826', '清新县': '441827', '英德市': '441881', '连州市': '441882', '东莞市': '441900', '东莞市辖区': '441901',
           '中山市': '442000', '中山市辖区': '442001', '潮州市': '445100', '湘桥区': '445102', '枫溪区': '445103', '潮安县': '445121',
           '饶平县': '445122', '揭阳市': '445200', '榕城区': '445202', '揭东县': '445221', '揭西县': '445222', '惠来县': '445224',
           '普宁市': '445281', '云浮市': '445300', '云城区': '445302', '新兴县': '445321', '郁南县': '445322', '云安县': '445323',
           '罗定市': '445381', '广西壮族自治区': '450000', '南宁市': '450100', '兴宁区': '450102', '青秀区': '450103', '江南区': '450105',
           '西乡塘区': '450107', '良庆区': '450108', '邕宁区': '450109', '武鸣县': '450122', '隆安县': '450123', '马山县': '450124',
           '上林县': '450125', '宾阳县': '450126', '横县': '450127', '柳州市': '450200', '城中区': '630103', '鱼峰区': '450203',
           '柳南区': '450204', '柳北区': '450205', '柳江县': '450221', '柳城县': '450222', '鹿寨县': '450223', '融安县': '450224',
           '融水苗族自治县': '450225', '三江侗族自治县': '450226', '桂林市': '450300', '秀峰区': '450302', '叠彩区': '450303', '象山区': '450304',
           '七星区': '450305', '雁山区': '450311', '阳朔县': '450321', '临桂县': '450322', '灵川县': '450323', '全州县': '450324',
           '兴安县': '450325', '永福县': '450326', '灌阳县': '450327', '龙胜各族自治县': '450328', '资源县': '450329', '平乐县': '450330',
           '荔蒲县': '450331', '恭城瑶族自治县': '450332', '梧州市': '450400', '万秀区': '450403', '蝶山区': '450404', '长洲区': '450405',
           '苍梧县': '450421', '藤县': '450422', '蒙山县': '450423', '岑溪市': '450481', '北海市': '450500', '海城区': '450502',
           '银海区': '450503', '铁山港区': '450512', '合浦县': '450521', '防城港市': '450600', '港口区': '450602', '防城区': '450603',
           '上思县': '450621', '东兴市': '450681', '钦州市': '450700', '钦南区': '450702', '钦北区': '450703', '灵山县': '450721',
           '浦北县': '450722', '贵港市': '450800', '港北区': '450802', '港南区': '450803', '覃塘区': '450804', '平南县': '450821',
           '桂平市': '450881', '玉林市': '450900', '玉州区': '450902', '容县': '450921', '陆川县': '450922', '博白县': '450923',
           '兴业县': '450924', '北流市': '450981', '百色市': '451000', '右江区': '451002', '田阳县': '451021', '田东县': '451022',
           '平果县': '451023', '德保县': '451024', '靖西县': '451025', '那坡县': '451026', '凌云县': '451027', '乐业县': '451028',
           '田林县': '451029', '西林县': '451030', '隆林各族自治县': '451031', '贺州市': '451100', '八步区': '451102', '昭平县': '451121',
           '钟山县': '451122', '富川瑶族自治县': '451123', '河池市': '451200', '金城江区': '451202', '南丹县': '451221', '天峨县': '451222',
           '凤山县': '451223', '东兰县': '451224', '罗城仫佬族自治县': '451225', '环江毛南族自治县': '451226', '巴马瑶族自治县': '451227',
           '都安瑶族自治县': '451228', '大化瑶族自治县': '451229', '宜州市': '451281', '来宾市': '451300', '兴宾区': '451302', '忻城县': '451321',
           '象州县': '451322', '武宣县': '451323', '金秀瑶族自治县': '451324', '合山市': '451381', '崇左市': '451400', '江洲区': '451402',
           '扶绥县': '451421', '宁明县': '451422', '龙州县': '451423', '大新县': '451424', '天等县': '451425', '凭祥市': '451481',
           '海南省': '460000', '海口市': '460100', '秀英区': '460105', '龙华区': '460106', '琼山区': '460107', '美兰区': '460108',
           '三亚市': '460200', '五指山市': '469001', '琼海市': '469002', '儋州市': '469003', '文昌市': '469005', '万宁市': '469006',
           '东方市': '469007', '定安县': '469021', '屯昌县': '469022', '澄迈县': '469023', '临高县': '469024', '白沙黎族自治县': '469025',
           '昌江黎族自治县': '469026', '乐东黎族自治县': '469027', '陵水黎族自治县': '469028', '保亭黎族苗族自治县': '469029', '琼中黎族苗族自治县': '469030',
           '西沙群岛': '469031', '南沙群岛': '469032', '中沙群岛的岛礁及其海域': '469033', '重庆市': '500000', '万州区': '500101',
           '涪陵区': '500102', '渝中区': '500103', '大渡口区': '500104', '沙坪坝区': '500106', '九龙坡区': '500107', '南岸区': '500108',
           '北碚区': '500109', '万盛区': '500110', '渝北区': '500112', '巴南区': '500113', '黔江区': '500114', '长寿区': '500115',
           '江津区': '500116', '合川区': '500117', '永川区': '500118', '南川区': '500119', '綦江县': '500222', '潼南县': '500223',
           '铜梁县': '500224', '大足县': '500225', '荣昌县': '500226', '璧山县': '500227', '梁平县': '500228', '城口县': '500229',
           '丰都县': '500230', '垫江县': '500231', '武隆县': '500232', '忠县': '500233', '开县': '500234', '云阳县': '500235',
           '奉节县': '500236', '巫山县': '500237', '巫溪县': '500238', '石柱土家族自治县': '500240', '秀山土家族苗族自治县': '500241',
           '酉阳土家族苗族自治县': '500242', '彭水苗族土家族自治县': '500243', '北部新区': '500244', '四川省': '510000', '成都市': '510100',
           '锦江区': '510104', '青羊区': '510105', '金牛区': '510106', '武侯区': '510107', '成华区': '510108', '龙泉驿区': '510112',
           '青白江区': '510113', '新都区': '510114', '温江区': '510115', '金堂县': '510121', '双流县': '510122', '郫县': '510124',
           '大邑县': '510129', '蒲江县': '510131', '新津县': '510132', '都江堰市': '510181', '彭州市': '510182', '邛崃市': '510183',
           '崇州市': '510184', '自贡市': '510300', '自流井区': '510302', '贡井区': '510303', '大安区': '510304', '沿滩区': '510311',
           '荣县': '510321', '富顺县': '510322', '攀枝花市': '510400', '东区': '510402', '西区': '510403', '仁和区': '510411',
           '米易县': '510421', '盐边县': '510422', '泸州市': '510500', '江阳区': '510502', '纳溪区': '510503', '龙马潭区': '510504',
           '泸县': '510521', '合江县': '510522', '叙永县': '510524', '古蔺县': '510525', '德阳市': '510600', '旌阳区': '510603',
           '中江县': '510623', '罗江县': '510626', '广汉市': '510681', '什邡市': '510682', '绵竹市': '510683', '绵阳市': '510700',
           '涪城区': '510703', '游仙区': '510704', '三台县': '510722', '盐亭县': '510723', '安县': '510724', '梓潼县': '510725',
           '北川羌族自治县': '510726', '平武县': '510727', '江油市': '510781', '广元市': '510800', '元坝区': '510811', '朝天区': '510812',
           '旺苍县': '510821', '青川县': '510822', '剑阁县': '510823', '苍溪县': '510824', '遂宁市': '510900', '船山区': '510903',
           '安居区': '510904', '蓬溪县': '510921', '射洪县': '510922', '大英县': '510923', '内江市': '511000', '东兴区': '511011',
           '威远县': '511024', '资中县': '511025', '隆昌县': '511028', '乐山市': '511100', '沙湾区': '511111', '五通桥区': '511112',
           '金口河区': '511113', '犍为县': '511123', '井研县': '511124', '夹江县': '511126', '沐川县': '511129', '峨边彝族自治县': '511132',
           '马边彝族自治县': '511133', '峨眉山市': '511181', '南充市': '511300', '顺庆区': '511302', '高坪区': '511303', '嘉陵区': '511304',
           '南部县': '511321', '营山县': '511322', '蓬安县': '511323', '仪陇县': '511324', '西充县': '511325', '阆中市': '511381',
           '眉山市': '511400', '东坡区': '511402', '仁寿县': '511421', '彭山县': '511422', '洪雅县': '511423', '丹棱县': '511424',
           '青神县': '511425', '宜宾市': '511500', '翠屏区': '511502', '宜宾县': '511521', '南溪县': '511522', '江安县': '511523',
           '长宁县': '511524', '高县': '511525', '珙县': '511526', '筠连县': '511527', '兴文县': '511528', '屏山县': '511529',
           '广安市': '511600', '广安区': '511602', '岳池县': '511621', '武胜县': '511622', '邻水县': '511623', '华蓥市': '511681',
           '达州市': '511700', '通川区': '511702', '达县': '511721', '宣汉县': '511722', '开江县': '511723', '大竹县': '511724',
           '渠县': '511725', '万源市': '511781', '雅安市': '511800', '雨城区': '511802', '名山县': '511821', '荥经县': '511822',
           '汉源县': '511823', '石棉县': '511824', '天全县': '511825', '芦山县': '511826', '宝兴县': '511827', '巴中市': '511900',
           '巴州区': '511902', '通江县': '511921', '南江县': '511922', '平昌县': '511923', '资阳市': '512000', '雁江区': '512002',
           '安岳县': '512021', '乐至县': '512022', '简阳市': '512081', '阿坝藏族羌族自治州': '513200', '汶川县': '513221', '理县': '513222',
           '茂县': '513223', '松潘县': '513224', '九寨沟县': '513225', '金川县': '513226', '小金县': '513227', '黑水县': '513228',
           '马尔康县': '513229', '壤塘县': '513230', '阿坝县': '513231', '若尔盖县': '513232', '红原县': '513233', '甘孜藏族自治州': '513300',
           '康定县': '513321', '泸定县': '513322', '丹巴县': '513323', '九龙县': '513324', '雅江县': '513325', '道孚县': '513326',
           '炉霍县': '513327', '甘孜县': '513328', '新龙县': '513329', '德格县': '513330', '白玉县': '513331', '石渠县': '513332',
           '色达县': '513333', '理塘县': '513334', '巴塘县': '513335', '乡城县': '513336', '稻城县': '513337', '得荣县': '513338',
           '凉山彝族自治州': '513400', '西昌市': '513401', '木里藏族自治县': '513422', '盐源县': '513423', '德昌县': '513424', '会理县': '513425',
           '会东县': '513426', '宁南县': '513427', '普格县': '513428', '布拖县': '513429', '金阳县': '513430', '昭觉县': '513431',
           '喜德县': '513432', '冕宁县': '513433', '越西县': '513434', '甘洛县': '513435', '美姑县': '513436', '雷波县': '513437',
           '贵州省': '520000', '贵阳市': '520100', '南明区': '520102', '云岩区': '520103', '花溪区': '520111', '乌当区': '520112',
           '小河区': '520114', '开阳县': '520121', '息烽县': '520122', '修文县': '520123', '清镇市': '520181', '六盘水市': '520200',
           '钟山区': '520201', '六枝特区': '520203', '水城县': '520221', '盘县': '520222', '遵义市': '520300', '红花岗区': '520302',
           '汇川区': '520303', '遵义县': '520321', '桐梓县': '520322', '绥阳县': '520323', '正安县': '520324', '道真仡佬族苗族自治县': '520325',
           '务川仡佬族苗族自治县': '520326', '凤冈县': '520327', '湄潭县': '520328', '余庆县': '520329', '习水县': '520330', '赤水市': '520381',
           '仁怀市': '520382', '安顺市': '520400', '西秀区': '520402', '平坝县': '520421', '普定县': '520422', '镇宁布依族苗族自治县': '520423',
           '关岭布依族苗族自治县': '520424', '紫云苗族布依族自治县': '520425', '安顺市开发区': '520426', '铜仁地区': '522200', '铜仁市': '522201',
           '江口县': '522222', '玉屏侗族自治县': '522223', '石阡县': '522224', '思南县': '522225', '印江土家族苗族自治县': '522226',
           '德江县': '522227', '沿河土家族自治县': '522228', '松桃苗族自治县': '522229', '万山特区': '522230', '黔西南布依族苗族自治州': '522300',
           '兴义市': '522301', '兴仁县': '522322', '普安县': '522323', '晴隆县': '522324', '贞丰县': '522325', '望谟县': '522326',
           '册亨县': '522327', '安龙县': '522328', '毕节地区': '522400', '毕节市': '522401', '大方县': '522422', '黔西县': '522423',
           '金沙县': '522424', '织金县': '522425', '纳雍县': '522426', '威宁彝族回族苗族自治县': '522427', '赫章县': '522428',
           '黔东南苗族侗族自治州': '522600', '凯里市': '522601', '黄平县': '522622', '施秉县': '522623', '三穗县': '522624', '镇远县': '522625',
           '岑巩县': '522626', '天柱县': '522627', '锦屏县': '522628', '剑河县': '522629', '台江县': '522630', '黎平县': '522631',
           '榕江县': '522632', '从江县': '522633', '雷山县': '522634', '麻江县': '522635', '丹寨县': '522636', '黔南布依族苗族自治州': '522700',
           '都匀市': '522701', '福泉市': '522702', '荔波县': '522722', '贵定县': '522723', '瓮安县': '522725', '独山县': '522726',
           '平塘县': '522727', '罗甸县': '522728', '长顺县': '522729', '龙里县': '522730', '惠水县': '522731', '三都水族自治县': '522732',
           '云南省': '530000', '昆明市': '530100', '五华区': '530102', '盘龙区': '530103', '官渡区': '530111', '西山区': '530112',
           '东川区': '530113', '呈贡县': '530121', '晋宁县': '530122', '富民县': '530124', '宜良县': '530125', '石林彝族自治县': '530126',
           '嵩明县': '530127', '禄劝彝族苗族自治县': '530128', '寻甸回族彝族自治县': '530129', '安宁市': '530181', '曲靖市': '530300',
           '麒麟区': '530302', '马龙县': '530321', '陆良县': '530322', '师宗县': '530323', '罗平县': '530324', '富源县': '530325',
           '会泽县': '530326', '沾益县': '530328', '宣威市': '530381', '玉溪市': '530400', '红塔区': '530402', '江川县': '530421',
           '澄江县': '530422', '通海县': '530423', '华宁县': '530424', '易门县': '530425', '峨山彝族自治县': '530426',
           '新平彝族傣族自治县': '530427', '元江哈尼族彝族傣族自治县': '530428', '保山市': '530500', '隆阳区': '530502', '施甸县': '530521',
           '腾冲县': '530522', '龙陵县': '530523', '昌宁县': '530524', '昭通市': '530600', '昭阳区': '530602', '鲁甸县': '530621',
           '巧家县': '530622', '盐津县': '530623', '大关县': '530624', '永善县': '530625', '绥江县': '530626', '镇雄县': '530627',
           '彝良县': '530628', '威信县': '530629', '水富县': '530630', '丽江市': '530700', '古城区': '530702', '玉龙纳西族自治县': '530721',
           '永胜县': '530722', '华坪县': '530723', '宁蒗彝族自治县': '530724', '普洱市': '530800', '思茅区': '530802',
           '宁洱哈尼族彝族自治县': '530821', '墨江哈尼族自治县': '530822', '景东彝族自治县': '530823', '景谷傣族彝族自治县': '530824',
           '镇沅彝族哈尼族拉祜族自治县': '530825', '江城哈尼族彝族自治县': '530826', '孟连傣族拉祜族佤族自治县': '530827', '澜沧拉祜族自治县': '530828',
           '西盟佤族自治县': '530829', '临沧市': '530900', '临翔区': '530902', '凤庆县': '530921', '云县': '530922', '永德县': '530923',
           '镇康县': '530924', '双江拉祜族佤族布朗族傣族自治县': '530925', '耿马傣族佤族自治县': '530926', '沧源佤族自治县': '530927',
           '楚雄彝族自治州': '532300', '楚雄市': '532301', '双柏县': '532322', '牟定县': '532323', '南华县': '532324', '姚安县': '532325',
           '大姚县': '532326', '永仁县': '532327', '元谋县': '532328', '武定县': '532329', '禄丰县': '532331', '红河哈尼族彝族自治州': '532500',
           '个旧市': '532501', '开远市': '532502', '蒙自县': '532522', '屏边苗族自治县': '532523', '建水县': '532524', '石屏县': '532525',
           '弥勒县': '532526', '泸西县': '532527', '元阳县': '532528', '红河县': '532529', '金平苗族瑶族傣族自治县': '532530', '绿春县': '532531',
           '河口瑶族自治县': '532532', '文山壮族苗族自治州': '532600', '文山县': '532621', '砚山县': '532622', '西畴县': '532623',
           '麻栗坡县': '532624', '马关县': '532625', '丘北县': '532626', '广南县': '532627', '富宁县': '532628', '西双版纳傣族自治州': '532800',
           '景洪市': '532801', '勐海县': '532822', '勐腊县': '532823', '大理白族自治州': '532900', '大理市': '532901', '漾濞彝族自治县': '532922',
           '祥云县': '532923', '宾川县': '532924', '弥渡县': '532925', '南涧彝族自治县': '532926', '巍山彝族回族自治县': '532927',
           '永平县': '532928', '云龙县': '532929', '洱源县': '532930', '剑川县': '532931', '鹤庆县': '532932', '德宏傣族景颇族自治州': '533100',
           '瑞丽市': '533102', '潞西市': '533103', '梁河县': '533122', '盈江县': '533123', '陇川县': '533124', '怒江傈僳族自治州': '533300',
           '泸水县': '533321', '福贡县': '533323', '贡山独龙族怒族自治县': '533324', '兰坪白族普米族自治县': '533325', '迪庆藏族自治州': '533400',
           '香格里拉县': '533421', '德钦县': '533422', '维西傈僳族自治县': '533423', '西藏自治区': '540000', '拉萨市': '540100',
           '城关区': '620102', '林周县': '540121', '当雄县': '540122', '尼木县': '540123', '曲水县': '540124', '堆龙德庆县': '540125',
           '达孜县': '540126', '墨竹工卡县': '540127', '昌都地区': '542100', '昌都县': '542121', '江达县': '542122', '贡觉县': '542123',
           '类乌齐县': '542124', '丁青县': '542125', '察雅县': '542126', '八宿县': '542127', '左贡县': '542128', '芒康县': '542129',
           '洛隆县': '542132', '边坝县': '542133', '山南地区': '542200', '乃东县': '542221', '扎囊县': '542222', '贡嘎县': '542223',
           '桑日县': '542224', '琼结县': '542225', '曲松县': '542226', '措美县': '542227', '洛扎县': '542228', '加查县': '542229',
           '隆子县': '542231', '错那县': '542232', '浪卡子县': '542233', '日喀则地区': '542300', '日喀则市': '542301', '南木林县': '542322',
           '江孜县': '542323', '定日县': '542324', '萨迦县': '542325', '拉孜县': '542326', '昂仁县': '542327', '谢通门县': '542328',
           '白朗县': '542329', '仁布县': '542330', '康马县': '542331', '定结县': '542332', '仲巴县': '542333', '亚东县': '542334',
           '吉隆县': '542335', '聂拉木县': '542336', '萨嘎县': '542337', '岗巴县': '542338', '那曲地区': '542400', '那曲县': '542421',
           '嘉黎县': '542422', '比如县': '542423', '聂荣县': '542424', '安多县': '542425', '申扎县': '542426', '索县': '542427',
           '班戈县': '542428', '巴青县': '542429', '尼玛县': '542430', '双湖特别区': '542431', '阿里地区': '542500', '普兰县': '542521',
           '札达县': '542522', '噶尔县': '542523', '日土县': '542524', '革吉县': '542525', '改则县': '542526', '措勤县': '542527',
           '林芝地区': '542600', '林芝县': '542621', '工布江达县': '542622', '米林县': '542623', '墨脱县': '542624', '波密县': '542625',
           '察隅县': '542626', '朗县': '542627', '西藏驻格尔木办事处市级': '542700', '西藏驻格尔木办事处县级': '542701', '陕西省': '610000',
           '西安市': '610100', '碑林区': '610103', '莲湖区': '610104', '灞桥区': '610111', '未央区': '610112', '雁塔区': '610113',
           '阎良区': '610114', '临潼区': '610115', '蓝田县': '610122', '周至县': '610124', '户县': '610125', '高陵县': '610126',
           '铜川市': '610200', '王益区': '610202', '印台区': '610203', '耀州区': '610204', '宜君县': '610222', '宝鸡市': '610300',
           '渭滨区': '610302', '金台区': '610303', '陈仓区': '610304', '凤翔县': '610322', '岐山县': '610323', '扶风县': '610324',
           '眉县': '610326', '陇县': '610327', '千阳县': '610328', '麟游县': '610329', '凤县': '610330', '太白县': '610331',
           '咸阳市': '610400', '秦都区': '610402', '杨凌区': '611101', '渭城区': '610404', '三原县': '610422', '泾阳县': '610423',
           '乾县': '610424', '礼泉县': '610425', '永寿县': '610426', '彬县': '610427', '长武县': '610428', '旬邑县': '610429',
           '淳化县': '610430', '武功县': '610431', '兴平市': '610481', '渭南市': '610500', '临渭区': '610502', '华县': '610521',
           '潼关县': '610522', '大荔县': '610523', '合阳县': '610524', '澄城县': '610525', '蒲城县': '610526', '白水县': '610527',
           '富平县': '610528', '韩城市': '610581', '华阴市': '610582', '延安市': '610600', '宝塔区': '610602', '延长县': '610621',
           '延川县': '610622', '子长县': '610623', '安塞县': '610624', '志丹县': '610625', '吴起县': '610626', '甘泉县': '610627',
           '富县': '610628', '洛川县': '610629', '宜川县': '610630', '黄龙县': '610631', '黄陵县': '610632', '汉中市': '610700',
           '汉台区': '610702', '南郑县': '610721', '城固县': '610722', '洋县': '610723', '西乡县': '610724', '勉县': '610725',
           '宁强县': '610726', '略阳县': '610727', '镇巴县': '610728', '留坝县': '610729', '佛坪县': '610730', '榆林市': '610800',
           '榆阳区': '610802', '神木县': '610821', '府谷县': '610822', '横山县': '610823', '靖边县': '610824', '定边县': '610825',
           '绥德县': '610826', '米脂县': '610827', '佳县': '610828', '吴堡县': '610829', '清涧县': '610830', '子洲县': '610831',
           '安康市': '610900', '汉滨区': '610902', '汉阴县': '610921', '石泉县': '610922', '宁陕县': '610923', '紫阳县': '610924',
           '岚皋县': '610925', '平利县': '610926', '镇坪县': '610927', '旬阳县': '610928', '白河县': '610929', '商洛市': '611000',
           '商州区': '611002', '洛南县': '611021', '丹凤县': '611022', '商南县': '611023', '山阳县': '611024', '镇安县': '611025',
           '柞水县': '611026', '杨凌示范区': '611100', '甘肃省': '620000', '兰州市': '620100', '七里河区': '620103', '西固区': '620104',
           '安宁区': '620105', '红古区': '620111', '永登县': '620121', '皋兰县': '620122', '榆中县': '620123', '嘉峪关市': '620200',
           '金昌市': '620300', '金川区': '620302', '永昌县': '620321', '白银市': '620400', '白银区': '620402', '平川区': '620403',
           '靖远县': '620421', '会宁县': '620422', '景泰县': '620423', '天水市': '620500', '秦州区': '620502', '麦积区': '620503',
           '清水县': '620521', '秦安县': '620522', '甘谷县': '620523', '武山县': '620524', '张家川回族自治县': '620525', '武威市': '620600',
           '凉州区': '620602', '民勤县': '620621', '古浪县': '620622', '天祝藏族自治县': '620623', '张掖市': '620700', '甘州区': '620702',
           '肃南裕固族自治县': '620721', '民乐县': '620722', '临泽县': '620723', '高台县': '620724', '山丹县': '620725', '平凉市': '620800',
           '崆峒区': '620802', '泾川县': '620821', '灵台县': '620822', '崇信县': '620823', '华亭县': '620824', '庄浪县': '620825',
           '静宁县': '620826', '酒泉市': '620900', '肃州区': '620902', '金塔县': '620921', '瓜州县': '620922', '肃北蒙古族自治县': '620923',
           '阿克塞哈萨克族自治县': '620924', '玉门市': '620981', '敦煌市': '620982', '庆阳市': '621000', '西峰区': '621002', '庆城县': '621021',
           '环县': '621022', '华池县': '621023', '合水县': '621024', '正宁县': '621025', '宁县': '621026', '镇原县': '621027',
           '定西市': '621100', '安定区': '621102', '通渭县': '621121', '陇西县': '621122', '渭源县': '621123', '临洮县': '621124',
           '漳县': '621125', '岷县': '621126', '陇南市': '621200', '武都区': '621202', '成县': '621221', '文县': '621222',
           '宕昌县': '621223', '康县': '621224', '西和县': '621225', '礼县': '621226', '徽县': '621227', '两当县': '621228',
           '临夏回族自治州': '622900', '临夏市': '622901', '临夏县': '622921', '康乐县': '622922', '永靖县': '622923', '广河县': '622924',
           '和政县': '622925', '东乡族自治县': '622926', '积石山保安族东乡族撒拉族自治县': '622927', '甘南藏族自治州': '623000', '合作市': '623001',
           '临潭县': '623021', '卓尼县': '623022', '舟曲县': '623023', '迭部县': '623024', '玛曲县': '623025', '碌曲县': '623026',
           '夏河县': '623027', '青海省': '630000', '西宁市': '630100', '城东区': '630102', '城西区': '630104', '城北区': '630105',
           '大通回族土族自治县': '630121', '湟中县': '630122', '湟源县': '630123', '海东地区': '632100', '平安县': '632121',
           '民和回族土族自治县': '632122', '乐都县': '632123', '互助土族自治县': '632126', '化隆回族自治县': '632127', '循化撒拉族自治县': '632128',
           '海北藏族自治州': '632200', '门源回族自治县': '632221', '祁连县': '632222', '海晏县': '632223', '刚察县': '632224',
           '黄南藏族自治州': '632300', '同仁县': '632321', '尖扎县': '632322', '泽库县': '632323', '河南蒙古族自治县': '632324',
           '海南藏族自治州': '632500', '共和县': '632521', '同德县': '632522', '贵德县': '632523', '兴海县': '632524', '贵南县': '632525',
           '果洛藏族自治州': '632600', '玛沁县': '632621', '班玛县': '632622', '甘德县': '632623', '达日县': '632624', '久治县': '632625',
           '玛多县': '632626', '玉树藏族自治州': '632700', '玉树县': '632721', '杂多县': '632722', '称多县': '632723', '治多县': '632724',
           '囊谦县': '632725', '曲麻莱县': '632726', '海西蒙古族藏族自治州': '632800', '格尔木市': '632801', '德令哈市': '632802',
           '乌兰县': '632821', '都兰县': '632822', '天峻县': '632823', '大柴旦': '632824', '冷湖': '632825', '茫崖': '632826',
           '宁夏回族自治区': '640000', '银川市': '640100', '兴庆区': '640104', '西夏区': '640105', '金凤区': '640106', '永宁县': '640121',
           '贺兰县': '640122', '灵武市': '640181', '石嘴山市': '640200', '大武口区': '640202', '惠农区': '640205', '平罗县': '640221',
           '吴忠市': '640300', '利通区': '640302', '红寺堡开发区': '640303', '盐池县': '640323', '同心县': '640324', '青铜峡市': '640381',
           '固原市': '640400', '原州区': '640402', '西吉县': '640422', '隆德县': '640423', '泾源县': '640424', '彭阳县': '640425',
           '中卫市': '640500', '沙坡头区': '640502', '中宁县': '640521', '海原县': '640522', '新疆维吾尔自治区': '650000', '乌鲁木齐市': '650100',
           '天山区': '650102', '沙依巴克区': '650103', '水磨沟区': '650105', '头屯河区': '650106', '达坂城区': '650107', '米东区': '650109',
           '乌鲁木齐县': '650121', '克拉玛依市': '650200', '独山子区': '650202', '克拉玛依区': '650203', '白碱滩区': '650204',
           '乌尔禾区': '650205', '吐鲁番地区': '652100', '吐鲁番市': '652101', '鄯善县': '652122', '托克逊县': '652123', '哈密地区': '652200',
           '哈密市': '652201', '巴里坤哈萨克自治县': '652222', '伊吾县': '652223', '哈密地直': '652224', '昌吉回族自治州': '652300',
           '昌吉市': '652301', '阜康市': '652302', '呼图壁县': '652323', '玛纳斯县': '652324', '奇台县': '652325', '吉木萨尔县': '652327',
           '木垒哈萨克自治县': '652328', '昌吉州直': '652329', '博尔塔拉蒙古自治州': '652700', '博乐市': '652701', '州本级': '652704',
           '精河县': '652722', '温泉县': '652723', '巴音郭楞蒙古自治州': '652800', '库尔勒市': '652801', '巴州直属': '652802',
           '巴州石油教育分局': '652803', '库尔勒市经济技术开发区': '652804', '轮台县': '652822', '尉犁县': '652823', '若羌县': '652824',
           '且末县': '652825', '焉耆回族自治县': '652826', '和静县': '652827', '和硕县': '652828', '博湖县': '652829', '阿克苏地区': '652900',
           '阿克苏市': '652901', '温宿县': '652922', '库车县': '652923', '沙雅县': '652924', '新和县': '652925', '拜城县': '652926',
           '乌什县': '652927', '阿瓦提县': '652928', '柯坪县': '652929', '阿克苏地区直属': '652930', '克孜勒苏柯尔克孜自治州': '653000',
           '阿图什市': '653001', '阿克陶县': '653022', '阿合奇县': '653023', '乌恰县': '653024', '喀什地区': '653100', '喀什市': '653101',
           '喀什地区本级': '653111', '疏附县': '653121', '疏勒县': '653122', '英吉沙县': '653123', '泽普县': '653124', '莎车县': '653125',
           '叶城县': '653126', '麦盖提县': '653127', '岳普湖县': '653128', '伽师县': '653129', '巴楚县': '653130',
           '塔什库尔干塔吉克自治县': '653131', '和田地区': '653200', '和田市': '653201', '和田县': '653221', '墨玉县': '653222',
           '皮山县': '653223', '洛浦县': '653224', '策勒县': '653225', '于田县': '653226', '民丰县': '653227', '和田地直': '653228',
           '伊犁哈萨克自治州': '654000', '伊犁州直属': '654001', '伊宁市': '654002', '奎屯市': '654003', '伊宁县': '654021',
           '察布查尔锡伯自治县': '654022', '霍城县': '654023', '巩留县': '654024', '新源县': '654025', '昭苏县': '654026', '特克斯县': '654027',
           '尼勒克县': '654028', '塔城地区': '654200', '塔城市': '654201', '乌苏市': '654202', '塔城地直': '654203', '额敏县': '654221',
           '沙湾县': '654223', '托里县': '654224', '裕民县': '654225', '和布克赛尔蒙古自治县': '654226', '阿勒泰地区': '654300',
           '阿勒泰市': '654301', '布尔津县': '654321', '富蕴县': '654322', '福海县': '654323', '哈巴河县': '654324', '青河县': '654325',
           '吉木乃县': '654326', '阿勒泰地直': '654327', '自治区直辖县级行政区划': '659000', '石河子市': '659001', '阿拉尔市': '659002',
           '图木舒克市': '659003', '五家渠市': '659004', '新疆生产建设兵团': '660000', '兵团农一师': '660100', '1团': '660101', '2团': '660102',
           '3团': '660103', '4团': '660104', '5团': '660105', '6团': '660106', '7团': '660107', '8团': '660108',
           '9团': '660109', '10团': '660110', '11团': '660111', '12团': '660112', '13团': '660113', '14团': '660114',
           '15团': '660115', '16团': '660116', '塔水处': '660117', '水工处': '660118', '沙井子民族学校': '660119', '农一师师直': '660122',
           '兵团农二师': '660200', '21团': '660201', '22团': '660202', '23团': '660203', '24团': '660204', '25团': '660205',
           '26团': '660206', '27团': '660207', '28团': '660208', '29团': '660209', '30团': '660210', '31团': '660211',
           '32团': '660212', '33团': '660213', '34团': '660214', '35团': '660215', '36团': '660216', '223团': '660217',
           '塔什店': '660218', '且末支队': '660219', '十一农场': '660221', '三建': '660222', '农二师师直': '660224', '兵团农三师': '660300',
           '41团': '660301', '42团': '660302', '43团': '660303', '44团': '660304', '45团': '660305', '46团': '660306',
           '48团': '660307', '49团': '660308', '50团': '660309', '51团': '660310', '52团': '660311', '53团': '660312',
           '托云牧场': '660313', '东风农场': '660314', '伽师总场': '660315', '红旗农场': '660316', '叶城二牧场': '660317', '农三师师直': '660319',
           '兵团农四师': '660400', '61团': '660401', '62团': '660402', '63团': '660403', '64团': '660404', '65团': '660405',
           '66团': '660406', '67团': '660407', '68团': '660408', '69团': '660409', '70团': '660410', '71团': '660411',
           '72团': '660412', '73团': '660413', '74团': '660414', '75团': '660415', '76团': '660416', '77团': '660417',
           '78团': '660418', '79团': '660419', '拜什墩': '660420', '良繁场': '660421', '农四师师直': '660422', '兵团农五师': '660500',
           '81团': '660501', '82团': '660502', '83团': '660503', '84团': '660504', '85团': '660505', '86团': '660506',
           '87团': '660507', '88团': '660508', '89团': '660509', '90团': '660510', '91团': '660511', '农五师师直': '660512',
           '兵团农六师': '660600', '101团': '660601', '102团': '660602', '103团': '660603', '105团': '660604', '106团': '660605',
           '107团': '660606', '108团': '660607', '109团': '660608', '110团': '660609', '111团': '660610', '芳草湖': '660611',
           '新湖': '660612', '军户': '660613', '共青团': '660614', '六运湖': '660615', '土墩子': '660616', '红旗': '660617',
           '奇台': '660618', '北塔山': '660619', '大黄山学校': '660620', '十三户学校': '660621', '农六师师直': '660622', '兵团农七师': '660700',
           '123团': '660701', '124团': '660702', '125团': '660703', '126团': '660704', '127团': '660705', '128团': '660706',
           '129团': '660707', '130团': '660708', '131团': '660709', '137团': '660710', '农七师奎管处': '660712',
           '农七师奎东农场': '660716', '农七师师直': '660717', '兵团农八师': '660800', '121团': '660801', '122团': '660802',
           '133团': '660804', '134团': '660805', '135团': '660806', '136团': '660807', '141团': '660808', '142团': '660809',
           '143团': '660810', '144团': '660811', '石总场': '660812', '147团': '660813', '148团': '660814', '149团': '660815',
           '150团': '660816', '152团': '660818', '通联中学': '660821', '柴油机厂学校': '660822', '玛管处中学': '660823',
           '天富红山嘴学校': '660824', '南山中学': '660825', '六建': '660826', '路桥中学': '660827', '农八师师直': '660829',
           '兵团农九师': '660900', '161团': '660901', '162团': '660902', '163团': '660903', '164团': '660904', '165团': '660905',
           '166团': '660906', '167团': '660907', '168团': '660908', '169团': '660909', '170团': '660910', '团结农场': '660911',
           '农九师师直': '660912', '兵团农十师': '661000', '181团': '661001', '182团': '661002', '183团': '661003', '184团': '661004',
           '185团': '661005', '186团': '661006', '187团': '661007', '188团': '661008', '190团': '661010', '农十师师直': '661013',
           '兵团建工师': '661100', '建工师师属': '661101', '兵团农十二师': '661200', '养禽场': '661201', '五一农场': '661202',
           '三坪农场': '661203', '头屯河农场': '661204', '一零四团': '661205', '西山农场': '661206', '二二一团': '661207',
           '农十二师师直': '661208', '兵团农十三师': '661300', '红星二牧场': '661301', '红星一牧场': '661302', '淖毛湖农场': '661303',
           '红星二场': '661304', '黄田农场': '661305', '红星三场': '661306', '红山农场': '661307', '柳树泉农场': '661308', '红星一场': '661309',
           '红星四场': '661310', '火箭农场': '661311', '农十三师师直': '661312', '兵团农十四师': '661400', '四十七团': '661401',
           '皮山农场': '661402', '一牧场': '661403', '224团': '661404', '兵团直属': '661501', '222团': '662201', '台湾省': '710000',
           '香港特别行政区': '810000', '澳门特别行政区': '820000'}

baijiaxing = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
              '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
              '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
              '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
              '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
              '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
              '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
xing = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕',
        '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛',
        '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉',
        '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康',
        '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝',
        '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵',
        '席', '季', '麻', '强', '贾', '路', '娄', '危', '江', '童', '颜', '郭', '梅', '盛', '林', '刁', '钟', '徐', '邱', '骆', '高', '夏',
        '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗',
        '丁', '宣', '贲', '邓', '郁', '单', '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', '裴', '陆',
        '荣', '翁', '荀', '羊', '於', '惠', '甄', '麴', '家', '封', '芮', '羿', '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫',
        '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', '伊', '宫', '宁', '仇',
        '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸', '司', '韶', '郜', '黎', '蓟', '薄',
        '印', '宿', '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阴', '欎', '胥', '能',
        '苍', '双', '闻', '莘', '党', '翟', '谭', '贡', '劳', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '舄', '璩', '桑', '桂',
        '濮', '牛', '寿', '通', '边', '扈', '燕', '冀', '郏', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连',
        '茹', '习', '宦', '艾', '鱼', '容', '向', '古', '易', '慎', '戈', '廖', '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘',
        '匡', '国', '文', '寇', '广', '禄', '阙', '东', '殴', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾',
        '敖', '融', '冷', '訾', '辛', '阚', '那', '简', '饶', '空', '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相',
        '查', '後', '荆', '红', '游', '竺', '权', '逯', '盖', '益', '桓', '公', '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方',
        '赫连', '皇甫', '尉迟', '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙', '轩辕', '令狐', '钟离', '宇文',
        '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空', '亓官', '司寇', '仉', '督', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', '壤驷', '公良',
        '拓跋', '夹谷', '宰父', '谷梁', '晋', '楚', '闫', '法', '汝', '鄢', '涂', '钦', '段干', '百里', '东郭', '南门', '呼延', '归', '海', '羊舌',
        '微生', '岳', '帅', '缑', '亢', '况', '后', '有', '琴', '梁丘', '左丘', '东门', '西门', '商', '牟', '佘', '佴', '伯', '赏', '南宫', '墨',
        '哈', '谯', '笪', '年', '爱', '阳', '佟',
        '付', '仝', '代', '令', '任', '但', '何', '欧', '佘', '余', '信', '修',
        '王', '李', '张', '刘', '陈', '杨', '黄', '吴', '赵', '周', '徐', '孙', '马', '朱', '胡', '林', '郭', '何', '高', '罗', '郑', '梁',
        '谢', '宋', '唐', '许', '邓', '冯', '韩', '曹', '曾', '彭', '萧', '蔡', '潘', '田', '董', '袁', '于', '余', '叶', '蒋', '杜', '苏',
        '魏', '程', '吕', '丁', '沈', '任', '姚', '卢', '傅', '钟', '姜', '崔', '谭', '廖', '范', '汪', '陆', '金', '石', '戴', '贾', '韦',
        '夏', '邱', '方', '侯', '邹', '熊', '孟', '秦', '白', '江', '阎', '薛', '尹', '段', '雷', '黎', '史', '龙', '陶', '贺', '顾', '毛',
        '郝', '龚', '邵', '万', '钱', '严', '赖', '覃', '洪', '武', '莫', '孔', '汤', '向', '常', '温', '康', '施', '文', '牛', '樊', '葛',
        '邢', '安', '齐', '易', '乔', '伍', '庞', '颜', '倪', '庄', '聂', '章', '鲁', '岳', '翟', '殷', '詹', '申', '欧', '耿', '关', '兰',
        '焦', '俞', '左', '柳', '甘', '祝', '包', '宁', '尚', '符', '舒', '阮', '柯', '纪', '梅', '童', '凌', '毕', '单', '季', '裴', '霍',
        '涂', '成', '苗', '谷', '盛', '曲', '翁', '冉', '骆', '蓝', '路', '游', '辛', '靳', '欧', '管', '柴', '蒙', '鲍', '华', '喻', '祁',
        '蒲', '房', '滕', '屈', '饶', '解', '牟', '艾', '尤', '阳', '时', '穆', '农', '司', '卓', '古', '吉', '缪', '简', '车', '项', '连',
        '芦', '麦', '褚', '娄', '窦', '戚', '岑', '景', '党', '宫', '费', '卜', '冷', '晏', '席', '卫', '米', '柏', '宗', '瞿', '桂', '全',
        '佟', '应', '臧', '闵', '苟', '邬', '边', '卞', '姬', '师', '和', '仇', '栾', '隋', '商', '刁', '沙', '荣', '巫', '寇', '桑', '郎',
        '甄', '丛', '仲', '虞', '敖', '巩', '明', '佘', '池', '查', '麻', '苑', '迟', '邝', '官', '封', '谈', '匡', '鞠', '惠', '荆', '乐',
        '冀', '郁', '胥', '南', '班', '储', '原', '栗', '燕', '楚', '鄢', '劳', '谌', '奚', '皮', '粟', '冼', '蔺', '楼', '盘', '满', '闻',
        '位', '厉', '伊', '仝', '区', '郜', '海', '阚', '花', '权', '强', '帅', '屠', '豆', '朴', '盖', '练', '廉', '禹', '井', '祖', '漆',
        '巴', '丰', '支', '卿', '国', '狄', '平', '计', '索', '宣', '晋', '相', '初', '门', '云', '容', '敬', '来', '扈', '晁', '芮', '都',
        '普', '阙', '浦', '戈', '伏', '鹿', '薄', '邸', '雍', '辜', '羊', '阿', '乌', '母', '裘', '亓', '修', '邰', '赫', '杭', '况', '那',
        '宿', '鲜', '印', '逯', '隆', '茹', '诸', '战', '慕', '危', '玉', '银', '亢', '嵇', '公', '哈', '湛', '宾', '戎', '勾', '茅', '利',
        '於', '呼', '居', '揭', '干', '但', '尉', '冶', '斯', '元', '束', '檀', '衣', '信', '展', '阴', '昝', '智', '幸', '奉', '植', '衡',
        '富', '尧', '闭', '由',
        ]
ming = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地',
        '为', '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自',
        '以', '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都',
        '好', '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开',
        '美', '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意',
        '动', '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯',
        '知', '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正',
        '感', '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果',
        '走', '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真',
        '打', '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界',
        '门', '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性',
        '马', '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让',
        '母', '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英',
        '军', '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快',
        '原', '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条',
        '呢', '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片',
        '罗', '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合',
        '反', '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运',
        '及', '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司',
        '巴', '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形',
        '影', '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈',
        '容', '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计',
        '您', '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻',
        '统', '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示',
        '愿', '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社',
        '算', '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息',
        '功', '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图',
        '具', '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引',
        '食', '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试',
        '怀', '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除',
        '跑', '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳',
        '验', '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿',
        '睡', '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店',
        '否', '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河',
        '续', '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪',
        '索', '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族',
        '低', '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅',
        '街', '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀',
        '律', '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职',
        '属', '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉',
        '遗', '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳',
        '差', '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府',
        '压', '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童',
        '顶', '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯',
        '巨', '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层',
        '付', '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀',
        '营', '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊',
        '降', '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙',
        '杰', '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡',
        '预', '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误', '乾',
        '坤']


