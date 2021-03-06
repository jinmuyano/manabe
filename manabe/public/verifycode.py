from django.http import HttpResponse


# 验证码字符存入session，图像返回给用户显示
def verify_code(request):
    from PIL import Image,ImageDraw,ImageFont
    import random
    # 定义变量，用户画面的颜色，宽，高
    bgcolor= (random.randrange(40,200),random.randrange(40,200),255)
    width=200
    height=40

    # 创建画布对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'

    # 随机选取4个值作为验证码
    rand_str=''
    for i in range(0,4):
        rand_str+=str1[random.randrange(0,len(str1))]

    # 构造字体对象
    import os
    path=os.path.join(os.path.dirname(__file__),'fonts','arial.ttf')
    font = ImageFont.truetype(path,23)

    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字体
    draw.text((20, 10), rand_str[0], font=font, fill=fontcolor)
    draw.text((70, 10), rand_str[1], font=font, fill=fontcolor)
    draw.text((120, 10), rand_str[2], font=font, fill=fontcolor)
    draw.text((170, 10), rand_str[3], font=font, fill=fontcolor)

    #释放画笔
    del draw

    #存入session，在用户提交他写的验证码时做对比
    request.session['verify_code']=rand_str

    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')