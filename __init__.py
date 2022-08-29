

import asyncio
import os
import re
from unicodedata import name
import pypinyin

from configs.path_config import IMAGE_PATH
avatar_path = IMAGE_PATH / "draw_card" / "prts"
from utils.image_utils import text2image
from configs.config import NICKNAME
from services.log import logger
from utils.data_utils import init_rank
from utils.message_builder import image , at, record, text
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
from models.bag_user import BagUser
from ._model import info_helper_basic, info_helper_skin, helper_intact, helper_star, helper_collect, draw_price
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
        设置价格 群号 价格(默认50一抽,请根据群内金币膨胀情况设置)
    抽干员:
        单抽才有立绘
        十连抽为头像
        指令:
        抽干员
        抽干员 十连
    设置助理:
        从已有干员中设置助理
        指令:
        设置助理 name
    查看助理:
        指令:
        我的助理
    查看助理所有立绘及皮肤
        指令:
        查看助理所有立绘及皮肤
    切换立绘/皮肤为默认形象
        指令:
        切换立绘[index]
    助理随机语音:
        默认日文,可以在后面加中文参数
        指令:
        助理随机语音 ?[中文]
    我的干员:
        指令:
        我的干员
    我的六星记录
        指令:
        我的六星记录
    我的黄票:
        指令:
        我的黄票
    黄票兑换:
        180黄票兑换任意6星干员
        45黄票兑换任意5星干员
        指令:
        黄票兑换 name
""".strip()

__plugin_superuser_usage__ = """
usage:
    更新干员数据 ?干员名字
    不加名字默认所有,比较慢
