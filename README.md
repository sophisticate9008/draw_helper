
# draw_helper 转型为收集游戏 以前版本在releases
使用前需私聊执行   私聊:更新干员数据

以前下载过的 私聊 更新干员数据 刷新所有干员信息

剩下的看帮助

#
2022/10/24

获取语音函数新增三次试错机会，间隔两秒，

抽到六星或三个以上五星不撤回

#
2022/10/23

设置助理代码部分少个await


#
2022/10/20
修复真寻更新月卡出错

新增功能

![image](https://user-images.githubusercontent.com/94435821/196965135-713f9374-0a18-4f14-802b-7600a3070f93.png)

夜晚11.50猜语音的字典强制清空

#
2022/9/30

功能不多屁事一堆，下个插件我一定搞热更新，立绘超出索引改为显示默认立绘
#
2022/9/29

新增干员跳过皮肤录入的同时也记录为没有皮肤，防止下一次新增干员刷新后依然要更新皮肤 更新txt文件
#
2022/9/28

星级录入设为优先级最高
因为后面网络的大量请求会影响星级录入
#
2022/9/25
更新新功能把修改好的倒序覆盖了，从备份里捞了回来
修复自动消耗月卡

#

2022/9/24

新增黄票月卡功能
与签到同指令，
一天仅可触发一次
23：50后将不能签到自动减一天

#
2022/9/23
修复新增皮肤遇到没有先前皮肤的干员报错的问题
仅一行代码
可以等近期上线月卡功能后统一更新（设计卡片鸽了了一段时间）
#
2022/9/16

发现检测到新增干员后也跳过了星级录入

解决办法：更新代码 或 再次录入干员数据

另外存在错误的皮肤信息则会新增皮肤失败，需要强制更新干员
#
2022/9/15

修复昨晚的记录倒序bug

#
2022/9/14

新增 【更新干员数据 新增皮肤】功能， 自动更新全部新皮肤

检测新增干员跳过皮肤录入

我的干员 我的六星记录 根据星级将名字变为彩色并且改为倒叙排列

新增抽干员30秒后撤回

忘写了，所有立绘改为合并消息， 默认价格改为10


#
2022/9/4

闲的将星级录入改为异步（速度提升上十倍）（另外忘说了，txt信息录入后可以删掉txt，这样更新干员数据就不会有大量跳过提示了，这是一开始就设计好的）

2022/8/29

修复星级录入失败的问题，仅一行
增加干员录入失败跳过并提醒，增加容错

十连改为一张图片，解决风控问题

![RBITHWIY4MLT%VRS2`Z`HW8](https://user-images.githubusercontent.com/94435821/187234432-09b94c14-ee8f-4e4c-85c9-57f83eb57bd2.jpg)



#
2022/8/20
新增助理随机语音功能

