# -*- coding: utf-8 -*-
# @Time    : 2020/11/19-16:45
# @Author  : 贾志凯    15716539228@163.com
# @File    : down.py
# @Software: win10  python3.6 PyCharm
from pathlib import Path
import os
from pysoftNLP.utils import down_resources
import zipfile
def down(url,my_file, zip_file):
    if not os.path.exists(my_file):
        if not zipfile.is_zipfile(zip_file):
            print('开始下载：', url)
            down_resources.download_decompress(url, zip_file)
        else:
            print("已有下载包！开始解压！")
            down_resources.unzip_file(zip_file)
    else:
        print("yes")


#下载预训练文件
def download_resource():
    path = 'D:\pysoftNLP_resources'
    if not os.path.exists(path):
        os.mkdir(path)
    #预训练的资源
    pre_training_file_file = Path("D:\pysoftNLP_resources\pre_training_file")
    pre_training_file_zip_file = "D:\pysoftNLP_resources\pre_training_file.zip"
    pre_training_file_url = 'https://github.com/xiaokai01/pysoftNLP/releases/download/0.0.4/pre_training_file.zip'
    down(pre_training_file_url,pre_training_file_file,pre_training_file_zip_file)

    # 分类模型资源
    classification_file = Path("D:\pysoftNLP_resources\classification")
    classification_zip_file = "D:\pysoftNLP_resources\classification.zip"
    classification_url = 'https://github.com/xiaokai01/pysoftNLP/releases/download/0.0.4/classification.zip'
    down(classification_url, classification_file, classification_zip_file)

    # 数据增强模型资源
    enhancement_file = Path("D:\pysoftNLP_resources\enhancement")
    enhancement_zip_file = "D:\pysoftNLP_resources\enhancement.zip"
    enhancement_url = 'https://github.com/xiaokai01/pysoftNLP/releases/download/0.0.4/enhancement.zip'
    down(enhancement_url, enhancement_file, enhancement_zip_file)

    # 关键字抽取模型资源
    extraction_file = Path("D:\pysoftNLP_resources\extraction")
    extraction_zip_file = "D:\pysoftNLP_resources\extraction.zip"
    extraction_url = 'https://github.com/xiaokai01/pysoftNLP/releases/download/0.0.4/extraction.zip'
    down(extraction_url, extraction_file, extraction_zip_file)

    # 命名实体识别模型资源
    entity_recognition_file = Path("D:\pysoftNLP_resources\entity_recognition")
    entity_recognition_zip_file = "D:\pysoftNLP_resources\entity_recognition.zip"
    entity_recognition_url = 'https://github.com/xiaokai01/pysoftNLP/releases/download/0.0.4/entity_recognition.zip'
    down(entity_recognition_url, entity_recognition_file, entity_recognition_zip_file)
