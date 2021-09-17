import os
import re
import time

keyWords=["auto","break","case","char","const","continue","default","do",
         "double","else","enum","extern","float","for","goto","if",
         "int","long","register","return","short","signed","sizeof","static",
         "struct","switch","typedef","union","unsigned","void","volatile","while"]

#把代码文件内的注释部分以及print(）内的内容删除
def remove(str):
    index=0     #记录注释开始的位置
    if(len(str)>=2):
        for i in range(1,len(str)):     #去除注释部分
            if str[i]=='/' and str[i-1]=='/':
                index=i
                break
        str=str[:index-1]

    index=0     #记录print开始的位置
    if(len(str)>=5):
        for i in range(0,len(str)-4):     #去掉print内的内容
            if (str[i]=='p' and str[i+1]=='r' and str[i+2]=='i'
                and str[i+3]=='n' and str[i+4]=='t'):
                index=i
                break
            else:
                index=-1
        str=str[:index]
    return str

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
            new_line = remove(line)       # 去除注释部分以及print()的内容
            new_line = removeNonLetter(new_line)    # 去除非字母部分
            new_line = new_line.strip()  # 去除前后空格
            li = new_line.split(" ")    #每一行分割成列表
        for i in li:
            lis.append(i)       #汇总成一个列表
    return lis

# 删除列表中的空值
def delEmpty(list):
    while '' in list:
        list.remove('')
    return list

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
def CountKey(dir,rank):
    lis = splitWord(dir)  # 获取单词列表
    word_list = []  # 存放关键字

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
        switch_index = []  # 记录switch所在的下标
        case_num = []  # 记录case的数量
        switch_num=0    # 记录switch的数量
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

    #rank3:终极要求：输出有几组if-else结构
    def rank_3():
        ifelse = []  # 记录所有单个if，else的列表
        if_else_num=0   #记录if-else的数量
        for word in lis:
            if word=="if" or word=="else":
                ifelse.append(word)     # 把所有的if else单独提取出来

        if_else = merge_if_else(ifelse)       # 逐步进行合并 先配对if-else
        if_elseif_else = merge_if_elseif_else(if_else)    #再配对if-elseif-else

        while("if-elseif-else" in if_elseif_else):  # 统计if-elseif-else
            for i in range(len(if_elseif_else)):
                if if_elseif_else[i]=="if-elseif-else":
                    if_elseif_else[i]=""

            if_elseif_else=delEmpty(if_elseif_else)     # 删除列表中的空值
            if(len(if_elseif_else)!=0):
                if_else=merge_if_else(if_elseif_else)   #再次进行合并
                if_elseif_else=merge_if_elseif_else(if_else)

        if_else = merge_if_else(if_elseif_else)     #对统计完if-elseif-else的列表进行合并
        while ("if-else" in if_else):  # 统计if-else的数目
            for i in range(len(if_else)):
                if if_else[i] == "if-else":
                    if_else[i] = ""
                    if_else_num += 1

            if_else = delEmpty(if_else)  # 删除列表中的空值
            if(len(if_else)!=0):
                if_else = merge_if_else(if_else)  # 再次进行合并
        print("if-else num: {0}".format(if_else_num))  # if-else的数目

    #rank4:拔高要求：输出有几组if-elseif-else结构
    def rank_4():
        ifelse = []  # 记录所有单个if，else的列表
        if_elseif_else_num = 0  # 记录if-elseif-else的数量
        for word in lis:
            if word == "if" or word == "else":
                ifelse.append(word)   # 把所有的if else单独提取出来

        if_else = merge_if_else(ifelse)  # 逐步进行合并 先配对if-else
        if_elseif_else = merge_if_elseif_else(if_else)  # 再配对if-elseif-else

        while ("if-elseif-else" in if_elseif_else):  # 统计if-elseif-else的数目
            for i in range(len(if_elseif_else)):
                if if_elseif_else[i] == "if-elseif-else":
                    if_elseif_else[i] = ""
                    if_elseif_else_num += 1

            if_elseif_else = delEmpty(if_elseif_else)  # 删除列表中的空值
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
    basedir,rank=input("请输入文件路径 完成等级:\n").split(" ")
    #basedir=r"C:\Users\MAC\Desktop\test.cpp"
    start_time = time.time()
    CountKey(basedir,int(rank))
    #print(time.time()-start_time)

