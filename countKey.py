import os
import re
from cProfile import Profile
import time

keyWords=["auto","break","case","char","const","continue","default","do",
         "double","else","enum","extern","float","for","goto","if",
         "int","long","register","return","short","signed","sizeof","static",
         "struct","switch","typedef","union","unsigned","void","volatile","while"]

#把代码文件内的注释部分以及引号内的内容删除
def remove(str):
    str = re.sub('(?<!:)\\/\\/.*|\\/\\*(\\s|.)*?\\*\\/',' ',str)    # 删除注释部分
    str = re.sub('\"([^\"]*)\"',' ',str)        # 删除带双引号的内容
    str = re.sub("\'([^\']*)\'", ' ', str)  # 删除带单引号的内容
    return str

#用正则表达式将非英文字符替换为空
def remove_non_letter(str):
    return re.sub('[^a-zA-Z]',' ',str)

# 删除列表中的空值
def del_empty(list):
    while '' in list:
        list.remove('')
    return list

#把文件内的单词分割为列表
def split_word(dir):
    f = open(dir, 'r', encoding='gbk')
    lines = f.readlines()
    new_line=""     # 用于记录文件内容的字符串
    for line in lines:
        if line != '' and line != '\n':  # 过滤掉空行
            new_line = new_line + line      # 把文件内容变成一个字符串

    new_line = remove(new_line)  # 去除注释部分以及引号的内容
    new_line = remove_non_letter(new_line)  # 去除非字母部分
    new_line = new_line.strip()  # 去除前后空格
    lis = new_line.split(" ")  # 分割成列表
    lis = del_empty(lis) # 删除列表中空值
    return lis

# 把if和对应else进行配对
def merge_if_else(list):
    if_else=[]    # 记录if-else结构的列表
    if_else.append(list[0])   #把if_else列表当成栈用
    for word in list[1:]:     #把else与其配对的if连接起来
        if word=="else":
            if if_else[-1]=="if":
                if_else.pop()
                if_else.append("if-else")
            else:
                if_else.append(word)
        else:
            if_else.append(word)
    #print(if_else)
    return if_else

        #把if-elseif_else进行配对

# 把if-elseif-else进行配对
def merge_if_elseif_else(list):
    if_elseif_else = []  # 记录if-elseif_else结构的列表
    if_elseif_else.append(list[0])  # 把if_elseif_else列表当成栈用
    for word in list[1:]:  # 把if_else与if_else连接起来
        if word == "if-else" and if_elseif_else[-1] != "if" and if_elseif_else[-1] != "else":
            if_elseif_else.pop()
            if_elseif_else.append("if-elseif-else")
        else:
            if_elseif_else.append(word)
    # print(if_elseif_else)
    return if_elseif_else

#按等级计算关键字字数
def count_key(dir,rank):
    word_list = split_word(dir)  # 获取单词列表
    keyword_list = []
    #rank1基础要求：输出关键字统计信息
    def rank_1():
        for word in word_list:
            if word in keyWords:  # 提取出关键字并存放到word_list中
                keyword_list.append(word)
                # continue
        print("total num: {0}".format(len(keyword_list)))

    # rank2进阶要求：输出有几组switch case结构，同时输出每组对应的case个数
    def rank_2():
        switch_case=[]
        for word in word_list:
            if word in ['switch','case']:        #提取出switch,case并存放到switch_case[ ]中
                switch_case.append(word)
        switch_num = 0  # 记录switch的数目
        case_num = []   # 记录case的数目
        for i in range(len(switch_case)):
            if switch_case[i] == "switch":
                switch_num += 1
                temp_case_num = 0
                for j in range(i+1,len(switch_case)):
                    if switch_case[j] == "case":
                        temp_case_num += 1
                    else:
                        break
                case_num.append(temp_case_num)

        print("switch num: {0}".format(switch_num))
        if (len(case_num) == 0):
            print("case num: 0")
        else:
            print("case num: ", end='')
            for num in case_num:
                print(str(num) + " ", end='')
            print()

    #rank3:拔高要求：输出有几组if-else结构
    def rank_3():
        ifOrElse = []  # 记录所有单个if，else的列表
        if_else_num=0   #记录if-else的数量
        for word in word_list:
            if word=="if" or word=="else":
                ifOrElse.append(word)     # 把所有的if else单独提取出来

        if_else = merge_if_else(ifOrElse)       # 逐步进行合并 先配对if-else
        if_elseif_else = merge_if_elseif_else(if_else)    #再配对if-elseif-else

        if(len(if_elseif_else)!=0):
            while("if-elseif-else" in if_elseif_else):  # 统计if-elseif-else
                for i in range(len(if_elseif_else)):
                    if if_elseif_else[i]=="if-elseif-else":
                        if_elseif_else[i]=""

                if_elseif_else=del_empty(if_elseif_else)     # 删除列表中的空值
                if(len(if_elseif_else)!=0):
                    if_else=merge_if_else(if_elseif_else)   #再次进行合并
                    if_elseif_else=merge_if_elseif_else(if_else)

        if(len(if_elseif_else)!=0):
            if_else = merge_if_else(if_elseif_else)     #对统计完if-elseif-else的列表进行合并
            while ("if-else" in if_else):  # 统计if-else的数目
                for i in range(len(if_else)):
                    if if_else[i] == "if-else":
                        if_else[i] = ""
                        if_else_num += 1

                if_else = del_empty(if_else)  # 删除列表中的空值
                if(len(if_else)!=0):
                    if_else = merge_if_else(if_else)  # 再次进行合并
        print("if-else num: {0}".format(if_else_num))  # if-else的数目

    #rank4:终极要求：输出有几组if-elseif-else结构
    def rank_4():
        ifOrElse = []  # 记录所有单个if，else的列表
        if_elseif_else_num = 0  # 记录if-elseif-else的数量
        for word in word_list:
            if word == "if" or word == "else":
                ifOrElse.append(word)   # 把所有的if else单独提取出来

        if_else = merge_if_else(ifOrElse)  # 逐步进行合并 先配对if-else
        if_elseif_else = merge_if_elseif_else(if_else)  # 再配对if-elseif-else

        if(len(if_elseif_else)!=0):
            while ("if-elseif-else" in if_elseif_else):  # 统计if-elseif-else的数目
                for i in range(len(if_elseif_else)):
                    if if_elseif_else[i] == "if-elseif-else":
                        if_elseif_else[i] = ""
                        if_elseif_else_num += 1

                if_elseif_else = del_empty(if_elseif_else)  # 删除列表中的空值
                if (len(if_elseif_else) != 0):
                    if_else = merge_if_else(if_elseif_else)  # 再次进行合并
                    if_elseif_else = merge_if_elseif_else(if_else)

        print("if-elseif-else num: {0}".format(if_elseif_else_num))  # if-elseif-else的数目

    if rank==1:
        rank_1()

    if rank==2:
        rank_1()
        rank_2()

    if rank==3:
        rank_1()
        rank_2()
        rank_3()

    if rank==4:
        rank_1()
        rank_2()
        rank_3()
        rank_4()

if __name__ == '__main__':
    basedir,rank=input("").split(" ")
    start_time = time.time()
    count_key(basedir,int(rank))
    time.sleep(1)
    print("\nRun Time: {0} seconds".format(time.time()-start_time))
