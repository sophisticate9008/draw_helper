


from services.db_context import db

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
                
