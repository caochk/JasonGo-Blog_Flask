from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random, string

# ================生成图片验证码================
class ImageCode:
    # 生成用于绘制字符串的随机颜色
    def rand_color(self):
        red = random.randint(32, 127)
        green = random.randint(25, 188)
        blue = random.randint(32, 127)
        return red, green, blue

    # 生成四位随机字符串
    def gen_text(self):
        str = random.sample(string.ascii_letters + string.digits, 4)
        return ''.join(str)

    # 绘制一些干扰线(draw为PIL库中的ImageDraw对象)
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50  # 验证码图片宽度、高度（可以自行设定）
        # 下面创建图片对象（设定背景色为白色）
        img = Image.new('RGB', (width, height), 'white')
        # 选择使用的字体及大小
        font = ImageFont.truetype(font='arial.ttf', size=40)
        # 新建ImageDraw对象
        draw = ImageDraw.Draw(img)
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 2, width, height)
        return img, code

    # 生成图片验证码并返回给控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        # 图片以二进制形式写入内存而非硬盘
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()  # 获取图片文件的字节码
        return code, bstring  # 返回验证码的字符串与字节码内容


# =============发送QQ邮箱验证码（参数为收件箱的地址、随机生成的验证码）=============
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
def send_email(receiver, ecode):
    # 自定义邮件内容（可在Python内混合编写HTML、CSS代码）
    content = f"<br/>欢迎注册Jason's博客系统账号，您的邮箱验证码为：" \
        f"<span style='color: red; font-size: 20px;'>{ecode}</span>，" \
        f"请复制到注册窗口中完成注册。<br>" \
              f"<span style='color: dodgerblue; font-size: 18px;'>使用Jason的博客系统，分享热爱的事物</span><br/>"

    # 发件人信息
    sender = "JasonBlog <774530647@qq.com>"  # 邮箱地址必须写对，不然发不出去

    # 实例化邮件对象，并指定邮件的一些关键信息
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('Jason的博客注册验证码', 'utf-8')  # 指定邮件的标题（UTF-8编码）
    message['From'] = sender  # 指定发件人
    message['To'] = receiver  # 指定收件人

    # 建立与QQ邮件服务器的连接
    smtpObj = SMTP_SSL('smtp.qq.com')
    # 通过发件人邮箱账号与授权码登录QQ邮箱
    smtpObj.login(user='774530647@qq.com', password='wiftpddlwozdbdib')
    # 发送邮件
    smtpObj.sendmail(sender, receiver, str(message))
    # 发送完成后断开与服务器的连接
    smtpObj.quit()

# 生成6位随机字符串作为邮箱验证码
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)