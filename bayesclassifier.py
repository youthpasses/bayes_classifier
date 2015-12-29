#!usr/bin/python
# -*- coding:utf-8 -*-

import os, sys
import math
import jieba
import parseurl

ABSPATH = os.path.abspath(sys.argv[0])
ABSPATH=os.path.dirname(ABSPATH) + '/'
print ABSPATH


def getPofClass(index, word_list):
    #输入类index的贝叶斯训练结果文件
    index_training_path = ABSPATH + 'bayes_training_outcome/' + str(index) + '_bayestraining.txt'
    file_index_training = open(index_training_path, 'r')
    dic_training = {}   #存储 index_bayestraining.txt 中的 (单词：P)
    training_word_p_list = file_index_training.readlines()
    allwords_fre_allwords_num = training_word_p_list[0].strip() #index_bayestraining.txt的第一行
    allwords_fre = int(allwords_fre_allwords_num[1])    #所有样本的所有单词的词频
    allwords_num = int(allwords_fre_allwords_num[0])    #所有样本的所有单词个数
    for i in xrange(1, len(training_word_p_list)):
        word_p = training_word_p_list[i].strip().split(',')
        dic_training[word_p[0]] = float(word_p[1])

    #遍历测试样本的wordlist，求每个Word的p
    p_list = []
    for word in word_list:
        word = word.strip()
        if word in dic_training:
            p_list.append(str(dic_training[word]))
        else:
            p_list.append(str(1.0 / (allwords_fre + allwords_num)))
    #计算P
    p_index = 0
    for p in p_list:
        p = math.log(float(p), 2)
        p_index = p_index + p
    return -p_index


def bayes(text):
    #rightIndex = int(filename.split('_')[0])
    #分词
    text = text.replace('腾讯科技', '')
    text = text.replace('腾讯财经', '')
    text = text.replace('腾讯体育', '')
    text = text.replace('腾讯汽车', '')
    text = text.replace('腾讯娱乐', '')
    text = text.replace('腾讯房产', '')
    text = text.replace('人民网', '')
    text = text.replace('新华网', '')
    text = text.replace('中新网', '')
    text = text.replace(' ', '')
    text = "".join(text.split())
    word_list = jieba.cut(text, cut_all=False)
    #停用词
    stopword_path = ABSPATH + 'data/stop.txt'
    file_stopword = open(stopword_path, 'r')
    stopword_list = file_stopword.readlines()
    for i in xrange(0, len(stopword_list)):
        word = stopword_list[i].strip()
        stopword_list[i] = word

    #去停用词
    word_list_nostop = []
    for word in word_list:
        word = word.strip().encode('utf-8')
        if word in stopword_list:
            pass
        else:
            word_list_nostop.append(word)
    #求每个类index的p
    max = 0
    maxIndex = 0
    for index in xrange(1, 8):
        y = getPofClass(index, word_list_nostop)
        #print str(index) + ':' + str(y)
        if y != float("inf") and y > max:
            max = y
            maxIndex = index
    return maxIndex


#从本地文件获取文本内容
def getTextFromNative(filename):
    #输入测试样本
    test_file_path = ABSPATH + 'data/test/' + filename
    file_test = open(test_file_path, 'r')
    text = file_test.read()
    return text


#测试本地文件
def nativeTest():

    #dir_path = 'data/test/'
    dir_path = os.path.join(os.path.dirname())
    file_list = os.listdir(dir_path)
    all_count = 0
    right_count = 0
    index_all_count = 0
    index_right_count = 0
    file_outcome = open(ABSPATH + 'outcome/outcome_native.txt', 'w')
    for filename in file_list:
        #去除隐藏文件
        a = filename.split('.')
        if a[1] == 'txt':
            all_count = all_count + 1
            index_all_count = index_all_count + 1
            b = filename.split('_')
            rightIndex = int(b[0])
            text = getTextFromNative(filename)
            getIndex = bayes(text)
            if getIndex == rightIndex:
                print filename + '----' + str(getIndex) + ' : right'
                right_count = right_count + 1
                index_right_count = index_right_count + 1
            else:
                print filename + '----' + str(getIndex) + ' : error'

            if index_all_count == 100:
                string = str(index_right_count) + ' / ' + str(index_all_count) + ' = ' + str(float(index_right_count) / index_all_count)
                print string
                file_outcome.write(string + '\n')
                index_all_count = 0
                index_right_count = 0

    string = str(right_count) + ' / ' + str(all_count) + ' = ' + str(float(right_count) / all_count)
    print string
    file_outcome.write(string)
    file_outcome.close()


def urlTest():
    file_urltest = open(ABSPATH + 'data/urltest.txt', 'r')
    index_url_list = file_urltest.readlines()
    print file_urltest.read()
    all_count = 0
    right_count = 1
    file_outcome = open(ABSPATH + 'outcome/outcome_url.txt', 'w')
    for index_url in index_url_list:
        index_url = index_url.strip().split('\\')
        index = int(index_url[0])
        url = index_url[1]
        text = parseurl.getTextFromUrl(url, index)
        text = text.strip()
        if len(text) == 0:
            continue
        all_count = all_count + 1
        getIndex = bayes(text)
        if index == getIndex:
            right_count = right_count + 1
        print str(index) + ' : ' + str(getIndex)
        file_outcome.write(str(index) + ',' + str(getIndex) + '\n')
    file_outcome.write(str(right_count) + ' / ' + str(all_count) + ' = ' + str(float(right_count) / all_count))
    file_outcome.close


#nativeTest()
urlTest()
