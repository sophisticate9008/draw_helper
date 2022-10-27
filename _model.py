from services.db_context import db
from datetime import datetime, timedelta
class info_helper_basic(db.Model):
    __tablename__ = "info_helper_basic"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), nullable=False)
    painting1 = db.Column(db.Unicode(),nullable=False)
    painting2 = db.Column(db.Unicode(),nullable=False)

    @classmethod
    async def store(cls, name, link:str, index:int):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            if index == 1:
                await me.update(painting1 = link).apply()
            if index == 2:
                await me.update(painting2 = link).apply()
        else:
            await cls.create(name = name,painting1 = link, painting2 = '')
            
    @classmethod
    async def get_all_name(cls):
        try:
            query = await cls.query.gino.all()
            return query
        except:
            return 0
        
    @classmethod
    async def get_url(cls, name):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = me = await query.gino.first()
        if me:
            return me.painting1
        else:
            return 0
    @classmethod
    async def get_all_url(cls, name):
        
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        painting_list = []
        if me:
            painting_list.append(me.painting1)
            painting_list.append(me.painting2)
            return painting_list
        else:
            return 0
    @classmethod
    async def is_exist(cls, name):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            return 1
        else:
            return 0                        
    @classmethod
    async def clear(cls, name):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()  
        if me:
            await me.update(painting1 = '').apply()
            await me.update(painting2 = '').apply()
        else:
            return False
        
        
                
class info_helper_skin(db.Model):
    __tablename__ = "info_helper_skin"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), nullable=False)
    skin1 = db.Column(db.Unicode(),nullable=False)
    skin2 = db.Column(db.Unicode(),nullable=False)
    skin3 = db.Column(db.Unicode(),nullable=False)
    skin4 = db.Column(db.Unicode(),nullable=False)
    skin5 = db.Column(db.Unicode(),nullable=False)
    skin6 = db.Column(db.Unicode(),nullable=False)
    @classmethod
    async def store(cls, name, link:str, index:int):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            if index == 1:
                await me.update(skin1 = link).apply()
            if index == 2:
                await me.update(skin2 = link).apply()
            if index == 3:
                await me.update(skin3 = link).apply()
            if index == 4:
                await me.update(skin4 = link).apply()
            if index == 5:
                await me.update(skin5 = link).apply()
            if index == 6:
                await me.update(skin6 = link).apply()            
        else:
            await cls.create(name = name, skin1 = link, skin2 = '', skin3 = '', skin4 = '', skin5 = '', skin6 = '')
    @classmethod
    async def get_all_url(cls, name):
        
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        painting_list = []
        if me:
            painting_list.append(me.skin1)
            painting_list.append(me.skin2)
            painting_list.append(me.skin3)
            painting_list.append(me.skin4)
            painting_list.append(me.skin5)
            painting_list.append(me.skin6)
            return painting_list
        else:
            return 0      
    @classmethod      
    async def is_exist(cls, name):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            return 1
        else:
            return 0   
    @classmethod
    async def record_none(cls, name, link):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(skin6 = link).apply()
        else:
            await cls.create(name = name, skin1 = '', skin2 = '', skin3 = '', skin4 = '', skin5 = '', skin6 = link)
    @classmethod
    async def get_new_index(cls, name):
        
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()  
        if me:
            
            list_ = [me.skin1, me.skin2, me.skin3, me.skin4, me.skin5, me.skin6]
            for i in range(6):
                            
                if list_[i] != '' and list_[i + 1] == '':
                    return i + 2
            return 1
        else:
            return 1
            

                
        
        
class helper_intact(db.Model):
    __tablename__ = "helper_intact"
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=True)
    my_qq = db.Column(db.BigInteger(), nullable=True)
    name = db.Column(db.Unicode(), nullable=True)   
    index = db.Column(db.Integer(), nullable=False)
    draw_count = db.Column(db.Integer(), nullable=False)
    @classmethod
    async def draw(cls, group_id:int, my_qq:int, name):
        query = cls.query.where((cls.group_id == group_id) & (cls.my_qq == my_qq))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(name = name).apply()
            await me.update(draw_count = me.draw_count + 1).apply()
        else:
            await cls.create(group_id = group_id, my_qq = my_qq, name = name, index = 1, draw_count = 1)
    @classmethod
    async def my(cls, group_id:int, my_qq:int):
        query = cls.query.where((cls.group_id == group_id) & (cls.my_qq == my_qq))
        query = query.with_for_update()     
        me = await query.gino.first()
        list_info = []
        if me:
            list_info.append(me.name)
            list_info.append(me.index)
            return list_info
        else:
            return 0        
        
    @classmethod
    async def select(cls, group_id:int, my_qq:int, index:int):
        query = cls.query.where((cls.group_id == group_id) & (cls.my_qq == my_qq))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(index = index).apply()
        else:
            return 0
        
    @classmethod
    async def get_all_users(cls, group_id:int):
        if not group_id:
            query = await cls.query.gino.all()
        else:
            query = await cls.query.where((cls.group_id == group_id)).gino.all()
        return query                            

