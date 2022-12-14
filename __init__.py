import asyncio
import base64
from io import BytesIO
import os
import re
import pypinyin
import httpx
from typing import List, Dict, Optional
from utils.http_utils import AsyncHttpx
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from utils.manager import withdraw_message_manager
from utils.decorator.shop import shop_register
import nonebot
from nonebot import Driver
driver: Driver = nonebot.get_driver()
from nonebot.plugin import require
from utils.utils import scheduler
from configs.path_config import IMAGE_PATH, FONT_PATH
yuanshen_ttf = str(FONT_PATH / "yuanshen.ttf")
avatar_path = IMAGE_PATH / "draw_card" / "prts"
from utils.image_utils import text2image
from configs.config import NICKNAME
from services.log import logger
from utils.data_utils import init_rank
from utils.message_builder import image , at, record, text
from nonebot import on_command, on_shell_command, on_message
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
from nonebot.params import CommandArg, ShellCommandArgs, Arg
from models.group_member_info import GroupInfoUser
from utils.utils import is_number,get_message_img, get_message_text
from models.bag_user import BagUser
from argparse import Namespace
from ._model import info_helper_basic, info_helper_skin, helper_intact, helper_star, helper_collect, draw_price, moon_card_prts
from lxml import etree
from .pic_make import pic_make_, revise_size_h

from datetime import datetime, timedelta
from nonebot.rule import ArgumentParser
from nonebot.matcher import Matcher
from hashlib import md5
path_ = os.path.dirname(__file__)
path_.replace('\\', '/')
data_basic = str(path_) + '/basic.txt'
data_skin = str(path_) + '/skin.txt'
pub_link = 'https://prts.wiki/images/{}/{}{}/'
pub_basic = '??????_{}_{}.png'
pub_skin = '??????_{}_skin{}.png'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
skin_top = 7
three_star = ['???????????????', "THRM-EX", '??????', '?????????', '?????????', '??????', '??????', '????????????', '?????????', '??????', '??????', '????????????', '?????????', '?????????', '??????', 
                '?????????', '??????', '??????', '???', '12F', '??????', '?????????', '??????', '??????', 'Castle-3', 'Lancet-2']
alphabet_list = ['a','b','c','d','e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'l', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


__zx_plugin_name__ = "??????????????????"
__plugin_usage__ = """
usage:
    ?????????????????????:
        ??????????????????????????????????????????,???????????????????????????????????????????????????
        ?????????????????? name(?????????????????????????????????)
        ?????????????????? ????????????(??????????????????????????????)
        ???????????? ?????? ??????(??????10??????,???????????????????????????????????????)
    ?????????:
        ??????????????????
        ??????????????????
        ??????:
        ?????????
        ????????? ??????
    ????????????:
        ??????????????????????????????
        ??????:
        ???????????? name
    ????????????:
        ??????:
        ????????????
    ?????????????????????????????????
        ??????:
        ????????????????????????
    ????????????/?????????????????????
        ??????:
        ????????????[index]
    ?????????????????????????????????:
        ????????????-n ???????????? -t ???????????? -l ???cn, jp
        ????????????????????????????????????
        ?????? ???????????? -n ????????? -l cn -t ?????? (?????????????????????)
    ???????????????
        ???????????? -x ???????????? -n ????????????
        ?????? ???????????? -n ????????? -x 2 (?????????????????????????????????????????????)
    ????????????????????????????????????
        ??????:???????????????
        ??????????????????????????????
        ?????????????????????????????????????????????
        ?????????????????????????????????????????????????????????bug????????????????????????????????????
        ?????????????????????????????????
    ????????????:
        ??????:
        ????????????
    ??????????????????
        ??????:
        ??????????????????
    ????????????:
        ??????:
        ????????????
    ????????????:
        180??????????????????6?????????
        45??????????????????5?????????
        ??????:
        ???????????? name
    ??????:
        23:50???????????????????????????????????????
        ????????????????????????
""".strip()

__plugin_superuser_usage__ = """
usage:
    ?????????????????? ?????????????
    ????????????????????????,?????????
""".strip()

__plugin_des__ = ""
__plugin_cmd__ = ["?????????","????????????", "????????????", "????????????????????????", "????????????[index]", "????????????", '????????????',"??????????????????", '????????????','????????????']
__plugin_type__ = ("???????????????")
__plugin_version__ = 1.0
__plugin_author__ = "???????????????"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["?????????","????????????", "????????????", "????????????????????????", '???????????? [index]', "????????????", '????????????', '??????????????????', '????????????', '????????????'],
}
guess_voice = {}
helper_par = ArgumentParser(add_help=False)
helper_par.add_argument("-n", "--name", default="default", help="????????????,???????????????")
helper_par.add_argument("-x", "--index",type=int, default=1, help="????????????,?????????1")
helper_par.add_argument("-l", "--longuage",default="jp",help="?????????,??????jp, ??????cn")
helper_par.add_argument("-t", "--title", default="default",help="????????????,??????????????????")



