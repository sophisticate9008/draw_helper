
import asyncio
import os
from configs.config import NICKNAME
from services.log import logger
from utils.data_utils import init_rank
from utils.message_builder import image , at
from nonebot import on_command
from nonebot.typing import T_State
from utils.utils import is_number
from utils.message_builder import custom_forward_msg
from nonebot.adapters.onebot.v11 import (
        GroupMessageEvent,
        MessageEvent,
        GROUP,
        Bot,
        Message,
        MessageSegment,
        PrivateMessageEvent
)
from nonebot.permission import SUPERUSER
import random
import time
from nonebot.params import CommandArg
from models.group_member_info import GroupInfoUser
from utils.utils import is_number
from ._model import info_helper_basic, info_helper_skin, helper_intact
import httpx
from lxml import etree
path_ = os.path.dirname(__file__)
path_.replace('\\', '/')
data_basic = str(path_) + '/basic.txt'
data_skin = str(path_) + '/skin.txt'
pub_link = 'https://prts.wiki/images/{}/{}{}/'
pub_basic = '立绘_{}_{}.png'
pub_skin = '立绘_{}_skin{}.png'

three_star = ['正义骑士号', "THRM-EX", '斑点', '泡普卡', '月见夜', '空爆', '梓兰', '史都华德', '安赛尔', '芙蓉', '炎熔', '安德切尔', '克洛丝', '米格鲁', '卡缇', 
                '玫兰莎', '翎羽', '香草', '芬', '12F', '杜林', '巡林者', '黑角', '夜刀', 'Castle-3', 'Lancet-2']
alphabet_list = ['a','b','c','d','e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'l', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
draw_cd = {}

__zx_plugin_name__ = "明日方舟助理"
__plugin_usage__ = """
usage:
    管理员私聊指令:
        更新干员数据（用于第一次载入,长时间没更新也可以用这个大量更新）
        更新干员数据 name(用于补全空缺和新增干员)
    抽干员:
        指令:
        抽干员
    设置助理:
        指令:
        我的助理
    查看助理所有立绘及皮肤
        指令:
        查看助理所有立绘及皮肤
    切换立绘/皮肤为默认形象
        指令:
        切换立绘[index]
""".strip()

__plugin_superuser_usage__ = """
usage:
    更新干员数据 ?干员名字
    不加名字默认所有,比较慢
""".strip()

__plugin_des__ = ""
__plugin_cmd__ = ["抽助理", "我的助理", "查看助理所有立绘", "切换立绘[index]"]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 1.0
__plugin_author__ = "冰蓝色光点"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["抽助理", "我的助理", "查看助理所有立绘", '切换立绘 [index]'],
}

update_list = on_command("更新干员数据", permission=SUPERUSER, priority=5, block=True)
draw_helper = on_command("抽助理",permission=GROUP, priority=5, block=True)
my_helper = on_command("我的助理",permission=GROUP, priority=5, block=True)
check_helper = on_command("查看助理所有立绘",permission=GROUP, priority=5, block=True)
switch_paint = on_command("切换立绘",permission=GROUP, priority=5, block=True)

