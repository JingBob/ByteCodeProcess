# 发布代码
1. git init
2. git add .
3. git commit -m "你的发布commit"
4. git remote add origin https://github.com/JingBob/ByteCodeProcess.git
6. git push -u origin master

# 更新仓库
### 第3步执行后若提示有冲突则先去解决带黄色感叹号的冲突文件可以考虑使用TortoiseGit 解决冲突后在执行执行4-6。没有冲突直接执行7。
1. git add .
2. git commit -m '日志内容'
3. git pull --rebase

4. git add .       # 或 git add 你修改的文件
5. git commit      # 这个commit的日志不会被提交
6. git rebase --continue # 建议不要使用git rebase --skip这个会忽略冲突将冲突标记（>>>>>>>>>>）一起提交

7. git push -u origin master