update_list = on_command("??????????????????", permission=SUPERUSER, priority=5, block=True)
set_price = on_command("????????????", permission=SUPERUSER, priority=5, block=True)
draw_char = on_command("?????????",permission=GROUP, priority=5, block=True)
my_helper = on_command("????????????",permission=GROUP, priority=5, block=True)
check_helper = on_command("????????????????????????",permission=GROUP, priority=5, block=True)
switch_paint = on_command("????????????",permission=GROUP, priority=5, block=True)
set_helper = on_command("????????????",permission=GROUP, priority=5, block=True)
my_char = on_command("????????????",permission=GROUP, priority=5, block=True)
my_record = on_command("??????????????????",permission=GROUP, priority=5, block=True)
my_ticket = on_command("????????????",permission=GROUP, priority=5, block=True)
ticket_convert = on_command("????????????",permission=GROUP, priority=5, block=True)
check_in = on_command("??????",permission=GROUP, priority=3, block=False)
painting = on_shell_command(
    "????????????", aliases={"????????????"}, permission=GROUP, priority=5, block=True, parser=helper_par
)
voice = on_shell_command(
    "????????????", aliases={"??????????????????"}, permission=GROUP, priority=5, block=True, parser=helper_par
)


def get_game_status(event:GroupMessageEvent):
    global guess_voice
    group = event.group_id
    return bool(guess_voice.get(group))

async def jishiqi(group):
    global guess_voice
    cd = guess_voice[group]["cd"]
    while cd > 0:
        guess_voice[group]["cd"] = cd
        cd -= 1
        await asyncio.sleep(1)
    guess_voice[group]["cd"] = None

command_prompt = on_command("????????????", rule=get_game_status,permission=GROUP,priority=5, block=True)
@command_prompt.handle()
async def _(bot: Bot,
    event: GroupMessageEvent,
    state: T_State,
    args: Message = CommandArg(),
):
    global guess_voice
    group = event.group_id
    name = guess_voice[group]["name"]
    print(guess_voice)
    if guess_voice[group].get("cd"):
        cd = guess_voice[group].get("cd")
        await command_prompt.finish(f"cd???,???{cd}s?????????")
    else:
        try:
            list_voice = await get_record_text(name, "??????")
        except:
            await command_prompt.send("??????????????????,???????????????,?????????")
        list_voice.remove(list_voice[2])
        cn_url = list_voice[0]
        if not await check_url(cn_url):
            list_voice.remove(list_voice[0])
        await command_prompt.send(record(random.choice(list_voice)))
        guess_voice[group]["cd"] = 10
        await jishiqi(group)
    
            
            
command_stop = on_command("???????????????",rule=get_game_status, permission=GROUP,priority=5, block=True)
@command_stop.handle()
async def _(bot: Bot,
    event: GroupMessageEvent,
    state: T_State,
    args: Message = CommandArg(),
):
    print("???????????????")
    group = event.group_id
    global guess_voice
    name = guess_voice[group].get("name")
    guess_voice[group] = {}
    await command_stop.finish(f"?????????{name},????????????")
        

