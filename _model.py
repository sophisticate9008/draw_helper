from tortoise import fields
from hashlib import md5
from services.db_context import Model

from datetime import datetime, timedelta
     
class helper_star(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    name = fields.CharField(255, null=True)
    star = fields.IntField()
    class Meta:
        table = 'helper_star'
        table_description = "干员星级名字"
    @classmethod
    async def star_record(cls, name, star):
        await cls.create(
            name=name,
            star=star
        )
    @classmethod
    async def get_star_list(cls, star):
        try:
            query = await cls.filter(star=star).all()       
            return query
        except:
            return False
    @classmethod
    async def is_exist(cls, name):
        if me := await cls.get_or_none(name=name):
            return True
        else:
            return False
    @classmethod
    async def get_star(cls, name: str):
        if me := await cls.get_or_none(name=name):
            return me.star
        else:
            return False 
    @classmethod
    async def get_all_url(cls, name):
        list_ = []
        list_.extend(get_basic(name))
        list_.extend(get_skin(name))
        return list_
    @classmethod
    async def get_all_name(cls):
        return cls.all()
        
    
                
class helper_collect(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    group_id = fields.BigIntField()
    uid = fields.BigIntField()
    name = fields.CharField(20000, null=True)
    ticket = fields.IntField()
    draw_count = fields.IntField()
    six_record = fields.IntField()#记录保底
    draw_record = fields.CharField(20000, null=True)#记录六星抽卡记录
    index_ = fields.IntField(unique=True)
    price = fields.IntField(unique=True)
    helper = fields.CharField(255, null=True, unique=True)
    class Meta:
        table = "helper_collect"
        table_description = "群员抽干员的数据表"
        unique_together = ("uid", "group_id")      
        
        
    @classmethod
    async def get_price(cls, group_id, uid):
        if me := await cls.get_or_none(group_id=group_id, uid=uid):
            return me.price
        else:
            return 10
    @classmethod
    async def set_price(cls, group_id, price):
        query = await cls.filter(group_id=group_id).all()
        for x in query:
            x.price = price
            await x.save()     
    @classmethod
    async def my(cls, group_id, uid):
        if me := await cls.get_or_none(group_id=group_id, uid=uid):
            list_info = []
            list_info.append(me.helper)
            list_info.append(me.index_)
            return list_info
        else:
            return 0

    @classmethod
    async def select(cls, group_id, uid, index_):
        if me := await cls.get_or_none(group_id=group_id, uid=uid):
            me.index_ = index_
            await me.save()
    @classmethod
    async def set_helper(cls, group_id, uid, helper):
        if me := await cls.get_or_none(group_id=group_id, uid=uid):  
            me.helper = helper
            await me.save()     

    @classmethod
    async def role_record(cls, group, uid, name):
        name_create = name + '_' + '0' + ' '
        if me := await cls.get_or_none(group_id=group,uid=uid):
            info_str = me.name
            name_list = info_str.split()
            for i in name_list:
                list_ = i.split('_')
                if list_[0] == name:
                    name_old = name + '_' + list_[1]
                    num_new = int(list_[1]) + 1
                    num_ = str(num_new)
                    name_new = name + '_' + num_
                   
                    info_str = info_str.replace(name_old, name_new)
                    me.name = info_str
                    me.draw_count = me.draw_count + 1
                    me.six_record = me.six_record + 1
                    await me.save()
                    return True
            info_str_ = info_str + name_create
            me.name = info_str_
            me.draw_count = me.draw_count + 1      
            me.six_record = me.six_record + 1
        else:
            await cls.create(group_id=group, uid=uid, name=name_create, ticket=0, draw_count=1, six_record=1, draw_record='', index_=1, price=10, helper='')
    @classmethod
    async def get_num(cls, group, uid, name):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            name_all = me.name
            name_list = name_all.split()                  
            for i in name_list:
                list_ = i.split('_')
                if name == list_[0]:
                    return int(list_[1])
            return 0
        else:
            return 0
    @classmethod
    async def get_all_num(cls, group, uid):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            name_all = me.name
            name_list = name_all.split()
            list_return = []            
            for i in name_list:                       
                list_ = i.split('_')
                list_return.append(list_)
            return list_return
        else:
            return False
    @classmethod
    async def get_ticket(cls, group, uid):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            return me.ticket
        else:
            return False
    @classmethod
    async def get_count(cls, group, uid):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            return me.draw_count   
        else:
            return False            
    @classmethod
    async def record_clear(cls, group, uid):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            me.six_record = 0
            await me.save()
        else:
            return False                            
    @classmethod
    async def get_six_record(cls, group, uid):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            return me.six_record
        else:
            return False
    @classmethod
    async def add_ticket(cls, group, uid, num):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            me.ticket += 1
            await me.save()
        else:
            return False
    @classmethod 
    async def ticket_convert(cls, group, uid, num):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            me.ticket -= num
            await me.save()
        else:
            return False
    @classmethod
    async def draw_record_(cls, group, uid, str_):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            me.draw_record += str_
            await me.save()
        else:
            return False
    @classmethod
    async def get_record(cls, group, uid):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            record = me.draw_record
            list_return = []
            record_ = record.split()
            for i in record_:
                list_return.append(i.split("_"))
            
            return list_return
        else:
            return False   
    @classmethod
    async def _run_script(cls):
        try:
            await cls.raw("ALTER TABLE helper_collect ADD index_ INT DEFAULT 1;")   
            await cls.raw("ALTER TABLE helper_collect ADD price INT DEFAULT 10;")
            await cls.raw("ALTER TABLE helper_collect ADD helper varchar(255) DEFAULT '';")
            print("添加字段 index_ price helper")
        except:
            pass

class moon_card_prts(Model):   

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    group_id = fields.BigIntField(null=True)
    uid = fields.BigIntField()
    rest_day = fields.IntField()
    time_last = fields.CharField(255)
    
    class Meta:
        table = "moon_card_prts"
        table_description = "群员月卡信息"
        unique_together = ("group_id", "uid")        
    @classmethod
    async def get_buy_list(cls, group):
        try:
            query = await cls.filter(group_id = group).all()          
            return query
        except:
            return False
    @classmethod
    async def buy(cls, group, uid):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            me.rest_day += 30
            await me.save()
        else:
            await cls.create(group_id = group, uid = uid, rest_day = 30, time_last = 0)
    @classmethod    
    async def get_rest_day(cls, group, uid):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            return me.rest_day
        else:
            return 0
    @classmethod
    async def check_in(cls, group, uid, time_last):

        if me := await cls.get_or_none(group_id=group, uid=uid):
            me.time_last = time_last
            me.rest_day -= 1 
            await me.save()
        else:
            return False
    @classmethod
    async def get_all_user(cls):
        query = await cls.all()
        return query
    
    @classmethod
    async def get_time(cls, group, uid):
        if me := await cls.get_or_none(group_id=group, uid=uid):
            return me.time_last
        else:
            return str(datetime.now().date())       


pub_link = 'https://prts.wiki/images/{}/{}{}/'
skin_top = 7
three_star = ['正义骑士号', "THRM-EX", '斑点', '泡普卡', '月见夜', '空爆', '梓兰', '史都华德', '安赛尔', '芙蓉', '炎熔', '安德切尔', '克洛丝', '米格鲁', '卡缇', 
                '玫兰莎', '翎羽', '香草', '芬', '12F', '杜林', '巡林者', '黑角', '夜刀', 'Castle-3', 'Lancet-2']

def get_basic(name: str):
    list_ = []
    for i in range(1, 3):
        if i == 2 and name in three_star:
            break
        path_ = get_path(f"立绘_{name}_{i}.png")
        list_.append(path_)
    return list_
       
def get_skin(name:str):
    list_ = []
    for i in range(1, skin_top):
        path_ = get_path(f"立绘_{name}_skin{i}.png")
        list_.append(path_)
    return list_

def get_avatar(name:str, index__:int):
    path_ = get_path(f"头像_{name}_skin{index__}.png")
    if index__ == 0:
        path_ = get_path(f"头像_{name}.png")
    return path_

def get_path(path:str):
    h1 = md5()
    h1.update(path.encode("utf-8"))
    md5_ = str(h1.hexdigest())
    return pub_link.format(md5_[0], md5_[0], md5_[1]) + path
