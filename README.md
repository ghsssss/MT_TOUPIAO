# MT
MT的自动投票功能，且可以推送到微信

使用方法：

1.安装requests，lxml，re，json，os依赖

2.青龙本地环境变量增加MT_COOKIE和PUSH_PLUS_TOKEN

3.定时器可以设置为每天请求一次，比如每天18点请求一次，corn表达式为0 18 * * *