class helper_star(db.Model):
    __tablename__ = "helper_star"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), nullable=True)
    star = db.Column(db.Integer(), nullable=False)
    @classmethod
    async def star_record(cls, name, star):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            pass
        else:
            await cls.create(name = name, star = star)            
    @classmethod
    async def get_star_list(cls, star):
        try:
            query = await cls.query.where(cls.star == star).gino.all()          
            return query
        except:
            return False
    @classmethod
    async def is_exist(cls, name):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            return True
        else:
            return False
    @classmethod
    async def get_star(cls, name: str):
        query = cls.query.where(cls.name == name)
        query = query.with_for_update()
        me = await query.gino.first()    
        if me:
            return me.star
        else:
            return False    
        
class draw_price(db.Model):
    __tablename__ = "draw_price"
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=True)
    price = db.Column(db.Integer(), nullable=False)
    @classmethod
    async def set_price(cls, group, price):
        query = cls.query.where(cls.group_id == group)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(price = price).apply()  
        else:
            await cls.create(group_id = group, price = price)          
    @classmethod
    async def get_price(cls, group):
        query = cls.query.where(cls.group_id == group)
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            return me.price
        else:
            return 10
                
class helper_collect(db.Model):
    __tablename__ = "helper_collect"
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=True)
    uid = db.Column(db.BigInteger(), nullable=True)
    name = db.Column(db.Unicode(), nullable=True)
    ticket = db.Column(db.Integer(), nullable=False)
    draw_count = db.Column(db.Integer(), nullable=False)
    six_record = db.Column(db.Integer(), nullable=False)#记录保底
    draw_record = db.Column(db.Unicode(), nullable=True)#记录六星抽卡记录
    @classmethod
    async def role_record(cls, group, uid, name):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        name_create = name + '_' + '0' + ' '
        if me:
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
                    await me.update(name = info_str).apply()
                    await me.update(draw_count = me.draw_count + 1).apply()
                    await me.update(six_record = me.six_record + 1).apply()
                    return True
            info_str_ = info_str + name_create
            await me.update(name = info_str_).apply()
            await me.update(draw_count = me.draw_count + 1).apply()       
            await me.update(six_record = me.six_record + 1).apply()     
        else:
            await cls.create(group_id = group, uid = uid, name = name_create, ticket = 0, draw_count = 1, six_record = 1, draw_record = '')
    @classmethod
    async def get_num(cls, group, uid, name):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:      
            name_all = me.name
            name_list = name_all.split()                  
            for i in name_list:
                list_ = i.split('_')
                if name == list_[0]:
                    return int(list_[1])
        else:
            return False
    @classmethod
    async def get_all_num(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
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
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            return me.ticket
        else:
            return False
    @classmethod
    async def get_count(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first() 
        if me:
            return me.draw_count   
        else:
            return False            
    @classmethod
    async def record_clear(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first() 
        if me:
            await me.update(six_record = 0).apply()
        else:
            return False                            
    @classmethod
    async def get_six_record(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first() 
        if me:
            return me.six_record
        else:
            return False
    @classmethod
    async def add_ticket(cls, group, uid, num):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(ticket = me.ticket + num).apply() 
        else:
            return False
    @classmethod 
    async def ticket_convert(cls, group, uid, num):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(ticket = me.ticket - num).apply()
        else:
            return False
    @classmethod
    async def draw_record_(cls, group, uid, str_):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            await me.update(draw_record = me.draw_record + str_).apply()
        else:
            return False
    @classmethod
    async def get_record(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update()
        me = await query.gino.first()
        if me:
            record = me.draw_record
            list_return = []
            record_ = record.split()
            for i in record_:
                list_return.append(i.split("_"))
            
            return list_return
        else:
            return False      

class moon_card_prts(db.Model):   
    __tablename__ = "moon_card_prts"
    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=False)
    uid = db.Column(db.BigInteger(), nullable=False)
    rest_day = db.Column(db.Integer(), nullable=False)
    time_last = db.Column(db.Unicode(), nullable=False)
    
    @classmethod
    async def get_buy_list(cls, group):
        try:
            query = await cls.query.where(cls.group_id == group).gino.all()          
            return query
        except:
            return False
    @classmethod
    async def buy(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update() 
        me = await query.gino.first()
        if me:
            await me.update(rest_day = me.rest_day + 30).apply()
        else:
            await cls.create(group_id = group, uid = uid, rest_day = 30, time_last = '0')
    @classmethod    
    async def get_rest_day(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update() 
        me = await query.gino.first()
        if me:
            return me.rest_day
        else:
            return 0
    @classmethod
    async def check_in(cls, group, uid, time_last):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update() 
        me = await query.gino.first()
        if me:
            await me.update(time_last = time_last).apply()
            await me.update(rest_day = me.rest_day - 1).apply()
        else:
            return False
    @classmethod
    async def get_all_user(cls):
        query = await cls.query.gino.all()
        return query
    
    @classmethod
    async def get_time(cls, group, uid):
        query = cls.query.where((cls.group_id == group) & (cls.uid == uid))
        query = query.with_for_update() 
        me = await query.gino.first()
        if me:
            return me.time_last
        else:
            return str(datetime.now().date())       
