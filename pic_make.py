from PIL import Image, ImageFilter, ImageDraw, ImageFont
import cmath
import os
path_ = os.path.dirname(__file__)
path_ = path_.replace('\\', '/')
res = str(path_) + "/resources/"
def addTransparency(img: Image, factor):
    """
    图片透明度函数
    """
    img = img.convert('RGBA')
    img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
    img = Image.blend(img, img_blender, factor)
    img_temp = img
    return img_temp

def revise_size_width(back: Image, basewidth):
    """
    根据宽度调大小
    """
    wpercent = basewidth / float(back.size[0])
    hsize = int (float(back.size[1]) * float(wpercent))
    back = back.resize((basewidth, hsize), Image.ANTIALIAS) 
    return back   

def revise_size_h(back: Image, baseh):
    """
    根据高度调大小
    """
    wpercent = baseh / float(back.size[1])
    width = int (float(back.size[0]) * float(wpercent))
    back = back.resize((width, baseh), Image.ANTIALIAS) 
    return back

def crop_square(back:Image):
    w = back.size[0]
    h = back.size[1]
    if w < h:
        box = (0, 0, w, w)
    else:
        box = (0, 0, h, h)
    back = back.crop(box)
    return back
    

def crop_round(back: Image):
    """
    圆形裁剪
    """
    back = crop_square(back)
    back = back.convert('RGBA')
    size = back.size[0]
    r = size / 2
    back_ = back.load() #背景像素加载   
    opaque = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    opaque_ = opaque.load()
    for i in range(size):
        for j in range(size):
            lx = abs(i - r)
            ly = abs(j - r)
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5
            if l > r:
                back_[i, j] = opaque_[i, j]
    return back
                
def round_corner(back: Image, r:int):
    """
    圆角边框
    """
    back_ = back.load()
    opaque = Image.new('RGBA', (back.size[0], back.size[1]), (0, 0, 0, 0))
    opaque_ = opaque.load()
    for i in range(0, r):
        for j in range(0, r):
            lx = abs(i - r)
            ly = abs(j - r)
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5
            if l > r:
                back_[i, j] = opaque_[i, j]  
                
    for i in range(back.size[0] - r, back.size[0]):
        for j in range(0, r):
            lx = abs(i - (back.size[0] - r))
            ly = abs(j - r)
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5
            if l > r:
                back_[i, j] = opaque_[i, j]    
                          
    for i in range(0, r):
        for j in range(back.size[1] - r, back.size[1]):
            lx = abs(i - r)
            ly = abs(j - (back.size[1] - r))
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5
            if l > r:
                back_[i, j] = opaque_[i, j]         
             
    for i in range(back.size[0] - r, back.size[0]):
        for j in range(back.size[1] - r, back.size[1]):
            lx = abs(i - (back.size[0] - r))
            ly = abs(j - (back.size[1] - r))
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5
            if l > r:
                back_[i, j] = opaque_[i, j]                
    return back

def pic_make_(back, avatar_helper, avatar_qq, nickname, day_rest, ticket_num, text_helper):
    
    back = revise_size_width(back, 800)

    logo_ = Image.open(res + '明日方舟.png')
    logo_ = revise_size_width(logo_, 135)

    gold_box = Image.open(res + '金色边框.png')
    gold_box = revise_size_width(gold_box, 200)

    black = Image.new('RGBA', (gold_box.size[0] - 4 , gold_box.size[1] - 1), (0, 0, 0, 225))#黑色遮块
    black1 = Image.new('RGBA', (180 , 8), (0, 0, 0, 175))
    black2 = Image.new('RGBA', (7 , 38), (0, 0, 0, 175))

    black3 = Image.new('RGBA', (180, 35), (0, 0, 0, 125))
    black3 = round_corner(black3, 10)



    keluxier = Image.open(res + '可露希尔.png')
    keluxier = revise_size_h(keluxier, 400)

    avatar = avatar_helper
    avatar = revise_size_h(avatar, 70)
    avatar = crop_round(avatar)

    black_box = Image.open(res + '黑色圆框.png')
    black_box = revise_size_h(black_box, 72)

    qq_avatar = avatar_qq
    qq_avatar = revise_size_h(qq_avatar, 80)

    qq_box = Image.open(res + 'qq头像框.png')
    qq_box = revise_size_h(qq_box, 82)

    text_helper = text_helper
    text_len = int(len(text_helper) * 2.0 * 12)
    talk_box = Image.new('RGBA', (text_len, 40), (0, 0, 0, 200))
    talk_box = round_corner(talk_box, 6)
    yuanshen_ttf = res + 'yuanshen.ttf'
    fontStyle = ImageFont.truetype(yuanshen_ttf, 12 , encoding="utf-8")


    if day_rest < 3:
        text_keluxier = f'温馨提示,博士的月卡将在{day_rest}后到期'
        text_keluxier1 = '不续费真的挺可惜的'
    else:
        text_keluxier = f'博士的月卡还剩余{day_rest}天到期'
        
    text_indiv = '签到成功，黄票加6'
    text_indiv1 = f'当前黄票为{ticket_num}'
    nick_name = "Dr." + nickname

    back.paste(logo_, (400 - int(logo_.size[0] / 2), 0), mask=logo_)
    back.paste(keluxier, (800 - keluxier.size[0], 0), mask=keluxier)
    back.paste(black, (595 + 2, 240 + 1), mask=black)
    back.paste(black1, (595 + 30, 240 + 63), mask=black1)
    back.paste(black2, (595 + 200, 240 + 25), mask=black2)
    back.paste(gold_box, (595, 240), mask=gold_box)
    back.paste(talk_box, (12 + 35, 400 - 12 - 35 - 20), mask=talk_box)
    back.paste(avatar, (12, 400 - 12 - 70), mask=avatar)
    back.paste(black_box, (11, 400 - 11 - 72), mask=black_box)
    back.paste(qq_avatar, (48, 48))
    back.paste(qq_box, (47, 47), mask=qq_box)
    back.paste(black3, (47 + 90, 47 + 40), mask = black3)
    draw = ImageDraw.Draw(back)
    draw.text((12 + 72, 400 - 12 - 35 - 6), text_helper, (255, 255, 255), font=fontStyle)
    draw.text((605, 250), text_keluxier, (255, 255, 0), font=fontStyle)

    if day_rest < 3:
        draw.text((605, 275), text_keluxier1, (255, 255, 0), font=fontStyle)
        
    fontStyle = ImageFont.truetype(yuanshen_ttf, 10 , encoding="utf-8")
    draw.text((47 + 90 + 3, 47 + 40 + 3), text_indiv, (255, 255, 160), font=fontStyle)
    draw.text((47 + 90 + 3, 47 + 40 + 3 + 15), text_indiv1, (255, 255, 160), font=fontStyle)
    fontStyle = ImageFont.truetype(yuanshen_ttf, 14 , encoding="utf-8")
    draw.text((47 + 90, 47 + 13), nick_name, (0, 0, 0), font=fontStyle)
    return back
