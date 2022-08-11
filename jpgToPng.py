import os


def Rename(filename):
    transF = os.path.splitext(filename)
    if transF[1] == '.png':
        new_name = transF[0] + '.jpg'
        os.rename(filename, new_name)
    elif transF[1] == '.txt':
        new_name = transF[0] + '.py'
        os.rename(filename, new_name)


def transform(file_path):
    # 读取所有文件
    allFiles = os.listdir(file_path)
    for file in allFiles:
        file_path1 = os.path.join(file_path, file)
        if os.path.isdir(file_path1):
            transform(file_path1)
        else:
            os.chdir(file_path)
            Rename(file)


if __name__ == '__main__':
    # 文件夹路径
    file_path = "C:\\pyqt\\DATA\\1\\"
    transform(file_path)