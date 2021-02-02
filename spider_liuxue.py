# -*- coding:utf-8 -*-
import random
import re
import requests
import pymysql
import time
import json
import pandas
import csv



class Liuxue():

    def __init__(self):

        # 随机user agent库
        self.user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
        ]
    # def Download_Html1(self):
    #     header = {
    #         "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    #     }
    #
    #     request = requests.get(url=r'http://www.compassedu.hk/university_7_1',headers = header)
    #     request.encoding = 'utf-8'
    #     # print(re1.text)
    #     f = open(r'../1.txt', 'a', encoding='utf-8')
    #     f.write(request.text)
        self.csv_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        self.csv_id = "cons" + self.csv_time + ".csv"
        self.creat_database_time = "country_"+self.csv_time
        self.creat_database_time_delHMS = time.strftime("%Y_%m_%d", time.localtime())
    def acode(self):
        az = []
        data = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'User-Agent':random.choice(self.user_agent),
            "timestamp" : "1611381650888",
            "sign" : "login"
        }

        re = requests.post(url = "http://api.compassedu.hk/index.php/api/v1/app/acode",data = data)
        re.encoding = 'UTF-8'
        re_text = re.json()   #type为dict
        data1 = re_text.get("data")

        for i in data1:     # 取data里面所有对象 0,a-z放到列表az
            az.append(i)

        with open('./acode.json', encoding='utf8') as f:
            acode = json.loads(f.read())

        # 第一行写入country_code,country_name\n
        # with open('.\\{}'.format(self.csv_id), 'a', encoding='utf8') as f:
        #     f.write("country_code,country_name\n")
        #     f.close()
        for j in az:
            cons = acode['data'][j]
            for i in cons:
                # 写入csv文件
                with open('.\\{}'.format(self.csv_id), 'a',encoding='utf8') as f:
                    f.write('{},{}\n'.format(i['code'], i['name']))

        # 读取csv文件写入数据库
        #创建数据库创建表
        sql_creat_database = "create database {};".format(self.creat_database_time_delHMS)
        sql_creat_table = "create table {}(" \
                          "country_id varchar(255)," \
                          "country_name varchar(255)," \
                          "country_code varchar(255)," \
                          "country_type varchar(255" \
                          "))".format(self.creat_database_time)
        print(sql_creat_database)
        self.write_db(sql_creat_database)
        time.sleep(0.5)
        print(sql_creat_table)
        self.write_db(sql_creat_table,database=sql_creat_database)
        time.sleep(0.5)
        with open(self.csv_id,"r",encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # 循环列表数据一条条写入库
                sql = "insert into country (country_code,country_name) values ('{}','{}')".format(row[0],row[1])
                self.write_db(sql,database="liuxue")


    def school_list(self):
        data = {
            "accept": "text/html, application/xhtml+xml, image/jxr, */*",
            "User-Agent":random.choice(self.user_agent),
            "page":"1",
            "count":"10000",
            "country":"",
            "sign":"d762b68723fa798f5e46f54bce192e91",
            "tab_id":"tab_usnews",
            "timestamp":"1611652121353",
            "top":"",
            "area":""
        }
        """
        美国12  
        英国7 
        澳大利亚9 
        香港11
        新加坡10
        """

        re1 = requests.post(url="http://api.compassedu.hk/index.php/api/v1/collegeapp/getlist",data=data)
        re1.encoding = "utf-8"
        re1 = re1.json()
        re1_list = re1.get("data")
        # 循环出所有的键值对
        for key in re1_list.get("list"):
            print("-------------------")
            # print(key)
            # print(type(key))    #key type dict
            try:
                id = key["id"]
                sort = key["sort"]
                univ_name = key["univ_name"]
                univ_ename = key["univ_ename"]
                city = key["city"]
                univ_logo = key["univ_logo"]
                url = key["url"]
            except Exception as e:
                print("字典键值对取值报错(有可能是列表type报错,不管)")
                print(e)
                continue
            # finally:
            print("字典键值对取值完成")
            # 数据库
            insert_sql = 'insert into school (univ_id,univ_sort,univ_name,univ_ename,city,univ_logo,url) values ("{}","{}","{}","{}","{}","{}","{}")'\
                                        .format(id,sort,univ_name,univ_ename,city,univ_logo,url)
            # print(insert_sql)
            self.write_db(insert_sql)
            print("写入数据库完成")
        print("字典键值对取值完成")

# 踩过的坑
# for value in key:
# #     # print(value,key[value])
# #     kv = {}
#     if value == "id":

# #         # print(key[value])
# #         # id_sql = "insert into school (univ_id) values ('{}')".format(key[value])
# #         # self.write_db(id_sql)
#     elif value == "sort":
# #         # sort_sql = "insert into school (univ_sort) values ('{}')".format(key[value])
# #         # self.write_db(sort_sql)
#     elif value == "univ_name":
# #         # name_sql = "insert into school (univ_name) values ('{}')".format(key[value])
# #         # self.write_db(name_sql)
#     elif value == "univ_ename":
# #         ename_sql = 'insert into school (univ_ename) values ("{}")'.format(key[value])
# #         print(ename_sql)
# #         print(value+key[value])
# #         self.write_db(ename_sql)
#     elif value == "city":
# #         city_sql = "insert into school (city) values ('{}')".format(key[value])
# #         self.write_db(city_sql)
#     elif value == "univ_logo":
# #         logo_sql = "insert into school (univ_logo) values ('{}')".format(key[value])
# #         self.write_db(logo_sql)
#     elif value == "url":
#         pass
#     elif value == "type":
#         pass
#     else:
#         continue
#         pass  #  #




    def write_db(self,sql,database='liuxue',host = '127.0.0.1',user = 'root',password = '123456',):
        con = pymysql.connect(host = host,user = user,password = password,database = database,port = 3307)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
        cur.close()




if __name__ == '__main__':
    liu = Liuxue()
    liu.acode()
    # liu.school_list()