begin_guess = on_command("???????????????", permission=GROUP, priority=5, block=True)
@begin_guess.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    global guess_voice
    group = event.group_id
    price = await draw_price.get_price(group)
    if get_game_status(event):
        await begin_guess.finish("??????????????????")
    else:
        guess_voice[group] = {}
        name = random.choice(await get_name_list())
        print(name) #?????????
        guess_voice[group]["name"] = name
        count = 0
        try:
            list_voice = await get_record_text(name, "??????")
        except:
            await begin_guess.send("????????????,???????????????")
        list_voice.remove(list_voice[2])
        cn_url = list_voice[0]
        if not await check_url(cn_url):
            list_voice.remove(list_voice[0])
        await begin_guess.send(record(random.choice(list_voice)))
        guess_voice[group]["time"] = 120
        while count < 120:
            if get_game_status(event):
                count += 1
                if guess_voice[group].get("win_uid"):
                    uid = guess_voice[group]["win_uid"]
                    winner = (await GroupInfoUser.get_member_info(uid, group)).user_name
                    await BagUser.add_gold(uid, group, price * 3)
                    gold = price * 3
                    guess_voice[group] = {}
                    await begin_guess.finish(f"??????{winner}?????????,?????????{name},??????{gold}??????")
                await asyncio.sleep(1)
            else:
                return
        guess_voice[group] = {}
        await begin_guess.finish(f"?????????,?????????{name},????????????")
            
guess = on_message(permission=GROUP, priority=996, rule=get_game_status)
@guess.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            ):
    group = event.group_id
    uid = event.user_id
    msg = get_message_text(event.json())
    global guess_voice
    name = guess_voice[group]["name"]
    if guess_voice[group].get("win_uid"):
        pass
    else:
        if msg == name:
            guess_voice[group]["win_uid"] = uid
        
@painting.handle()
async def _(
    bot: Bot,
    event: GroupMessageEvent,
    state: T_State,
    args: Namespace = ShellCommandArgs(),
):
    group = event.group_id
    uid = event.user_id
    if args.name == "default":
        list_my = await helper_intact.my(group, uid)
        if list_my == 0:
            await voice.finish("????????????????????????",at_sender = True)
        else:
            list_select = await get_helper_all_pic(list_my[0])
        try:
            pic_url = list_select[args.index - 1]
            await painting.send(image(pic_url),at_sender=True)
        except:
            await painting.finish("??????????????????") 
    else:
        list_role = await get_all_have(group, uid)
        if args.name in list_role:
            list_select = await get_helper_all_pic(args.name)
            try:
                pic_url = list_select[args.index - 1]
                await painting.send(image(pic_url),at_sender=True)
            except:
                await painting.finish("??????????????????")
        else:
            await painting.finish("????????????????????????????????????????????????",at_sender=True)         



