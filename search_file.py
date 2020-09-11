'''
根据用户的输入查找文件
'''

import pyodbc
import threading
import servers


def do_search(result, title_index, invert_index):
    marks = dict()
    for word in result:
        if word in title_index:
            for key, value in title_index[word].items():
                if key in marks:
                    marks[key] += value*10       #标题占10分
                else:
                    marks[key] = 0
                    marks[key] += value*10
        if word in invert_index:
            for key, value in invert_index[word].items():
                if key in marks:
                    marks[key] += value*1       #正文占1分
                else:
                    marks[key] = 0
                    marks[key] += value*1
            #按照字典的index升序排列
            #然后计算权值，得到分值
    sort_marks = sorted(marks.items(), key = lambda x:x[1], reverse = True)
    # print("分数{}".format(sort_marks))
    if sort_marks:
        #得到marks，根据数据库提取文章
        mutex = threading.Lock()
        conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
        rsor = conn.cursor()

        _path = []
        f_id = ''
        # flag = 0
        for article in sort_marks:
            # if flag < 50:
            f_id += str(article[0]) + ','
            #     flag += 1
            # else:
            #     break
        f_id = f_id[:-1]
        str_f_id = ',' + f_id + ','
        with mutex:
            select_sql = "select file_path, content from file_table where f_id in ({}) order by charindex(','+convert(varchar,f_id)+',', '{}')".format(f_id, str_f_id)
            rsor.execute(select_sql)
            _path = list(rsor.fetchall())
        # print(_path)
        return _path
    else:
        return None

def search_similiar(vacablory, title_index, invert_index):
    marks = dict()
    if vacablory in title_index:
        for key, value in title_index[vacablory].items():
            if key in marks:
                marks[key] += value*10       #标题占10分
            else:
                marks[key] = 0
                marks[key] += value*10
    if vacablory in invert_index:
        for key, value in invert_index[vacablory].items():
            if key in marks:
                marks[key] += value*1       #正文占1分
            else:
                marks[key] = 0
                marks[key] += value*1
        #按照字典的index升序排列
        #然后计算权值，得到分值
    sort_marks = sorted(marks.items(), key = lambda x:x[1], reverse = True)

    if sort_marks:
        #得到marks，根据数据库提取文章
        mutex = threading.Lock()
        conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
        rsor = conn.cursor()

        _path = []
        f_id = ''
        flag = 0
        for article in sort_marks:
            if flag < 10:
                f_id += str(article[0]) + ','
                flag += 1
            else:
                break
        f_id = f_id[:-1]

        with mutex:
            rsor.execute("select file_path from file_table where f_id in ({})".format(f_id))
        #     _path = list(rsor.fetchmany(2))
        # print(_path)
            for i in list(rsor.fetchmany(2)):
                _path.append(i[0])
        # print(_path)
        return _path
    else:
        return None

def choose_search(choose_w):
    mutex = threading.Lock()
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
    rsor = conn.cursor()

    file_title = ''
    for c_w in choose_w:
        file_title += "'" + c_w[:-5] + "',"
    file_title = file_title[:-1]
    # print(file_title)

    _path = []
    with mutex:
        sql = "select file_path, content from file_table where file_name in ({})".format(file_title)
        # print(sql)
        rsor.execute(sql)
        _path = list(rsor.fetchall())
    
    if _path:
        # print('1')
        return _path
    else:
        # print('2')
        return None

def choosepartfile(choosepart):
    mutex = threading.Lock()
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
    rsor = conn.cursor()
    sql = "select file_class from file_table where file_part = '{}'".format(choosepart)
    _path = []

    with mutex:
        rsor.execute(sql)
        _path = list(rsor.fetchall())

    if _path:
        return _path
    else:
        return None

if __name__ == "__main__":
    pass
    # chooseclass = 'CSS教程'
    # f_dir = r'D:\Code\Code\Code\基于自然语言处理的索引型知识库\html文件\\' + chooseclass
    # f_list = servers.get_files_name(f_dir)
    # choose_search(f_list)