# WeChatPush

基于itchat的微信消息接收端 感谢itchat大佬 和itchat-uos开发 因为我有些地方需要更改就单独下载了itchat的包然后更改的

你可以挂在服务器上或者 电脑上 亦或者 单片机上 反正想咋玩就咋玩 微信真的毒瘤 消息推送迟迟不安排 难顶 😱

[itchat](https://github.com/littlecodersh/ItChat)

[itchat-uos](https://github.com/why2lyj/ItChat-UOS)

包自己导吧 环境文件我就不删了 嘻嘻

需要修改 itchat/config 内的 设备ID 和phone 0对应小米 1对应oppo 2对应华为 4对应腾讯推送 3对应fcm（服务器还没整）

不接收的消息来自用户名 写在itchat/config BLOCK_NAME 数组里 包含关系 只需要输入前几位就行

目前mipush 腾讯云推送 支持通知栏直接回复 需要的话 在itchat/config 里的 MES_THROUGH 改为 1 并且在FarPush 快速回复里填写你的服务器地址 像这样 http://192.168.0.1:9091/send
这样的话FarPush 在接收到透传消息 会发送支持回复的通知 然后通知你的服务器 发送消息 用的是python flask 端口默认在9091 可能需要您开启防火墙 或者自行更改端口


如果window 等需要使用图片请在main.py 里 itchat 参数内删掉 enablecmdqr

[FarPush](www.coolapk.com/apk/com.farplace.farpush)

# FarPush 交流群 833957139

如果运行失败 请导入 requests包 pyqrcode包 pypng包 flask包 gevent 包

感谢分支 [WeChatPush](https://github.com/IlineI/WeChatPush) 消息的更多完善感谢@chase355 感谢

CenterOS 还需要 yum install xdg-utils

# 欢迎star 嘻嘻嘻 感谢您的帮助

我不会python 所以就只在itchat基础上加了推送的代码

