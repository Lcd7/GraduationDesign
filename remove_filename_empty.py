import os

'''
去掉文件名的空格
'''
if __name__ == "__main__":

    a = './html文件'
    for parent, dirnames, filenames in os.walk(a):
        for filename in filenames:
            os.rename(os.path.join(parent, filename), os.path.join(parent, filename.replace(' ', '')))
