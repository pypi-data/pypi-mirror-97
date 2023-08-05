# -*- coding: utf-8 -*-
# @Time    : 2020/11/3-15:23
# @Author  : 贾志凯    15716539228@163.com
# @File    : mian.py
# @Software: win10  python3.6 PyCharm
import pandas as pd
import numpy as np
from pysoftnlp.classification.load_data import train_df, test_df
from keras.utils import to_categorical
from keras.models import Model
from keras.optimizers import Adam,SGD
from keras.layers import Input, BatchNormalization, Dense,Dropout,SeparableConv1D,Embedding,LSTM
from bert.extract_feature import BertVector
import time
import argparse
import os
#读取文件
def read_data(train_data, test_data):
    train_df = pd.read_csv(train_data)
    train_df.columns = ['id', 'label', 'text']
    test_df = pd.read_csv(test_data)
    test_df.columns = ['id', 'label', 'text']


args = {'encode':'bert','sentence_length':50,'num_classes':9,'batch_size':128,'epochs':100}
out_path = 'C:/Users/Administrator/Desktop'
def train(args,out_path):
    print('encoding开始！')
    star_encod_time = time.time()
    bert_model = BertVector(pooling_strategy="REDUCE_MEAN", max_seq_len=args.sentence_length)  # bert词向量
    f = lambda text: bert_model.encode([text])["encodes"][0]
    train_df['x'] = train_df['text'].apply(f)
    test_df['x'] = test_df['text'].apply(f)
    end_encod_time = time.time()
    print("encoding时间：%s" % (end_encod_time - star_encod_time))
    x_train = np.array([vec for vec in train_df['x']])
    x_test = np.array([vec for vec in test_df['x']])
    y_train = np.array([vec for vec in train_df['label']])
    y_test = np.array([vec for vec in test_df['label']])
    print('x_train: ', x_train.shape)

    y_train = to_categorical(y_train, args.num_classes)
    y_test = to_categorical(y_test, args.num_classes)

    x_in = Input(shape=(768,))
    x_out = Dense(1024, activation="relu")(x_in)
    x_out = BatchNormalization()(x_out)
    x_out = Dropout(0.2)(x_out)
    x_out = Dense(512, activation="relu")(x_out)
    x_out = BatchNormalization()(x_out)
    x_out = Dropout(0.2)(x_out)
    x_out = Dense(256, activation="relu")(x_out)
    x_out = BatchNormalization()(x_out)
    x_out = Dropout(0.2)(x_out)
    x_out = Dense(128, activation="relu")(x_out)
    x_out = BatchNormalization()(x_out)
    x_out = Dropout(0.2)(x_out)
    x_out = Dense(64, activation="relu")(x_out)
    x_out = BatchNormalization()(x_out)
    x_out = Dropout(0.2)(x_out)
    x_out = Dense(32, activation="relu")(x_out)
    x_out = BatchNormalization()(x_out)
    x_out = Dropout(0.2)(x_out)
    x_out = Dense(16, activation="relu")(x_out)
    x_out = BatchNormalization()(x_out)
    x_out = Dense(args.num_classes, activation="softmax")(x_out)
    model = Model(inputs=x_in, outputs=x_out)
    print(model.summary())

    model.compile(loss='categorical_crossentropy',  # categorical_crossentropy
                  optimizer=Adam(),  # adam
                  metrics=['accuracy'])

    # 模型训练以及评估
    model.fit(x_train, y_train, batch_size=args.batch_size, epochs=args.epochs)
    wenj = '863_classify_768' + '_' + str(args['sentence_length']) + '_' + str(args['num_classes']) + '_' + str(args['batch_size']) + '_' + str(args['epochs']) + '.h5'
    out_path = os.path.join(out_path, wenj)
    model.save(out_path)

    t3 = time.time()
    print("训练时间：%s" % (t3 - end_encod_time))
    print(model.evaluate(x_test, y_test))
    t4 = time.time()
    print('模型验证时长:', t4 - t3)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--status', choices=['train', 'test'], help='update algorithm', default='test')
#     parser.add_argument('--encode', choices=['bert','robert','word2vec','fasttxt'], help='词向量模型', default='bert')
#     parser.add_argument('--sentence_length',help='句子长度', default=50,type=int)
#     parser.add_argument('--num_classes', help='类别', type=int)#是几分类
#     parser.add_argument('--batch_size', help='类别', type=int,default=128)  # 是几分类
#     parser.add_argument('--epochs', help='类别', type=int, default=100)  # 是几分类
#     args = parser.parse_args()
#     print(args.status)
#     if args.status == 'train':
#         if args.encode == 'bert':
#             print('encoding开始！')
#             star_encod_time = time.time()
#             bert_model = BertVector(pooling_strategy="REDUCE_MEAN", max_seq_len = args.sentence_length) #bert词向量
#             f = lambda text: bert_model.encode([text])["encodes"][0]
#             train_df['x'] = train_df['text'].apply(f)
#             test_df['x'] = test_df['text'].apply(f)
#             end_encod_time = time.time()
#             print("encoding时间：%s" % (end_encod_time - star_encod_time))
#             x_train = np.array([vec for vec in train_df['x']])
#             x_test = np.array([vec for vec in test_df['x']])
#             y_train = np.array([vec for vec in train_df['label']])
#             y_test = np.array([vec for vec in test_df['label']])
#             print('x_train: ', x_train.shape)
#
#             y_train = to_categorical(y_train, args.num_classes)
#             y_test = to_categorical(y_test, args.num_classes)
#
#             x_in = Input(shape=(768,))
#             x_out = Dense(1024, activation="relu")(x_in)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dropout(0.2)(x_out)
#             x_out = Dense(512, activation="relu")(x_out)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dropout(0.2)(x_out)
#             x_out = Dense(256, activation="relu")(x_out)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dropout(0.2)(x_out)
#             x_out = Dense(128, activation="relu")(x_out)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dropout(0.2)(x_out)
#             x_out = Dense(64, activation="relu")(x_out)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dropout(0.2)(x_out)
#             x_out = Dense(32, activation="relu")(x_out)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dropout(0.2)(x_out)
#             x_out = Dense(16, activation="relu")(x_out)
#             x_out = BatchNormalization()(x_out)
#             x_out = Dense(args.num_classes, activation="softmax")(x_out)
#             model = Model(inputs=x_in, outputs=x_out)
#             print(model.summary())
#
#             model.compile(loss='categorical_crossentropy',  # categorical_crossentropy
#                           optimizer=Adam(),  # adam
#                           metrics=['accuracy'])
#
#             # 模型训练以及评估
#             model.fit(x_train, y_train, batch_size=args.batch_size, epochs=args.epochs)
#             model.save('863_classify_hy_1024_9.h5')
#
#             t3 = time.time()
#             print("训练时间：%s" % (t3 - end_encod_time))
#             print(model.evaluate(x_test, y_test))
#             t4 = time.time()
#             print('模型验证时长:',t4 - t3)