@voice.handle()
async def _(
    bot: Bot,
    event: GroupMessageEvent,
    state: T_State,
    args: Namespace = ShellCommandArgs(),
):
    group = event.group_id
    uid = event.user_id
    if args.name == "default":
        list_my = await helper_intact.my(group, uid)
        if list_my == 0:
            await voice.finish("????????????????????????",at_sender = True)
        else:
            name_ = list_my[0]
            list_voice = await get_record_text(name_, args.title)
            if "cn" in args.longuage:
                url_voice = list_voice[0]
                if await check_url(url_voice):
                    await voice.send(record(url_voice))
                    return
                else:
                    await voice.finish('????????????????????????????????????', at_sender=True)                
            url_voice = list_voice[1] 
            await voice.send(record(url_voice))
            voice_text = list_voice[2]
            await voice.finish(voice_text)                
                
    else:
        list_role = await get_all_have(group, uid)
        if args.name in list_role:
            list_voice = await get_record_text(args.name, args.title)
            if "cn" in args.longuage:
                url_voice = list_voice[0]
                if await check_url(url_voice):
                    await voice.send(record(url_voice))
                    return
                else:
                    await voice.finish('???????????????????????????????????????', at_sender=True)                
            url_voice = list_voice[1] 
            await voice.send(record(url_voice))
            voice_text = list_voice[2]
            await voice.finish(voice_text)   
        else:
            await voice.finish("????????????????????????????????????????????????",at_sender=True)

            
            
        

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
    if any(key in msg for key in["????????????","????????????????????????"]):
        iscontinue = 0
    while (len(char_list) < 250 and count_out < 10):
        role_list = []
        url = 'https://prts.wiki/w/%E5%88%86%E7%B1%BB:%E5%B9%B2%E5%91%98'
        try:
            for i in range(2):
                
                r = await AsyncHttpx.get(url=url)

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
        await update_list.finish("????????????")

    if iscontinue == 1:
        async with httpx.AsyncClient(headers={'User-Agent': ua},timeout=5) as client:
            tasks_list = []  
            for i in char_list:
                if await helper_star.is_exist(i):
                    continue
                tasks_list.append(get_star(client, i, bot, event))
            try:
                await asyncio.gather(*tasks_list)
            except:
                pass
        
        for name in char_list:
            is_exist = await info_helper_basic.is_exist(name)
            if is_exist == 1:
                continue
            basic_ = await get_basic(name)
            for i in range(len(basic_)):
                await info_helper_basic.store(name, basic_[i], i + 1)
                logger.info(f"{name}????????????{i + 1}????????????")
            
        for name in char_list:
            is_exist = await info_helper_skin.is_exist(name)
            if is_exist == 1:
                continue            
            skin_ = await get_skin(name)
            for i in range(len(skin_)):
                await info_helper_skin.store(name, skin_[i], i + 1)
            logger.info(f"{name}????????????????????????")
    elif msg in char_list:
        name = msg
        basic_ = await get_basic(name)
        for i in range(len(basic_)):
            await info_helper_basic.store(name, basic_[i], i + 1)
        logger.info(f"{name}????????????????????????")
        skin_ = await get_skin(name)
        for i in range(len(skin_)):
            await info_helper_skin.store(name, skin_[i], i + 1)
        logger.info(f"{name}????????????????????????")
    elif msg == "????????????????????????":
        for name in char_list:
            await info_helper_basic.clear(name)
            basic_ = await get_basic(name)
            for i in range(len(basic_)):
                await info_helper_basic.store(name, basic_[i], i + 1)
            logger.info(f"{name}????????????????????????")
        for name in char_list:           
            skin_ = await get_skin(name)
            for i in range(len(skin_)):
                await info_helper_skin.store(name, skin_[i], i + 1)
            logger.info(f"{name}????????????????????????")
    await update_list.finish("????????????")  
async def get_basic(name: str):
    list_ = []
    for i in range(1, 3):
        if i == 2 and name in three_star:
            break
        path_ = get_path(f"??????_{name}_{i}.png")
        list_.append(path_)
    return list_
       
async def get_skin(name:str):
    list_ = []
    for i in range(1, skin_top):
        path_ = get_path(f"??????_{name}_skin{i}.png")
        list_.append(path_)
    return list_

def get_avatar(name:str, index_:int):
    path_ = get_path(f"??????_{name}_skin{index_}.png")
    if index_ == 0:
        path_ = get_path(f"??????_{name}.png")
    return path_

def get_path(path:str):
    h1 = md5()
    h1.update(path.encode("utf-8"))
    md5_ = str(h1.hexdigest())
    return pub_link.format(md5_[0], md5_[0], md5_[1]) + path

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
            await set_price.finish("????????????")
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
    star_char = '???'
    if msg != '??????':
        if gold_have < price:
            await draw_char.finish(f"??????????????????,???????????????{price}??????", at_sender = True)
        list_return = await draw_single(group, uid, price)
        name = list_return[0]
        star = list_return[1]
        star_str = star_char * star
        count_ = list_return[2] + 1
        ticket = list_return[3]
        no_six = list_return[4]
        pic_url = await info_helper_basic.get_url(name)
        msg_tuple = (f'???????????????????????????{name}', image(pic_url), f"????????????{star_str}\n?????????????????????{count_}\n???????????????????????????{ticket}\n??????{no_six}??????????????????")
        msg_id = await draw_char.send(Message(msg_tuple), at_sender=True)
        try:
            if star != 6:                
                withdraw_message_manager.withdraw_message(
                    event,
                    msg_id,
                    (60, 1)
                )

        except:
            pass
    else:
        price_ = price * 10
        if gold_have < price_:
            await draw_char.finish(f"??????????????????,??????????????????{price_}??????", at_sender = True)
        msg_list = []
        player = (await GroupInfoUser.get_member_info(uid, group)).user_name
        list_list = []
        six_num = 0
        five_num = 0
        for i in range(10):
            list_return = await draw_single(group, uid, price)
            if list_return[1] == 5:
                five_num += 1
            if list_return[1] == 6:
                six_num += 1
            list_list.append(list_return)
        msg_id = await draw_char.send(image(b64 = pic2b64(await buide_image(list_list))), at_sender = True)
        try:
            if six_num == 0 and five_num < 3:
                withdraw_message_manager.withdraw_message(
                    event,
                    msg_id,
                    (60, 1)
                )

        except:
            pass


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
            str_ = name + '_' + str(six_record) + ' '
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
    r = await AsyncHttpx.get(url)
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
            if i != '':
                list_select.append(i)
    if list_skin != 0:
        for i in list_skin:
            if i != '':
                list_select.append(i)
    return list_select        