""".strip()

__plugin_des__ = ""
__plugin_cmd__ = ["抽干员","设置助理", "我的助理", "查看助理所有立绘", "切换立绘[index]", '助理随机语音 ?[中文]', '我的干员', '我的黄票','黄票兑换']
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 1.0
__plugin_author__ = "冰蓝色光点"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["抽干员","设置助理", "我的助理", "查看助理所有立绘", '切换立绘 [index]', '助理随机语音 ?[中文]', '我的干员', '我的六星记录', '我的黄票', '黄票兑换'],
}

update_list = on_command("更新干员数据", permission=SUPERUSER, priority=5, block=True)
set_price = on_command("设置价格", permission=SUPERUSER, priority=5, block=True)
draw_char = on_command("抽干员",permission=GROUP, priority=5, block=True)
my_helper = on_command("我的助理",permission=GROUP, priority=5, block=True)
check_helper = on_command("查看助理所有立绘",permission=GROUP, priority=5, block=True)
switch_paint = on_command("切换立绘",permission=GROUP, priority=5, block=True)
voice = on_command("助理随机语音",permission=GROUP, priority=5, block=True)
set_helper = on_command("设置助理",permission=GROUP, priority=5, block=True)
my_char = on_command("我的干员",permission=GROUP, priority=5, block=True)
my_record = on_command("我的六星记录",permission=GROUP, priority=5, block=True)
my_ticket = on_command("我的黄票",permission=GROUP, priority=5, block=True)
ticket_convert = on_command("黄票兑换",permission=GROUP, priority=5, block=True)

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
    try:
        for i in char_list:
            if await helper_star.is_exist(i):
                continue
            try:
                star = await get_star(i)
            except:
                await bot.send(event, f"{i}录入星级出错跳过")
            await helper_star.star_record(i,star)
            logger.info(f"{i}星级为{star},录入")
        await bot.send(event,"干员星级录入完毕")
    except:
        await bot.send(event,"干员星级录入完毕")    
    
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

@set_price.handle()
async def _(bot: Bot,
            event: PrivateMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    msg = args.extract_plain_text().strip()
    msg_ = msg.split()
    try:
        if len(msg_) == 2:
            group = int(msg_[0])
            price = int(msg_[1])
            await draw_price.set_price(group,price)
            await set_price.finish("设置成功")
    except:
        pass
                    
@draw_char.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    msg = args.extract_plain_text().strip()
    uid = event.user_id
    group = event.group_id    
    price = await draw_price.get_price(group)
    gold_have = await BagUser.get_gold(uid, group)
    star_char = '★'
    if msg != '十连':
        if gold_have < price:
            await draw_char.finish(f"你的金币不够,一抽价格为{price}金币", at_sender = True)
        list_return = await draw_single(group, uid, price)
        name = list_return[0]
        star = list_return[1]
        star_str = star_char * star
        count_ = list_return[2] + 1
        ticket = list_return[3]
        no_six = list_return[4]
        pic_url = await info_helper_basic.get_url(name)
        msg_tuple = (f'你本次抽到的干员为{name}', image(pic_url), f"稀有度为{star_str}\n已经抽到次数为{count_}\n本次获得黄票数量为{ticket}\n累计{no_six}没有获得六星")
        await draw_char.finish(Message(msg_tuple), at_sender=True)
    else:
        price_ = price * 10
        if gold_have < price_:
            await draw_char.finish(f"你的金币不够,十抽抽价格为{price_}金币", at_sender = True)
        msg_list = []
        player = (await GroupInfoUser.get_member_info(uid, group)).user_name
        msg_list = await chain_reply_text(bot, msg_list, f'此为{player}的十连')
        for i in range(10):
            list_return = await draw_single(group, uid, price)
            name = list_return[0]
            star = list_return[1]
            star_str = star_char * star
            count_ = list_return[2] + 1
            ticket = list_return[3]
            pinyin = pypinyin.pinyin(name, style=pypinyin.NORMAL)
            pinyin_ = ''
            for i in pinyin:
                pinyin_ += i[0]
            pic = pinyin_ + '.png'
            avatar = avatar_path
            avatar_ = str(avatar.absolute()) + '/' + pic
            image_file = f"file:///{avatar_}"
            msg_list = await chain_reply(bot, msg_list, image_file, f"{name}[{star_str}]\n抽到次数为{count_}\n获得黄票{ticket}")
        await bot.send_group_forward_msg(group_id=group, messages=msg_list)
            

            
            
async def chain_reply(bot, msg_list, image, text:str):
    data = {
        "type": "node",
        "data": {
            "name": f"{NICKNAME}",
            "uin": f"{bot.self_id}",
            "content": [
                {"type": "text", "data": {"text": text}},
                {"type": "image", "data": {"file": image}},
            ],
        },
    }
    msg_list.append(data)
    return msg_list            

async def chain_reply_text(bot, msg_list, text:str):
    data = {
        "type": "node",
        "data": {
            "name": f"{NICKNAME}",
            "uin": f"{bot.self_id}",
            "content": [
                {"type": "text", "data": {"text": text}},
            ],
        },
    }
    msg_list.append(data)
    return msg_list    

async def draw_single(group, uid, price):
    await BagUser.spend_gold(uid, group, price)
    rand = random.randint(1, 100)
    ticket = 0
    list_ = []
    if await draw_assist(rand, 1, 2, 6, group, uid, 1, 10, 25 , list_):
        return list_
    if await draw_assist(rand, 93, 100, 5, group, uid, 1, 5, 13, list_):
        return list_
    if await draw_assist(rand, 43, 92, 4, group, uid, 1, 0, 1, list_):
        return list_
    if await draw_assist(rand, 3, 42, 3, group, uid, 1, 0, 0, list_):
        return list_

async def draw_assist(rand, rand_l, rand_r, star, group, uid, ticket_1, ticket_2, ticket_3, list_):
    list_choice = []
    star_ = star - 3
    list_choice.append(await get_star_list(3))
    list_choice.append(await get_star_list(4))
    list_choice.append(await get_star_list(5))
    list_choice.append(await get_star_list(6))
    
    six_record = await helper_collect.get_six_record(group, uid)
    if star == 6:
        more = six_record - 50
        if more > 0: 
            rand_r += more * 2 
    if rand >= rand_l and rand <= rand_r:
        name = random.choice(list_choice[star_])
        await helper_collect.role_record(group, uid, name)
        num = await helper_collect.get_num(group, uid, name)
        if num == 0:
            ticket = ticket_1
        if num > 0 and num <= 5:
            ticket = ticket_2
        if num > 5:
            ticket = ticket_3
        await helper_collect.add_ticket(group, uid, ticket)
        if star == 6:
            str_ = name + '_' + str(six_record + 1) + ' '
            await helper_collect.draw_record_(group, uid ,str_)
            await helper_collect.record_clear(group, uid)
        six_record = await helper_collect.get_six_record(group, uid)      
        list_.append(name)
        list_.append(star)
        list_.append(num)
        list_.append(ticket)
        list_.append(six_record)
        return True
    else:
        list_ = []
        return False
                
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

#设置助理

@set_helper.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    msg = args.extract_plain_text().strip()
    list_return = await helper_collect.get_all_num(group, uid)
    list_char = []
    if list_return:         
        for i in list_return:
            list_char.append(i[0])
        if msg in list_char:
            name = msg
            pic_url = await info_helper_basic.get_url(name)
            msg_tuple = (f'你的助理已经设置为{name}', image(pic_url))
            await helper_intact.draw(group, uid, name)    
            await set_helper.finish(Message(msg_tuple), at_sender=True)
        else:
            await set_helper.finish("你还没抽到该干员,不能设置该助理",at_sender = True)            
    else:
        await set_helper.finish("请先抽干员")

        
#我的助理    

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
        await my_helper.finish("你还没有设置助理",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
        
    pic_url = list_select[list_my[1] - 1]
    
    msg_tuple = (f'你当前的助理是{list_my[0]}', image(pic_url))
    await draw_char.finish(Message(msg_tuple), at_sender=True)                    

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
        await my_helper.finish("你还没有设置助理",at_sender = True)
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
        await my_helper.finish("你还没有设置助理",at_sender = True)
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


@voice.handle()
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
        await my_helper.finish("你还没有设置助理",at_sender = True)
    name = list_my[0]
    url_jp = 'https://static.prts.wiki/voice/{}/{}_{}.wav'
    url_cn = 'https://static.prts.wiki/voice_cn/{}/{}_{}.wav'
    url_text = 'https://prts.wiki/index.php?title={}/语音记录&action=edit'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    r = httpx.get(url=url_text.format(name), headers={'User-Agent': ua}, timeout=5)
    parse_html = etree.HTML(r.text)
    xpath_voice = '//textarea/text()'
    char_voice=parse_html.xpath(xpath_voice)
    texts = char_voice[0].split('\n\n')    
    key_text = texts[0]
    key = re.search('key=(.*)', key_text)
    key = key.groups()[0]    
    list_voice = []
    for i in texts:
        list_tmp = []
        results = re.search('=(.*)\n.*\|中文\|(.*)}}{{VoiceData/word\|日文\|',i)
        try:
            list_tmp.append(results.groups()[0])
            list_tmp.append(results.groups()[1])
            list_voice.append(list_tmp)
        except:
            pass
    voice_sel = random.choice(list_voice)
    voice_title = voice_sel[0]
    voice_text = voice_sel[1]
    url_voice = url_jp.format(key, name, voice_title)
    if msg == '中文':
        url_voice = url_cn.format(key, name, voice_title)  
        if await check_url(url_voice):
            await voice.send(record(url_voice))
            await voice.finish()
        else:
            await voice.finish('你当前的助理没有中文语音', at_sender = True)       
    await voice.send(record(url_voice))
    await voice.finish(voice_text)
    
async def get_star(name:str):
    url_pub = 'https://prts.wiki/index.php?title={}&action=edit'
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'    
    url_only = url_pub.format(name)
    r = httpx.request('get',url=url_only, headers={'User-Agent': ua}, timeout=5)
    parse_html = etree.HTML(r.text)
    xpath_char='//textarea/text()'
    info_page=parse_html.xpath(xpath_char)
    info_str = re.search('稀有度=(.*)',info_page[0])
    star = int(info_str.groups()[0]) + 1
    return star

async def get_star_list(star):
    query = await helper_star.get_star_list(star)
    all_name = [id.name for id in query]
    return all_name

@my_char.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    list_return = await helper_collect.get_all_num(group, uid)
    chaifen = int(len(list_return) / 30) + 1
    msg_list = []
    player = (await GroupInfoUser.get_member_info(uid, group)).user_name
    msg_list.append(f'此为{player}的干员情况')
    draw_count = await helper_collect.get_count(group, uid)
    msg_list.append(f'共抽了{draw_count}抽')
    for i in range(chaifen):
        text = ''
        for j in range(i * 30, (i + 1) * 30):
            try: 
                text = text + str(int(list_return[j][1]) + 1).ljust(30) + list_return[j][0] + '\n'
            except:
                break
        msg_list.append(image(b64=(await text2image(text, color="#f9f6f2", padding=10)).pic2bs4()))
        
    await bot.send_group_forward_msg(
        group_id=event.group_id, messages=custom_forward_msg(msg_list, bot.self_id)
    )

@my_record.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    list_return = await helper_collect.get_record(group, uid)
    chaifen = int(len(list_return) / 30) + 1
    msg_list = []
    player = (await GroupInfoUser.get_member_info(uid, group)).user_name
    msg_list.append(f'此为{player}的六星记录')
    for i in range(chaifen):
        text = ''
        for j in range(i * 30, (i + 1) * 30):
            try:
                text = text + list_return[j][1].ljust(30) + list_return[j][0] + '\n'
            except:
                break
        msg_list.append(image(b64=(await text2image(text, color="#f9f6f2", padding=10)).pic2bs4()))
    await bot.send_group_forward_msg(
        group_id=event.group_id, messages=custom_forward_msg(msg_list, bot.self_id)
    )
    
@my_ticket.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id 
    ticket = await helper_collect.get_ticket(group, uid)
    await my_ticket.finish(f"你的黄票数量为{ticket}", at_sender = True)

@ticket_convert.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    msg = args.extract_plain_text().strip()
    list_six = await get_star_list(6)
    list_five = await get_star_list(5)
    ticket_have = await helper_collect.get_ticket(group, uid)
    if msg in list_six:
        if ticket_have < 180:
            await ticket_convert.finish("黄票不足以兑换六星",at_sender = True)
        await helper_collect.ticket_convert(group, uid, 180)
        await helper_collect.role_record(group, uid, msg)
        await ticket_convert.finish(f"消耗180黄票成功兑换{msg}")
    if msg in list_five:
        if ticket_have < 45:
            await ticket_convert.finish("黄票不足以兑换五星",at_sender = True)
        await helper_collect.ticket_convert(group, uid, 45)
        await helper_collect.role_record(group, uid, msg)
        await ticket_convert.finish(f"消耗45黄票成功兑换{msg}")    
    await ticket_convert.finish("不支持兑换其他星级干员", at_sender = True)    
        