@update_list.handle()
async def _(bot: Bot,
            event: PrivateMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    msg = args.extract_plain_text().strip()
    char_list = []
    count_out = 0
    msg = str(msg)
    iscontinue = 1
    if msg in char_list:
        iscontinue = 0
     
    while (len(char_list) < 250 and count_out < 10):
        role_list = []
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        url = 'https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E5%B9%B2%E5%91%98'
        try:
            for i in range(2):
                
                r = httpx.request('get',url=url, headers={'User-Agent': ua})

                # t = httpx.request('get',url='http://httpbin.org/get', headers={'User-Agent': ua})
                # print(t.text)

                parse_html = etree.HTML(r.text)
                xpath_char='//div[@class="mw-category-group"]/ul/li/a[@title=.]/text()'
                char_page=parse_html.xpath(xpath_char)
                role_list.extend(char_page)
                xpath_url1 = '//div[@id="mw-pages"]/a/@href'
                url_list=parse_html.xpath(xpath_url1)
                url = 'https://prts.wiki/' + url_list[0]
            char_list.extend(role_list)
        except:
            count_out += 1
    if len(char_list) < 250:
        await update_list.finish("未知错误")
    if msg in char_list:
        iscontinue = 0
    if iscontinue == 1:      
        try:
            with open(data_basic, 'r', encoding='utf-8') as ba:
                for i in ba:
                    arr_basic = i.split()
                    name = arr_basic[1]
                    is_exist = await info_helper_basic.is_exist(name)
                    if is_exist == 1:
                        logger.info(f"{name}基础信息已载入,跳过")
                        continue            
                    paint1 = arr_basic[2]
                    await info_helper_basic.store(name, paint1, 1)
                    logger.info(f"初始化载入{name}基础立绘1完成")
                    if name in three_star:
                        continue   
                    try:
                        paint2 = arr_basic[3]
                    except:
                        pass
                    if paint2 != '':
                        await info_helper_basic.store(name, paint2, 2)
                        logger.info(f"初始化载入{name}基础立绘2完成")
            with open(data_skin, 'r', encoding='utf-8') as sk:
                for i in sk:
                    arr_skin = i.split()
                    name = arr_skin[1]
                    is_exist = await info_helper_skin.is_exist(name)
                    if is_exist == 1:
                        logger.info(f"{name}皮肤信息已载入,跳过")
                        continue
                    skin = []
                    for j in range(2, 5):
                        try:
                            skin.append(arr_skin[j])
                        except:
                            pass
                    if len(skin) == 0:
                        await info_helper_skin.record_none(name, '')  
                        logger.info(f"{name}没有皮肤")                   
                        continue
                    for j in range(len(skin)):
                        await info_helper_skin.store(name, skin[j], j + 1)
                        ord = j + 1
                        logger.info(f"初始化载入{name}皮肤立绘{ord}完成")                            
        except:
            pass              
    if msg in char_list:
        logger.info(f"开始更新{msg}的基础信息")
        msg_list = [msg]
        try:
            await store(msg_list, 3, 0, 1)
        except:
            pass
        logger.info(f"开始更新{msg}的皮肤信息")
        try:
            await store(msg_list, 4, 1, 1)
        except:
            pass        
        await bot.send(event,f"更新{msg}信息完毕")
    else:
        logger.info("开始录入干员基础立绘信息....")
        try:
            await store(char_list, 3, 0, 0)
            await bot.send(event,'更新基础立绘信息完毕')
        except:
            await bot.send(event,"更新基础立绘信息完毕或出错停止")
        logger.info("开始录入干员皮肤立绘信息....")
        try:
            await store(char_list, 4, 1, 0)
            await bot.send(event,'更新皮肤立绘信息完毕')
        except:
            await bot.send(event,"更新皮肤立绘信息完毕或出错停止")
        
    
async def request(client, i, j, k, l, type):
    if type == 0:
        now = pub_basic
    if type == 1:
        now = pub_skin    
    link_splic = pub_link.format(k,k,l) + now.format(i, j)
    try: 
        r = await client.get(link_splic)
        if r.status_code == 200:
            if type == 0:     
                await info_helper_basic.store(i, link_splic, j)
                logger.info(f"{i}基础立绘{j}录入完毕")    
            else:
                await info_helper_skin.store(i, link_splic, j)
                logger.info(f"{i}皮肤立绘{j}录入完毕")        
    except:
        pass
    
#存储函数     
async def store(char_list, num, type, force):
    async with httpx.AsyncClient(timeout=5) as client:
        
        if type == 0:
            now = pub_basic
        if type == 1:
            now = pub_skin
        
        for i in char_list:
            is_exist = 0
            if force == 0:
                if type == 0:
                    is_exist = await info_helper_basic.is_exist(i)
                if type == 1:
                    is_exist = await info_helper_skin.is_exist(i)
            if is_exist == 1:
                continue
            for j in range(1, num):
                tasks_list = []
                if j == 2 and i in three_star:
                    break;
                for k in range(10):
                    for l in range(10):
                        tasks_list.append(request(client, i, j, k, l, type))         
                for k in range(10):
                    for l in alphabet_list:

                        tasks_list.append(request(client, i, j, k, l, type))                        


                for k in alphabet_list:
                    for l in range(10):
                        tasks_list.append(request(client, i, j, k, l, type))    
                        
                                     
                for k in alphabet_list:
                    for l in alphabet_list:
                        tasks_list.append(request(client, i, j, k, l, type)) 
                try:
                    await asyncio.gather(*tasks_list)
                except:
                    pass
            if type == 1:
                await info_helper_skin.record_none(i, '')    
                    
                    
@draw_helper.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id    
    global draw_cd
    try:
        if draw_cd[group]:
           pass 
    except KeyError:
        draw_cd[group] = {}
    try:
        if draw_cd[group][uid]:
            pass
    except KeyError:
        draw_cd[group][uid] = {}    
    try:
        time_pass = int (time.time() - draw_cd[group][uid]['time'])
        if time_pass < 180:
            time_rest = 180 - time_pass
            draw_refuse = [f'才过去了{time_pass}s时间,这样频繁变动人员会出问题的',
                           f'不行不行，你会伤了助理的心的，等{time_rest}s再换吧',
                           f'你的助理似乎还没有达到目的,暂时不想被换'
                           ]    
            
            await draw_helper.finish(random.choice(draw_refuse), at_sender=True)
    except KeyError:
        pass
    draw_cd[group][uid]['time'] = time.time()            

    name_list = await get_name_list()
    name = random.choice(name_list) 
    pic_url = await info_helper_basic.get_url(name)
    msg_tuple = (f'你的助理是{name}', image(pic_url), "请多多关照")
    await helper_intact.draw(group, uid, name)    
    await draw_helper.finish(Message(msg_tuple), at_sender=True)

    
                
async def get_name_list():
    query = await info_helper_basic.get_all_name()
    all_name = [id.name for id in query]
    return all_name


async def check_url(url):
    r = httpx.get(url)
    if r.status_code == 200:
        return True
    else:
        return False

async def get_helper_all_pic(name:str):
    list_select = []
    list_basic = await info_helper_basic.get_all_url(name)
    list_skin = await info_helper_skin.get_all_url(name)
    if list_basic != 0:
        for i in list_basic:
            if i != '' and await check_url(i):
                list_select.append(i)
    if list_skin != 0:
        for i in list_skin:
            if i != '':
                list_select.append(i)
    return list_select        

@my_helper.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    
    list_my = await helper_intact.my(group, uid)
    if list_my == 0:
        await my_helper.finish("你还没有抽助理",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
        
    pic_url = list_select[list_my[1] - 1]
    
    msg_tuple = (f'你当前的助理是{list_my[0]}', image(pic_url))
    await draw_helper.finish(Message(msg_tuple), at_sender=True)                    

@check_helper.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    list_my = await helper_intact.my(group, uid)
    if list_my == 0:
        await my_helper.finish("你还没有抽助理",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
    pic_num = len(list_select)  
    msg_list = ["你当前助理的立绘"]
    for i in range(pic_num):
         msg_list.append(image(list_select[i]))
    msg_tuple = tuple(msg_list)
    await check_helper.finish(Message(msg_tuple), at_sender=True)  
    
      
    
@switch_paint.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    msg = args.extract_plain_text().strip()
    list_my = await helper_intact.my(group, uid)
    if list_my == 0:
        await my_helper.finish("你还没有抽助理",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
    pic_num = len(list_select)  
    if is_number(msg):
        index = int(msg)
        if index >= 1 and index <= pic_num:
            await helper_intact.select(group, uid, index)
            await switch_paint.finish(f'默认立绘已经切换为{index}号立绘',at_sender = True)
        else:
            await switch_paint.finish('超出索引值', at_sender = True)
    else:
        await switch_paint.finish('不是数字', at_sender = True)
