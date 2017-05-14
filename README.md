# never forget checkin

#自动签到脚本

现支持 什么值得买, 网易云音乐, ss-panel, 大部分BBS（支持cookies和账号密码登陆方式）

#使用方法

首先安装python依赖  
```$pip(3) install -r requirements.txt```  
随后将config.json.simple改名为config.json并在config.json中输入相应信息  
```$cp(mv) config.json.simple config.json```  
```$vim(nano) config.json```  
运行  
```$python(3) checkin.py```  
将checkin.py加入systemd即可
