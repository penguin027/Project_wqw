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

        # rank2进阶要求：输出有几组switch case结构，同时输出每组对应的case个数
        def rank_2():
            i = 0
            switch_num = 0  # 记录switch的数量
            for word in lis:
                if word == "switch":
                    switch_num += 1
                    switch_index.append(i)  # 记录switch的下标值
                i += 1
            print("switch num: {0}".format(switch_num))

            for i in range(len(switch_index)):
                case = 0
                if i != len(switch_index) - 1:
                    for j in range(switch_index[i], switch_index[i + 1]):
                        if (lis[j] == 'case'):
                            case += 1
                    case_num.append(case)
                if i == len(switch_index) - 1:
                    for j in range(switch_index[len(switch_index) - 1], len(lis)):
                        if (lis[j] == 'case'):
                            case += 1
                    case_num.append(case)
            print("case num: {0}".format(case_num))

        # rank3:拔高要求：输出有几组if else结构
        def rank_3():
            if_else_num = 0  # 记录if else的数量
            for word in lis:
                if word == "if" or word == "else":
                    if_else.append(word)
            print(if_else)
            for i in range(len(if_else)):
                if i != len(if_else) - 2 and i != len(if_else) - 1:  # 排除if_else列表的最后两个元素，否则可能越界
                    if if_else[i] == "if" and if_else[i + 1] == "else" and if_else[i + 1] != "if":
                        if_else[i] = ""
                        if_else[i + 1] = ""
                        if_else_num += 1
            print(if_else)
            print(if_else_num)

    if rank==1:
        rank_1()

    if rank==2:
        rank_1()
        rank_2()

    if rank==3:
        rank_1()
        rank_2()
        rank_3()



if __name__ == '__main__':
    start_time = time.time()
    basedir=r"C:\Users\MAC\Desktop\test.cpp"
    CountKey(basedir,3)
    
    # time.sleep(1)
    # print(time.time()-start_time)
    


