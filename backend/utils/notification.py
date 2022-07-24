# -*-coding:utf-8-*-
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email(object):
    """
    发送邮件模块
    """

    def __init__(self, mail_from, mail_to, mail_key):
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.password = mail_key
        self.smtp_server = "smtp.126.com"

    def _attach_image(self, id):
        # 图片的路径, 默认是和脚本相同的路径下的文件，可以绝对路径指定某个图片。
        fp = open("{0}.jpg".format(id), "rb")
        images = MIMEImage(fp.read())
        fp.close()
        images.add_header("Content-ID", "<image{0}>".format(id))
        return images

    def _message(self, subject, content):
        msg = MIMEMultipart()
        email_body = MIMEText(content, _subtype="html", _charset="utf-8")
        msg["From"] = self.mail_from
        msg["To"] = ", ".join(self.mail_to)
        msg["Subject"] = subject
        msg.attach(email_body)
        # msg.attach(self._attach_image('1'))
        # 如果需要插入多张图片, 按照下面的方式多次调用, 并在 html 中增加对应的 <img>标签
        # msg.attach(self._attach_image('2'))
        # msg.attach(self._attach_image('3'))
        # msg.attach(self._attach_image('4'))
        # msg.attach(self._attach_image('5'))
        return msg.as_string()

    def send(self, subject, content):
        message = self._message(subject, content)
        try:
            server = smtplib.SMTP(self.smtp_server)
            server.ehlo()
            server.starttls()
            server.login(self.mail_from, self.password)
            server.sendmail(self.mail_from, self.mail_to, message.encode("utf-8"))
            server.quit()
            return True
        except Exception as e:
            print(e)


def mail_body():
    body = """
    <html>
    <head>

    </head>
    <body>
        <h2>测试标题</h2>
            <p class="section-text">测试文本1；</p>
            <br/>
            <p class="section-text">测试图片
            如下</p>
            <p><img src="cid:image1" class="img-responsive"></p>                  
    </body>
    </html>
    return body
    """
    return body


if __name__ == "__main__":
    pass
