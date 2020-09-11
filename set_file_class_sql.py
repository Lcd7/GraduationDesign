import threading
import pyodbc
import os


def get_all_files(dir):
    _files_ = dict()
    num = 0
    for root, _, files in os.walk(dir):
        # print(root) #当前目录路径  
        # print(dirs) #当前路径下所有子目录  
        # print(files) #当前路径下所有非目录子文件
        # print('\n')
        num += 1
        if num > 1:
            _class = root.split('\\')[-1]
            _files_[_class] = files
    return _files_

if __name__ == "__main__":

    mutex = threading.Lock()
    database = 'dbo.file_table'
    conn = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-RQTO7L9;DATABASE=lcd_test;UID=sa;PWD=Soda.123')
    rsor = conn.cursor()

    #把文章的课程名存入数据库
    files = get_all_files('html文件')
    with mutex:
        for key, value in files.items():
            f_class = key
            f_name = ''
            for item in value:
                aaa = "'" + item.replace(' ','')[:-5] + "',"
                f_name += aaa
            sql1 = "update file_table set file_class = '{}' where file_name in({})".format(f_class ,f_name[:-1])
            rsor.execute(sql1)
            rsor.commit()
    
    #本课程的类别存入数据库
    # part_dict = dict()
    # part_dict['HTML/CSS'] = []
    # sql2 = "update file_table set file_part = '{}' where file_class in({})".format()