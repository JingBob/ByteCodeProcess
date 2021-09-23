#!/usr/bin/env python
# @Project ：dataprocess 
# @File    ：BuildKotlinPro.py
# @Author  ：
# @Date    ：2021/9/21 14:10 
# 
# --------------------------------------------------------
import os
from tqdm import tqdm

ProPath = "E:\kotlinProject\gradle\\101-200"
Prolist = next(os.walk(ProPath))[1]
i = 0
NowPath = os.getcwd()
for ProName in tqdm(Prolist[37:]):
    i = i + 1
    print("正在build第个%d项目：" % i, ProName)
    os.chdir(ProPath + "\\" + ProName)
    try:
        success = os.system("gradlew.bat")
        # 0表示执行成功
        if success == 0:
            try:
                success = os.system("gradlew.bat build")
                if success == 0:
                    with open(NowPath + "\\" + "buildsuccess.txt", 'a+', encoding='utf-8') as f:
                        f.write(ProPath + "\\" + ProName + "\n")
            except:
                print("Unkonwn error")
    except:
        print("Build Error")
    os.chdir(ProPath)
