# WeChatPush

基于itchat的微信消息接收端，感谢itchat大佬和itchat-uos开发。因为我有些地方需要更改就单独下载了itchat的包然后更改的。

你可以挂在服务器上或者电脑上，亦或者单片机上。

[itchat](https://github.com/littlecodersh/ItChat)

[itchat-uos](https://github.com/why2lyj/ItChat-UOS)

包自己导吧，环境文件我就不删了，嘻嘻。

⚠ 需要修改 itchat/config 内的 DINGTALK_WEBHOOK 为你的钉钉机器人 webhook 地址。

不接收的消息来自用户名写在 itchat/config BLOCK_NAME 数组里，包含关系，只需要输入前几位就行。

目前支持钉钉推送，快速回复需要在 FarPush 快速回复里填写你的服务器地址，像这样 http://192.168.0.1:9091/send。

快速查看语音或者图片请在快速回复里填入你的服务器地址 http://192.168.0.1:9091/send，这样后面的/send 不影响，会自动处理。

存储的文件在 files 文件夹内。

如果 window 等需要使用图片请在 main.py 里 itchat 参数内删掉 enablecmdqr。

后台运行请使用 nohup python3 main.py& tail -f nohup.out

[FarPush](www.coolapk.com/apk/com.farplace.farpush)

# FarPush 交流群 833957139

导入库 pip3 install -r requirements.txt

感谢分支 [WeChatPush](https://github.com/IlineI/WeChatPush) 消息的更多完善感谢@chase355 感谢

CentOS 还需要 yum install xdg-utils

# 欢迎 star 嘻嘻嘻 感谢您的帮助

我不会 python 所以就只在 itchat 基础上加了推送的代码

# 2023/2/6 

续费服务器和域名 2伯 服务器截至 2023/10月

# 2024/1/10

没钱续费服务器 
⚠ 我公开了服务器端的 jar 包以后大家就跑这个 jar 包到你的服务器吧 然后把 python 里的推送地址改成你的服务器 ip

再见

# 2024/2/28

小米商店上架了可分享内容的 app 咫尺妙享 或许很快又会再见😂
# 2024/9/21

新的服务器买好了一年期限 可以继续用推送了哈哈😄 

## 环境变量设置

在运行程序之前，请确保设置以下环境变量：
