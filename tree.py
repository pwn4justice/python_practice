# -*- encoding: utf-8 -*-
# tree.py - small tool to list of directories in a tree-like format.
# author: pwn4justice

import os
import sys
import getopt

# 全局变量
max_level=65535
space = 4
a_flag = 0
d_flag = 0  
buffer = ""

def usage():
    print("\nUsage: tree [-L level] [-ad] [-o filename] [-p path]")
    print("")
    print('-' * 6, end="")
    print(" Listing options ", end="")
    print('-' * 6)

    print("-a \t\t\t All files are listed.")
    print("-d \t\t\t List directories only.")
    print("-L level \t\t Descend only level directories deep.")
    print("-o filename \t\t Output to file instead of stdout.")
    print("-p path \t\t Specify a directory to list.")
    print("e.g.")
    print("\ttree.py -L 2 -a")
    print("\ttree -d")
    print("\ttree.py -L 2 -d -o a.txt")
    print("\ttree.py -L 1 -d -o a.txt -p C:\\\\")
    print("\ttree.py -L 1 -a -o D:\\\\a.txt -p C:\\\\")


# print_dir() 函数:
# path: 字符串,绝对路径
# level: 整数值,代表当前访问层次
def print_dir(path, level):                                       
    all_files = os.listdir(path)
    
    for every in all_files:
        # 最大层次管理,由 -L 参数指定
        if level <= max_level:      
            
            # 分水岭,输出所有文件还是只输出目录?
            if a_flag:   
                if level == 0:
                    print("|---", every)
                else:
                    # 层次打印
                    print("\r|"," " * space * level,"|---%s" % every)       
                    

            # isdir() 和 isfile() 等函数必须使用绝对路径作为参数
            file = os.path.join(path, every)
            
            # 如果设置了 d_flag
            if os.path.isdir(file) and d_flag:
                if level == 0:
                    print("|---", every)
                else:
                    print("\r|"," " * space * level,"|---%s" % every)   

            # 进入子目录
            if os.path.isdir(file):
                try:
                    os.chdir(file)
                    # 递归调用
                    print_dir(os.getcwd(), level + 1)
                    os.chdir(os.path.abspath('..'))
                except PermissionError:     
                    # 遇到权限问题,直接跳过,不处理
                    pass
            # 退出子目录


# dump() 函数:
# filename: 字符串,文件名
# path: 字符串,当前工作路径
# level: 整数值,代表当前访问层次
def dump(filename, path, level):
    all_files = os.listdir(path)
    
    # 构造一个缓冲区,先将结果存入缓冲区,再一次性写入文件,否则文件频繁读写浪费资源
    global buffer
    
    for every in all_files:
        if level <= max_level:
        
            
            # 如果是将所有文件名都写入
            if a_flag:   
                if level == 0:
                    buffer += '\n'
                    buffer += "|---%s" % every
                else:
                    buffer += "\r|"
                    buffer += "\t" * level
                    buffer += "|---%s" % every

            file = os.path.join(path, every)
            
            # 如果设置了 d_flag
            if os.path.isdir(file) and d_flag:
                if level == 0:
                    buffer += '\n'
                    buffer += "|---%s" % every
                else:
                    buffer += "\r|"
                    buffer += "\t" * level
                    buffer += "|---%s" % every
            
            if os.path.isdir(file):
                try:
                    os.chdir(file)
                    dump(filename, os.getcwd(), level + 1)
                    os.chdir(os.path.abspath('..'))
                except PermissionError:
                    pass

    # 如果递归回到了 level == 0 的状态,则将所有结果写入文件
    if level == 0:
        with open(filename, "w+") as f:
            f.write(buffer)



def main(path = '.'):
    filename = ""
    global a_flag
    global d_flag
    global max_level
    
    # 提取参数
    args = sys.argv[1:]

    try:
        opts, args = getopt.getopt(args, "adL:o:p:", ["level=","output=","path="])
    except getopt.GetoptError:
        print("getopt.GetoptError")
        usage()
        sys.exit(2) 
    
    # 解析参数,打印树状图的准备工作
    for o, v in opts:
    
        # 如果指定了 -a 选项
        if o in ('-a', ):
            # 设置全局变量 a_flag
            a_flag = 1
            
            # 如果同时指定了 d_flag,意味着出错了,-a和-d不能同时出现
            if d_flag:
                print("***Wrong Arguments.***")
                usage()
                sys.exit(2)

        # 如果指定了 -d 选项
        elif o in ('-d', ):
            # 设置全局变量 d_flag
            d_flag = 1
            
            # -a 和 -d 水火不容
            if a_flag:
                print("***Wrong Arguments.***")
                usage()
                sys.exit(2)
        
        # 如果指定了 -L 选项或者 --level
        elif o in ('-L', '--level'):
            max_level = int(v)

        # 如果用户指定了某一个特殊的工作目录
        elif o in ('-p', '--path'):       
            path = v
        
        #如果指定了 -o ,输出文件,如果用户故意指定-o "",则和没指定结果一样
        elif o in ('-o', '--output'):
            filename = v



    # 既没有指定 -a 也没有指定 -d, 则默认为 -a
    if not a_flag and not d_flag:
        a_flag = 1
    
    # 如果 -o 指定了,则不进行标准输出,否则进行标准输出 stdout 
    if filename != "":
        dump(filename, path, level = 0)
        #
        print("Write to %s Success." % filename)
    else:
        # 打印工作的目录
        print("*** PATH: %s ***" % path)
        print()
        print_dir(path, level = 0)


# 模块化代码
if __name__ == "__main__":

    # 如果没有任何参数,则退出
    if len(sys.argv) == 1:      
        usage()
        sys.exit(2)
    main() 


