# -*- encoding: utf-8 -*-
# tree.py - small tool to list of directories in a tree-like format.
# author: pwn4justice

import os
import sys
import getopt


filename=""
max_level=65535
space = 4
    

def usage():
    print("Usage: tree [-L level] [-ad] [-o filename]   ;; Notice: -L must before -a/-d!")
    print("\t[[[Copyright: @liubin]]]")
    print("")
    print('-' * 6, end="")
    print(" Listing options ", end="")
    print('-' * 6)

    print("-a \t\t\t All files are listed.")
    print("-d \t\t\t List directories only.")
    print("-L level \t\t Descend only level directories deep.")
    print("-o filename \t\t Output to file instead of stdout.")


def print_dir(path, level):
    #allfiles = os.listdir(os.getcwd())
    allfiles = os.listdir(path)
    for every in allfiles:
        if level <= max_level:
            if level == 0:
                print("|---", every)
            else:
                print("\r|"," " * space * level,"|---%s" % every)

            if os.path.isdir(every):

                os.chdir(every)
                tmp = level + 1
                print_dir(os.getcwd(), tmp)
                os.chdir("../")


def print_onlydir(path, level):
    allfiles = os.listdir(path)
    for every in allfiles:
        if level <= max_level:
            if os.path.isdir(every):
                if level == 0:
                    print("|---", every)
                else:
                    print("\r|"," " * space * level,"|---%s" % every)
                
                os.chdir(every)
                tmp = level + 1
                print_onlydir(os.getcwd(), tmp)
                os.chdir("../")
            else:
                continue
      
def write_to_file_a(f, path, level):
    allfiles = os.listdir(path)
    for every in allfiles:
        if level <= max_level:
            if level == 0:
                f.write("\n|---" + every)
            else:
                f.write("\r|" + " " * space * 2 * level + "|---%s" % every)

            if os.path.isdir(every):
                os.chdir(every)
                tmp = level + 1
                write_to_file_a(f, os.getcwd(), tmp)
                os.chdir("../")

def write_to_file_d(f, path, level):
    allfiles = os.listdir(path)
    for every in allfiles:
        if level <= max_level:
            if os.path.isdir(every):
                if level == 0:
                    f.write("\n|---" + every)
                else:
                    f.write("\r|" + " " * space * 2 * level + "|---%s" % every)
                
                os.chdir(every)
                tmp = level + 1
                write_to_file_d(f, os.getcwd(), tmp)
                os.chdir("../")
                
        
        
def main(path = '.'):
    args = sys.argv[1:]
    a_flag = 0
    d_flag = 0
    try:
        opts, args = getopt.getopt(args, "adL:o:", ["level=","output="])
    except getopt.GetoptError:
        print("getopt.GetoptError")
        usage()
        sys.exit(2) 

    print("PATH: %s" % path)
    print()
    for o, v in opts:
        if o in ('-a', ):
            a_flag = 1
            
            if d_flag:
                print("***Wrong Arguments.***")
                usage()
                sys.exit(2)
                
            # do all files list action
            print_dir(os.getcwd(), level = 0) 

        elif o in ('-d', ):
            d_flag = 1
            # test '-a' 
            if a_flag:
                print("***Wrong Arguments.***")
                usage()
                sys.exit(2)
            else:
                # do dir only action
                print_onlydir(os.getcwd(), level = 0)
            
        elif o in ('-L', '--level'):
            global max_level
            max_level = int(v)

        elif o in ('-o', '--output'):
            filename = v
            # do output thing
            with open(filename, "w+") as f:
                # rewrite!
                if a_flag:
                    write_to_file_a(f, os.getcwd(), level = 0)
                if d_flag:
                    write_to_file_d(f, os.getcwd(), level = 0)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(2)
    main() 


