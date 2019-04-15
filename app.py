from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import paramiko
import os
import time
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9z2SNrr86ZejumpU4hSMa5xry0tLD263V38C3twWNq9ZTr4eIkxTjPMNT3SHyeGzE/yk8JLxexC8M9kzcwAQQEQD6msApg7AaLAn0iV63HaiT7GbMld9wnu4A14261GorC87rWc0BNu603IrNCSzIAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('704ac71eddb12e51957d76b6d6bbf514')
i=0
j=0
prods_pic=[]
prods_webs=[]
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    #ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python test_ssh.py '+str(event.message.text),get_pty=True)
    fp = open("input.txt", "w")	 
    fp.write(str(event.message.text))	 
    fp.close()
    sftp.put('input.txt', 'input.txt')
# message = TextSendMessage(text="驗證碼")
#line_bot_api.reply_message(event.reply_token, message)
# message = ImageSendMessage(original_content_url=str(url),preview_image_url=str(url))
#line_bot_api.reply_message(event.reply_token, message)
# profile = line_bot_api.get_profile(user_id)
    user_id = event.source.user_id
    message = TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
    thumbnail_image_url='https://i.imgur.com/aumnJPq.png',
    title='Menu',
    text='Please select',
    actions=[
    PostbackTemplateAction(
        label='買東西',
        data='買東西'
    ),
    PostbackTemplateAction(
        label='登入',
        data='登入'
    )
    ]
    )
    )
    line_bot_api.push_message(user_id, message)
    ssh.close()
@handler.add(PostbackEvent)#,message=ButtonsTemplate)
def handle_postback(event):
    #postback=event
    user_id=event.source.user_id
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
    if (event.postback.data)=="帳號":
        message = TextSendMessage(text="請輸入帳號:")
        line_bot_api.push_message(user_id, message)
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message2(event):
            user_id = event.source.user_id
            ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python account.py '+str(event.message.text)+' '+str(user_id),get_pty=True)
            #message = TextSendMessage(text="收到")
            #line_bot_api.reply_message(event.reply_token, message)
            #postback.postback.data="break"
            #event=postback
    elif (event.postback.data)=="密碼":
        message = TextSendMessage(text="請輸入密碼:")
        line_bot_api.push_message(user_id, message)
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message3(event):
            ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python password.py '+str(event.message.text),get_pty=True)
            #message = TextSendMessage(text="收到")
            #line_bot_api.reply_message(event.reply_token, message)
    elif (event.postback.data)=="驗證碼":
        message = TextSendMessage(text="請輸入驗證碼:")
        line_bot_api.push_message(user_id, message)
        stdin,stdout,stderr=ssh.exec_command('python3 login.py')
        time.sleep(5)
        #os.system("0x1A")
        print(stdout.readline())
        if os.path.isfile("image2.txt"):
            os.remove('image2.txt')
        else:
            os.mknod("image2.txt")
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.get('image.txt', 'image2.txt')
        fp=open('image2.txt', 'r')
        url=fp.readline()
        fp.close()
        message = ImageSendMessage(original_content_url=str(url),preview_image_url=str(url))
        line_bot_api.push_message(user_id, message)
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message4(event):
            stdin.channel.send(str(event.message.text))
            stdin.channel.shutdown_write()
            #message = TextSendMessage(text="收到")
            #line_bot_api.reply_message(event.reply_token, message)  
    elif (event.postback.data)=="登入":      
        message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
        thumbnail_image_url='https://i.imgur.com/aumnJPq.png',
        title='Menu',
        text='Please select',
        actions=[
        PostbackTemplateAction(
            label='帳號',
            data='帳號'
        ),
        PostbackTemplateAction(
            label='密碼',
            data='密碼'
        ),
        PostbackTemplateAction(
            label='驗證碼',
            data='驗證碼'
        )
        ]
        )
        )
        line_bot_api.push_message(user_id, message)
    elif (event.postback.data)=="買東西":
        message = TextSendMessage(text="您要買甚麼呢?")
        line_bot_api.push_message(user_id, message) 
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message5(event):
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            fp = open("input.txt", "w")	 
            fp.write(str(event.message.text))	 
            fp.close()
            sftp.put('input.txt', 'input.txt')
        #stdin,stdout,stderr=ssh.exec_command('python3 auto_login.py')
        #if os.path.isfile("auto_image2.txt"):
            #os.remove('auto_image2.txt')
        #os.mknod("auto_image2.txt")
        #sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        #sftp = ssh.open_sftp()
        #sftp.get('auto_image.txt', 'auto_image2.txt')
        #fp=open('auto_image2.txt', 'r')
        #url=fp.readline()
        #fp.close()
            if os.path.isfile("prods_img2.txt"):
                os.remove('prods_img2.txt')
            else:
                os.mknod("prods_img2.txt")
            sftp.get('prods_img.txt', 'prods_img2.txt')
            with open('prods_img2.txt', 'r', encoding='UTF-8') as file:
                for line in file:
                    prods_pic.append(line.rstrip('\n'))
            i=0
            message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
            columns=[
            ImageCarouselColumn(
                image_url=prods_pic[i],
                action=PostbackTemplateAction(
                    label='Buy Now',
                    #text='',
                    data=str(i)
                )
            ),
            ImageCarouselColumn(
                image_url=prods_pic[i+1],
                action=PostbackTemplateAction(
                    label='Buy Now',
                    #text='',
                    data=str(i+1)
                )
            ),
            ImageCarouselColumn(
                image_url=prods_pic[i+2],
                action=PostbackTemplateAction(
                    label='Buy Now',
                    #text='',
                    data=str(i+2)
                )
            )
            ]
            )
            )
            line_bot_api.reply_message(event.reply_token, message)
    elif (event.postback.data)==str(i) or (event.postback.data)==str(i+1) or (event.postback.data)==str(i+2):
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        if os.path.isfile("prods_web2.txt"):
            os.remove('prods_web2.txt')
        else:
            os.mknod("prods_web2.txt")
        sftp.get('prods_web.txt', 'prods_web2.txt')
        z=0
        with open('prods_web2.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                prods_webs.append(line.rstrip('\n'))
        for web in prods_webs:
            print(web)  
        message = TextSendMessage(text="成功")
        line_bot_api.push_message(user_id, message)
        ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python3 purchase.py '+prods_webs[int(event.postback.data)],get_pty=True)
        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)