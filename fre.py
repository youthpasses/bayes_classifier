#!/usr/bin/python
# -*- coding:utf-8 -*-

import jieba

word_num_pre_list = []
word_allClass_list = []


def getWordDic(index):
    index_word_fre = 0
    word_dic = {}
    for i in xrange(100, 1000):
        #获得类index的wordDic
        #得到语料中的样本文档
        file_path = 'data/training/' + str(index) + '_' + str(i) + '.txt'
        if (i % 50) == 0:
            print file_path

        file_index_i = open(file_path, 'r')
        text = file_index_i.read()
        text = text.replace('腾讯科技', '')
        text = text.replace('腾讯财经', '')
        text = text.replace('腾讯体育', '')
        text = text.replace('腾讯汽车', '')
        text = text.replace('腾讯娱乐', '')
        text = text.replace('腾讯房产', '')
        text = text.replace('人民网', '')
        text = text.replace('新华网', '')
        text = text.replace('中新网', '')
        text = "".join(text.split())
        word_list = jieba.cut(text, cut_all=False)

        #停用词表
        file_s = open('data/stop.txt')
        stopwordlist = file_s.readlines()
        for j in xrange(0, len(stopwordlist)):
            stopword = stopwordlist[j].strip()
            stopwordlist[j] = stopword
        #遍历每个样本文档的单词，若不在停用词表则记录
        for word in word_list:
            word = word.strip().encode('utf-8')

            if word in stopwordlist:
                pass
            else:
                index_word_fre = index_word_fre + 1
                if word in word_dic:    #判断word是否统计过，如果在本文档中已经出现过，
                    word_dic[word] = word_dic[word] + 1
                else:
                    word_dic[word] = 1
                    if word not in word_allClass_list:
                        word_allClass_list.append(word)
    return word_dic, index_word_fre


def getWordFre(index):
    (wordDic, index_word_pre) = getWordDic(index)
    index_word_num = len(wordDic)

    print 'num = ' + str(index_word_num) + ', pre = ' + str(index_word_pre)
    word_num_pre_list.append(str(index_word_num))
    word_num_pre_list.append(str(index_word_pre))

    wordDicList = sorted(wordDic.iteritems(), key=lambda asd: asd[1], reverse=True)
    i_allwords_fre_path = 'medfiles/fre/' + str(index) + '_fre.txt'
    file_i_allwords_fre = open(i_allwords_fre_path, 'w')
    for word_fre in wordDicList:
            file_i_allwords_fre.write(word_fre[0] + ',' + str(word_fre[1]) + '\n')
    file_i_allwords_fre.close


def fre():
    for index in xrange(1, 8):
        getWordFre(index)
    file_word_num_allClass = open('medfiles/word_num_allClass.txt', 'w')
    word_num_allClass = len(word_allClass_list)
    file_word_num_allClass.write(str(word_num_allClass) + '\n')
    print word_num_pre_list
    for i in xrange(0, 13, 2):
        file_word_num_allClass.write(word_num_pre_list[i] + ',' + word_num_pre_list[i + 1] + '\n')
    file_word_num_allClass.close
    #heheda()


def heheda():
    print 'fre.fre() method has been exed ~ ~'
