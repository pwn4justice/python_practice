# -*- encoding: utf-8 -*-
# to convert chinese name to Pinying version
# author: pwn4justice
# date: 20","9/7/","8
# 待改进：1.转换后文本去重功能 2.添加 -o,指定输出文件

import sys

def compress():
    pass
    

def convert(fullname, filename=None):
    words = {
        "zhang": [ "章","张","长","丈","璋","樟" ],
        "li": [ "李","理","力","离","丽","利","莉","粒","黎","栗" ],
        "liu": [ "留","刘","流","六","柳","浏","琉" ],
        "wei": [ "为","位","微","伟","维","卫","威","魏","唯","韦","薇","巍","玮","炜","蔚","尉" ],
        "fang": [ "方","芳","昉","妨" ],
        "na": [ "娜","纳" ],
        "ming": [ "明","铭","鸣","名","茗" ],
        "jing": [ "静","景","京","井","晶","劲","敬","靖","菁","荆","婧" ],
        "jin" : [ "今","进","金","锦"],
        "kun" : [ "坤","昆" ],
        "wang": [ "王","旺","汪" ],
        "lei": [ "雷","磊" ],
        "yang": [ "杨","阳","羊","扬","央","漾","洋" ],
        "yan": [ "言","燕","艳","严","炎","研","岩","颜","彦","妍","闫","延" ],
        "yong": [ "永","勇","咏","庸","甬" ],
        "jun": [ "均","军","君","俊","骏","钧","郡","筠","竣","隽" ],
        "jie": [ "杰","姐","节","结","截","洁","婕","颉","劼" ],
        "qiang": [ "强","羌" ],
        "juan": [ "娟","鹃" ],
        "tao": [ "涛","桃","陶","韬","滔","焘" ],
        "min": [ "民","敏","闵","闽","旻","珉" ],
        "xiu": [ "修","秀","休" ],
        "lan": [ "兰","岚","澜" ],
        "gang": [ "刚","港","冈","罡","岡" ],
        "ping": [ "平","萍","苹" ],
        "hui": [ "辉","汇","慧","惠","晖","徽","卉","蕙" ],
        "cheng": [ "程","成","澄","城","诚","呈","承","丞" ],
        "chen": [ "陈","晨","宸","辰","琛" ],
        "lin": [ "林","琳","临","霖","麟" ],
        "ling": [ "灵","玲" ],
        "chao": [ "超","朝","晁" ],
        "hong": [ "红","宏","洪","鸿","虹","弘","泓" ],
        "gui": [ "贵","归","桂" ],
        "ying": [ "颖","英","应","莹","迎","盈","瑛" ],
        "yin": [ "因","银","音","印","尹","茵" ],
        "yu": [ "于","雨","玉","余","语","宇","羽","瑜" ],
        "peng": [ "鹏","彭","朋","蓬" ],
        "hua": [ "化","花","华" ],
        "fei": [ "非","飞","费","菲","霏" ],
        "mei": [ "美","梅","媚","玫" ],
        "xin": [ "新","心","鑫","信","欣","辛","馨","昕","忻","歆" ],
        "xing": [ "星","邢" ],
        "bo": [ "博","波","卜","玻" ],
        "bin": [ "斌","宾","彬" ],
        "bing": [ "冰","兵","秉" ],
        "hao": [ "号","浩","昊","郝","皓","豪" ],
        "kai": [ "凯","恺","铠" ],
        "zhen": [ "真","震","振","珍","甄" ],
        "jian": [ "建","健" ],
        "dan": [ "旦","丹" ],
        "xue": [ "雪","薛" ],
        "ning": [ "宁" ],
        "ting": [ "婷","亭","庭" ],
        "long": [ "龙","隆","泷" ],
        "feng": [ "冯","封","峰","凤","丰","锋","奉" ],
        "jia": [ "加","佳","贾","嘉","伽" ],
        "huang": [ "黄","煌" ],
        "shu": [ "树","叔","舒","淑" ],
        "zhi": [ "之","至","知","志","智","芝" ],
        "rong": [ "荣","容","蓉","融" ],
        "yun": [ "云","运","韵","芸","允" ],
        "hai": [ "海" ],
        "shuai": [ "帅" ],
        "chun": [ "纯","春","淳" ],
        "xiang": [ "想","向","项","香","相","祥","湘","襄" ],
        "guo": [ "国","果","郭","过" ],
        "ma": [ "马","玛" ],
        "qian": [ "钱","千","倩","茜","谦" ],
        "liang": [ "量","良","亮","梁" ],
        "zhao": [ "赵","兆","昭","召" ],
        "nan": [ "楠","娚" ],
        "sun": [ "孙" ],
        "fan": [ "范","凡","帆","樊" ],
        "zhou": [ "周","粥","舟" ],
        "han": [ "汗","韩","寒","涵","翰","晗" ],
        "wu": [ "吴","五","武","午","伍","邬","巫" ],
        "dong": [ "东","洞","冬","董" ],
        "huan": [ "环","欢","幻" ],
        "gao": [ "高","郜" ],
        "qin": [ "琴","秦","勤","钦","沁","覃","芹" ],
        "rui": [ "瑞","锐","睿","蕊" ],
        "chang": [ "常","昌","畅" ],
        "xu": [ "许","徐","旭" ],
        "xia": [ "夏","霞" ],
        "lu": [ "路","露","陆","鲁","卢","鹿","璐" ],
        "wen": [ "文","温","闻","雯","玟" ],
        "zhong": [ "中", "钟", "忠","仲" ]
    }
    
    for word in fullname:
        for key in words:
            #print(key)
            if word in words[key]:
                #print("---if---")
                fullname = fullname.replace(word, key)
                #print(id(fullname))
                break
    if filename == None:
        print(fullname) 
    try:
        with open(filename, "a+") as f:
            f.write(fullname)
    except Exception:
        pass

    
if __name__ == "__main__":
    
    if '-f' in sys.argv:
        index = sys.argv.index('-f')        #-f: 指定从哪个文件解析
        origin = sys.argv[index+1]
        filename = "pinying.txt"
        #start parsing...
        print("[*] Parsing from origin file: %s..." % origin)
        with open(origin, 'r') as f:
            name = f.readline()
            while name:
                ##print(name)
                convert(name, filename = filename)
                name = f.readline()
        ##end
        print("[*] Successfully save to file: %s" % filename)
        print("[*] Process End!")         
    elif len(sys.argv) == 1:
        origin = "names500.txt"
        filename = "pinying.txt"
        #start parsing...
        print("[*] Parsing defaule file: \'names500.txt\' ...")
        with open(origin, 'r') as f:
            name = f.readline()
            while name:
                ##print(name)
                convert(name, filename=filename)
                name = f.readline()
        ##end
        print("[*] Successfully save to file: %s" % filename)
        print("[*] Process End!")
    else:
        if len(sys.argv) == 2:
            convert(sys.argv[1])
        else:
            print("Usage")

   