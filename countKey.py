import os
import re
import time

keyWords=["auto","break","case","char","const","continue","default","do",
         "double","else","enum","extern","float","for","goto","if",
         "int","long","register","return","short","signed","sizeof","static",
         "struct","switch","typedef","union","unsigned","void","volatile","while"]

#用正则表达式将非英文字符替换为空
def removeNonLetter(str):
    return re.sub('[^a-zA-Z]',' ',str)

#把文件内的单词分割为列表
def splitWord(dir):
    lis = []  # 存放所有的单词
    f = open(dir, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        if line != '' and line != '\n':  # 过滤掉空行
            new_line = removeNonLetter(line)
            new_line = new_line.strip()  # 去除前后空格
            li = new_line.split(" ")
        for i in li:
            lis.append(i)
    return lis


#按等级计算关键字字数
def CountKey(dir,rank):
    lis = splitWord(dir)  # 获取单词列表
    word_list = []  # 存放关键字

    switch_index = []  # 记录switch所在的下标
    case_num = []  # 记录case的数量

    if_else = []    #记录所有if，else的列表

    #rank1基础要求：输出关键字统计信息
    def rank_1():
        for word in lis:
            if word in keyWords:        #提取出关键字并存放到word_list中
                word_list.append(word)
                #continue
        print("total num: {0}".format(len(word_list)))


    if rank==1:
        rank_1()



if __name__ == '__main__':
    start_time = time.time()
    basedir=r"C:\Users\MAC\Desktop\test.cpp"
    CountKey(basedir,1)
    # time.sleep(1)
    # print(time.time()-start_time)
    