#????????????

@set_helper.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    msg = args.extract_plain_text().strip()
    list_return = await get_all_have(group, uid)
    if list_return:         
        if msg in list_return:
            name = msg
            pic_url = await info_helper_basic.get_url(name)
            msg_tuple = (f'???????????????????????????{name}', image(pic_url))
            await helper_intact.draw(group, uid, name)    
            await set_helper.finish(Message(msg_tuple), at_sender=True)
        else:
            await set_helper.finish("????????????????????????,?????????????????????",at_sender = True)            
    else:
        await set_helper.finish("???????????????")

async def get_all_have(group, uid):
    list_return = await helper_collect.get_all_num(group, uid)
    list_char = []
    if list_return:         
        for i in list_return:
            list_char.append(i[0])
        return list_char
    else:
        return False

       
#????????????    

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
        await my_helper.finish("????????????????????????",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
        
    try:
        pic_url = list_select[list_my[1] - 1]
        if not await check_url(pic_url):
            pic_url = list_select[0]
    except:
        pic_url = list_select[0]
        
    
    msg_tuple = (f'?????????????????????{list_my[0]}', image(pic_url))
    await draw_char.finish(Message(msg_tuple), at_sender=True)                    

#????????????????????????
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
        await my_helper.finish("????????????????????????",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
    pic_num = len(list_select)  
    player = (await GroupInfoUser.get_member_info(uid, group)).user_name
       
    msg_list = [f"{player}??????????????????{list_my[0]}"]
    msg_list.append(f'?????????????????????') 
    for i in range(pic_num):
         msg_list.append(image(list_select[i]))
    await bot.send_group_forward_msg(
        group_id=event.group_id, messages=custom_forward_msg(msg_list, bot.self_id)
    ) 
    
      
    
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
        await my_helper.finish("????????????????????????",at_sender = True)
    else:
        list_select = await get_helper_all_pic(list_my[0])
    pic_num = len(list_select)  
    if is_number(msg):
        index = int(msg)
        if index >= 1 and index <= pic_num:
            await helper_intact.select(group, uid, index)
            await switch_paint.finish(f'???????????????????????????{index}?????????',at_sender = True)
        else:
            await switch_paint.finish('???????????????', at_sender = True)
    else:
        await switch_paint.finish('????????????', at_sender = True)

 
async def get_star(client, name:str, bot, event):
    url_pub = 'https://prts.wiki/index.php?title={}&action=edit' 
    url_only = url_pub.format(name)
    try:
        r = await client.get(url=url_only, headers={'User-Agent': ua})
        parse_html = etree.HTML(r.text)
        xpath_char='//textarea/text()'
        info_page=parse_html.xpath(xpath_char)
        info_str = re.search('?????????=(.*)',info_page[0])
        star = int(info_str.groups()[0]) + 1
        await helper_star.star_record(name, star)
        logger.info(f"{name}?????????{star},??????")
    except:
        logger.warning(f"{name}??????????????????,??????")
        await bot.send(event, f"{name}????????????????????????")

async def get_new_skin():
    url = 'https://prts.wiki/w/%E9%A6%96%E9%A1%B5' 

    try:
        r = AsyncHttpx.get(url=url)
        parse_html = etree.HTML(r.text)
        xpath_char = '(//div/i[@class="fa-tshirt fas"])[1]/../..//a/@title'
        list_return = parse_html.xpath(xpath_char)
        return list_return
    except:
        return False
    
async def get_new_role():
    url = 'https://prts.wiki/w/%E9%A6%96%E9%A1%B5' 

    try:
        r = AsyncHttpx.get(url=url)
        parse_html = etree.HTML(r.text)
        xpath_char = '(//div/i[@class="fa-user-plus fas"])[1]/../..//a/@title'
        list_return = parse_html.xpath(xpath_char)
        return list_return
    except:
        return False              
            
           

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
    msg_list.append(f'??????{player}???????????????')
    draw_count = await helper_collect.get_count(group, uid)
    msg_list.append(f'?????????{draw_count}???')
    for i in range(chaifen - 1, -1 , -1):
        list_ = []
        for j in range((i + 1) * 30 - 1, i * 30 - 1, -1):
            try:
                list_.append(list_return[j])
            except:
                continue
        a = await build_img_record(list_)
        b = pic2b64(a)
        msg_list.append(image(b64=b))
        
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
    msg_list.append(f'??????{player}???????????????')
    
    for i in range(chaifen - 1, -1, -1):
        list_ = []
        for j in range((i + 1) * 30 - 1, i * 30 - 1, -1):
            try:
                list_.append(list_return[j])
            except:
                continue
        a = await build_img_record(list_)
        b = pic2b64(a)
        msg_list.append(image(b64=b))
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
    await my_ticket.finish(f"?????????????????????{ticket}", at_sender = True)

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
            await ticket_convert.finish("???????????????????????????",at_sender = True)
        await helper_collect.ticket_convert(group, uid, 180)
        await helper_collect.role_record(group, uid, msg)
        await ticket_convert.finish(f"??????180??????????????????{msg}")
    if msg in list_five:
        if ticket_have < 45:
            await ticket_convert.finish("???????????????????????????",at_sender = True)
        await helper_collect.ticket_convert(group, uid, 45)
        await helper_collect.role_record(group, uid, msg)
        await ticket_convert.finish(f"??????45??????????????????{msg}")    
    await ticket_convert.finish("?????????????????????????????????", at_sender = True)    



            

async def buide_image(list_:list):
    img_back = Image.new("RGB",(720, 430),(255,255,255))
    fontStyle = ImageFont.truetype(yuanshen_ttf, 12, encoding="utf-8")
    draw = ImageDraw.Draw(img_back)
    draw.text((0, 10), "????????????", (0, 0, 0), font=fontStyle)
    draw.text((0, 30), "??????", (0, 0, 0), font=fontStyle)
    draw.text((0, 180), "????????????", (0, 0, 0), font=fontStyle)
    draw.text((0, 200), "????????????", (0, 0, 0),  font=fontStyle)
    draw.text((0, 220), "????????????", (0, 0, 0), font=fontStyle)
    draw.text((0, 240), "??????", (0, 0, 0), font=fontStyle)
    draw.text((0, 390), "????????????", (0, 0, 0), font=fontStyle)
    draw.text((0, 410), "????????????", (0, 0, 0), font=fontStyle)
    color_ = []
    color_.append((0, 170, 255))
    color_.append((170, 120, 255))
    color_.append((255, 180, 40))
    color_.append((255, 130, 0))
    tmp = 0
    column_ = 0
    
    for list_return in list_:
        tmp += 1
        if tmp > 5:
            column_ = 1
            tmp -= 5
        name = list_return[0]
        star = list_return[1]
        count_ = list_return[2] + 1
        ticket = list_return[3]
        star_ = star - 3
        draw.text((120 * tmp, 10 + column_ * 210), name, (0, 0, 0), font=fontStyle)
        draw.text((120 * tmp, 30 + column_ * 210), str(star), color_[star_], font=fontStyle)
        draw.text((120 * tmp, 180 + column_ * 210), str(count_), (0, 0, 0), font=fontStyle)
        draw.text((120 * tmp, 200 + column_ * 210), str(ticket), (0, 0, 0), font=fontStyle)
        pinyin = pypinyin.pinyin(name, style=pypinyin.NORMAL)
        pinyin_ = ''
        for i in pinyin:
            pinyin_ += i[0]
        pic = pinyin_ + '.png'
        avatar = avatar_path
        avatar_ = str(avatar.absolute()) + '/' + pic
        try:
            img = Image.open(avatar_)
            img_back.paste(img, (tmp * 120, 50 + column_ * 210))
        except:
            try:
                pil = await get_pic_pil(get_avatar(name, 0))
                img = revise_size_h(pil, 120)
                img_back.paste(img, (tmp * 120, 50 + column_ * 210))
            except:
                pass     
    return img_back

def pic2b64(pic: Image) -> str:
    """
    ??????:
        PIL?????????base64
    ??????:
        :param pic: ??????PIL?????????????????????
    """
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return "base64://" + base64_str

async def get_record_text(name, title):
    url_jp = 'https://static.prts.wiki/voice/{}/{}?filename={}.wav'
    url_cn = 'https://static.prts.wiki/voice_cn/{}/{}?filename={}.wav'
    url_text = 'https://prts.wiki/index.php?title={}/????????????&action=edit'
    count = 0
    issucceed = 0
    while count < 3 and issucceed == 0:
        try:
            r = await AsyncHttpx.get(url=url_text.format(name))
            parse_html = etree.HTML(r.text)
            xpath_voice = '//textarea/text()'
            char_voice=parse_html.xpath(xpath_voice)
            issucceed = 1
        except:
            logger.warning("??????????????????,2s?????????")
            count += 1
            await asyncio.sleep(2)
    texts = char_voice[0].split('\n\n')    
    key_text = texts[0]
    key = re.search('key=(.*)', key_text)
    key = key.groups()[0]    
    list_voice = []
    for i in texts:
        list_tmp = []
        results = re.search('=(.*)\n.*\|??????\|(.*)}}{{VoiceData/word\|??????\|',i)
        index = re.search('\|??????.*=(.*)',i)
        try:
            list_tmp.append(results.groups()[0])
            list_tmp.append(results.groups()[1])
            list_tmp.append(index.groups()[0])
            list_voice.append(list_tmp)

        except:
            pass
    voice_sel = random.choice(list_voice)       
    for i in list_voice:
        if i[0] == title:
            voice_sel = i
            break  
    list_return = []    
    voice_title = voice_sel[0]
    voice_text = voice_sel[1]
    voice_index = voice_sel[2]
    url_voice_jp = url_jp.format(key, voice_index, voice_title)
    url_voice_cn = url_cn.format(key, voice_index, voice_title)  
    list_return.append(url_voice_cn)
    list_return.append(url_voice_jp)
    list_return.append(voice_text)
    return list_return



async def build_img_record(list_ : list):
    color_ = []
    color_.append((0, 170, 255))
    color_.append((170, 120, 255))
    color_.append((255, 180, 40))
    color_.append((255, 130, 0))
    lens = len(list_)

    img_back = Image.new("RGB",(400, 42 + (lens * 2 - 1) * 12),(255,255,255))
    fontStyle = ImageFont.truetype(yuanshen_ttf, 12, encoding="utf-8")
    draw = ImageDraw.Draw(img_back)
    for i in range(lens):
        name = list_[i][0]
        count = int(list_[i][1]) + 1
        star = await helper_star.get_star(name)
        star_ = star - 3
        draw.text((0, 21 + i * 2 * 12), name, color_[star_], font=fontStyle)
        draw.text((400 - 12 * 4, 21 + i * 2 * 12), str(count), (0, 0, 0), font=fontStyle)
    return img_back

async def get_pic_pil(url):
    async with httpx.AsyncClient(headers={'User-Agent': ua},timeout=5) as client:
        resp = await client.get(url=url)
    resp.raise_for_status()
    pic = resp.content
    pil_return = Image.open(BytesIO(pic))
    return pil_return

async def build_sign_card(group:int, uid:int):
    list_my = await helper_intact.my(group, uid)
    if list_my == 0:
        name = 'none'
        url = 'none'
    else:
        name = list_my[0]
        list_select = await get_helper_all_pic(name)
        index_ = list_my[1] - 1
        try:
            url = list_select[index_]
        except:
            url = list_select[0]
    try:
        url += "?image_process=format,webp/quality,Q_10"
        back = await get_pic_pil(url)
    except:
        back = Image.new('RGBA', (800, 800), (255, 255, 255, 300))
    if '_1' in url:
        box = (back.size[0] / 4, 0, back.size[0] / 4 * 3, back.size[1] / 4) #????????????
        back = back.filter(ImageFilter.GaussianBlur(radius=18)) #????????????
        back = back.crop(box) #??????
    else:
        box = (back.size[0] / 4, back.size[0] / 4, back.size[0] / 4 * 3, back.size[1] / 4 * 2)
        back = back.filter(ImageFilter.GaussianBlur(radius=18)) #????????????
        back = back.crop(box) #??????
    nickname = (await GroupInfoUser.get_member_info(uid, group)).user_name
    qq_avatar_url = f"http://q1.qlogo.cn/g?b=qq&nk={uid}&s=640"
    try:
        qq_avatar = await get_pic_pil(qq_avatar_url)
    except:
        qq_avatar = Image.new('RGBA', (640, 640), (255, 255, 255, 300))
    
    pinyin = pypinyin.pinyin(name, style=pypinyin.NORMAL)
    pinyin_ = ''
    skin_index = 0
    for i in range(1, skin_top):
        if f"skin{i}" in url:
            skin_index = i
            break
    try:
        pil = await get_pic_pil(get_avatar(name, skin_index))
        avatar_helper = revise_size_h(pil, 120)
    except:
        avatar_helper =  Image.new('RGBA', (120, 120), (255, 255, 255, 300))
    try:
        text_helper = (await get_record_text(name, "??????"))[2]
    except:
        text_helper = '??????????????????'
    ticket_num = await helper_collect.get_ticket(group, uid)   
    rest_day = await moon_card_prts.get_rest_day(group, uid)
    card = pic_make_(back, avatar_helper, qq_avatar, nickname, rest_day, ticket_num, text_helper)
    return card
    
use = require("use")
@driver.on_startup
async def my_shop_mooncard_prts():
    @shop_register(
        name="????????????",
        price=30,
        des="???????????????????????????????????????50?????????30????????????????????????????????????",
        load_status=True,
        daily_limit=1,
        is_passive=False,
        icon=None,
        ** {"multi":50},
    )
    async def sign_gift(user_id: int, group_id: int, multi: int):
        price = await draw_price.get_price(group_id)
        gold_have = await BagUser.get_gold(user_id, group_id)
        if gold_have >= price * multi:   
            await BagUser.spend_gold(user_id, group_id, price * multi)
            await moon_card_prts.buy(group_id, user_id)
        
@check_in.handle()
async def _(bot: Bot,
            event: GroupMessageEvent,
            state: T_State,
            args: Message = CommandArg(),
            ):
    uid = event.user_id
    group = event.group_id
    a = datetime.now().date()
    b = str(a)
    if await moon_card_prts.get_rest_day(group, uid) > 0:
        if b != await moon_card_prts.get_time(group, uid):
            await helper_collect.add_ticket(group, uid, 6)
            await moon_card_prts.check_in(group, uid, b)
            try:
                sign_card = await build_sign_card(group, uid)
            except:
                await check_in.finish("?????????,???????????????",at_sender=True)
            await check_in.send(image(b64 = pic2b64(sign_card)), at_sender = True)

   
@scheduler.scheduled_job(
    "cron",
    hour=23,
    minute=50,
    
)
async def _():
    try:
        global guess_voice
        guess_voice = {}
        query = await moon_card_prts.get_all_user()
        for i in query:
            if i.rest_day > 0:
                if i.time_last != str(datetime.now().date()):
                    await moon_card_prts.check_in(i.group_id, i.uid, str(datetime.now().date()))
    except:
        logger.info("????????????????????????")
                
    
    
    
