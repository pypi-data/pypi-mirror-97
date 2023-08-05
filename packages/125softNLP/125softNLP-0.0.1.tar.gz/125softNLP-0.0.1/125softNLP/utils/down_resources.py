# -*- coding: utf-8 -*-
# @Time    : 2020/11/19-10:48
# @Author  : 贾志凯    15716539228@163.com
# @File    : down_resources.py
# @Software: win10  python3.6 PyCharm
from urllib import request, error
import sys
import zipfile
import tarfile
import socket

socket.setdefaulttimeout(15)
def progressbar(cur):
    percent = '{:.2%}'.format(cur)
    sys.stdout.write('\r')
    sys.stdout.write('[%-100s] %s' % ('=' * int(cur*100), percent))
    sys.stdout.flush()
    # print(cur)

def schedule(blocknum,blocksize,totalsize):
    '''
    blocknum:当前已经下载的块
    blocksize:每次传输的块大小
    totalsize:网页文件总大小
    '''
    percent = 0
    if totalsize == 0:
        percent = 0
    elif totalsize == -1 and blocknum==0:
        print('响应失败，正在重新连接……')
        download()
    elif totalsize == -1 and blocknum != 0:  #已经下载了，当前传输的为0， 可以忽略
        pass
    else:
        percent = blocknum * blocksize / totalsize
        progressbar(percent)
    if percent > 1.0:
        percent = 1.0
        progressbar(percent)
    # print('\n'+'download : %.2f%%' %(percent))


def download(url,path):
    try:
        filename,headers = request.urlretrieve(url, path, schedule)
        # print("headers",headers)
    except error.HTTPError as e:
        print(e)
        print(url + ' download failed!' + '\r\n')
        print('请手动下载：%s' %url)
    except error.URLError as e:
        print(url + ' download failed!' + '\r\n')
        print('请手动下载：%s' %url)
        print(e)
    except Exception as e:
        print(e)
        print('请手动下载：%s' %url)
    else:
        print('\r\n' + url + ' download successfully!')
        print('文件的名字：',filename)
        return filename
def unzip_file(zip_src):
    r = zipfile.is_zipfile(zip_src)
    dst_dir = str(zip_src).split('.')[0]
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
        fz.close()# 关闭文件，必须有，释放内存
    else:
        print('This is not zip')

def unzip(path):
    zip_file = zipfile.ZipFile(path)
    dst_dir = str(path).split('.')[0]
    zip_list = zip_file.namelist()  # 得到压缩包里所有文件
    for f in zip_list:
        zip_file.extract(f,dst_dir)  # 循环解压文件到指定目录
    zip_file.close()  # 关闭文件，必须有，释放内存

def untar(path = 'D:\pysoftNLP_resources\data.zip'):
    tar = tarfile.open(path)
    tar.extractall()
    tar.close()

def download_decompress(url,path):
    filename = download(url, path)

    try:
        if str(filename).split('.')[-1] == 'zip':
            print('开始解压zip文件，请等待……')
            # unzip()
            unzip_file(filename)
            print('解压完成，可以使用')
    except Exception as e:
        print(e)
        print('解压失败，请手动解压')
    try:
        if str(filename).split('.')[-1] == 'gz':
            print('开始解压tar.gz文件，请等待……')
            untar()
            print('解压完成，可以使用')
    except Exception as e:
        print(e)
        print('解压失败，请手动解压')

# if __name__ == '__main__':
# print('开始下载：https://codeload.github.com/chengtingting980903/zzsnML/tar.gz/1.0.0')
# download_decompress()
# print('开始下载：https://github.com/xiaokai01/download_test/releases/download/0.0.1/863_classify_hy_1024_9.zip')
# download_decompress(url='https://github.com/chengtingting980903/zzsnML/releases/download/1.0.0/data.zip', path='data.zip')
# download_decompress(url= 'https://github.com/xiaokai01/download_test/releases/download/0.0.1/863_classify_hy_1024_9.zip', path= 'D:\pysoftNLP_resources\data.zip')
