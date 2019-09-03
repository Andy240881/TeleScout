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
class MyException(Exception):
  def __init__(self, value):
    self.value = value
# Channel Access Token
line_bot_api = LineBotApi('9z2SNrr86ZejumpU4hSMa5xry0tLD263V38C3twWNq9ZTr4eIkxTjPMNT3SHyeGzE/yk8JLxexC8M9kzcwAQQEQD6msApg7AaLAn0iV63HaiT7GbMld9wnu4A14261GorC87rWc0BNu603IrNCSzIAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('704ac71eddb12e51957d76b6d6bbf514')
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
user_id=''
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global user_id
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
    user_id = event.source.user_id
    ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python build.py '+user_id,get_pty=True)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    fp = open("input.txt", "w")  
    fp.write(str(event.message.text))    
    fp.close()
    sftp.put('input.txt', '/home/4105056023/user_cookie/'+user_id+'/input2.txt')
    ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python3 QA.py '+user_id,get_pty=True)
    print(ssh_stdout.readlines())
    #自訂資料夾名稱
    newdir = user_id+'/'
    #判斷資料夾是否存在
    if not os.path.exists(newdir):
    #建立資料夾
        os.makedirs(newdir)
    if os.path.isfile(user_id+"/qa.txt"):
        os.remove(user_id+'/qa.txt')
        os.mknod(user_id+"/qa.txt")
    else:
        os.mknod(user_id+"/qa.txt")
    sftp.get('/home/4105056023/user_cookie/'+user_id+'/QA_result.txt', user_id+'/qa.txt')
    fp = open(user_id+'/qa.txt', "r")  
    action=fp.readline()    
    fp.close()
    print(action)
    print('\n')
    if action=='none':
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
            label='取消訂單',
            data='取消訂單'
        ),
        PostbackTemplateAction(
            label='登入',
            data='登入'
        )
        ]
        )
        )
        line_bot_api.push_message(user_id, message)
    elif action=='buy':
        message = TextSendMessage(text="您要買甚麼呢?")
        line_bot_api.push_message(user_id, message) 
        i=0
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message5(event):
            if event.message.text=="restart":
                return
            global user_id
            prods_pic=[]
            prods_prices=[]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            fp = open("input.txt", "w")  
            fp.write(str(event.message.text))    
            fp.close()
            sftp.put('input.txt', '/home/4105056023/user_cookie/'+user_id+'/input.txt')
            stdin,stdout,stderr=ssh.exec_command('python3 money/money.py '+user_id)
            time.sleep(2)
            stdin,stdout,stderr=ssh.exec_command('python3 pb/predict.py '+user_id)
            print(stderr.readlines())
            time.sleep(3)
            #自訂資料夾名稱
            newdir = user_id+'/'
            #判斷資料夾是否存在
            if not os.path.exists(newdir):
            #建立資料夾
                os.makedirs(newdir)
            if os.path.isfile(user_id+"/prods_img2.txt"):
                os.remove(user_id+'/prods_img2.txt')
                os.mknod(user_id+"/prods_img2.txt")
            else:
                os.mknod(user_id+"/prods_img2.txt")
            sftp.get('/home/4105056023/user_cookie/'+user_id+'/prods_img.txt', user_id+'/prods_img2.txt')
            with open(user_id+'/prods_img2.txt', 'r', encoding='UTF-8') as file:
                for line in file:
                    print(line)
                    prods_pic.append(line.rstrip('\n'))
            if os.path.isfile(user_id+"/prods_price2.txt"):
                os.remove(user_id+'/prods_price2.txt')
                os.mknod(user_id+"/prods_price2.txt")
            else:
                os.mknod(user_id+"/prods_price2.txt")
            sftp.get('/home/4105056023/user_cookie/'+user_id+'/prods_price.txt', user_id+'/prods_price2.txt')
            with open(user_id+'/prods_price2.txt', 'r', encoding='UTF-8') as file:
                for line in file:
                    print(line)
                    prods_prices.append(line.rstrip('\n'))
            print("delet")
            message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
            columns=[
            ImageCarouselColumn(
                image_url=prods_pic[i],
                action=PostbackTemplateAction(
                    label="$"+str(prods_prices[i]),
                    #text='',
                    data=str(i)
                )
            ),
            ImageCarouselColumn(
                image_url=prods_pic[i+1],
                action=PostbackTemplateAction(
                    label="$"+str(prods_prices[i+1]),
                    #text='',
                    data=str(i+1)
                )
            ),
            ImageCarouselColumn(
                image_url=prods_pic[i+2],
                action=PostbackTemplateAction(
                    label="$"+str(prods_prices[i+2]),
                    #text='',
                    data=str(i+2)
                )
            )
            ]
            )
            )
            line_bot_api.reply_message(event.reply_token, message)
            prods_pic.clear()
            prods_prices.clear()
    elif action=='cancel':
        refund_pic=[]
        refund_time=[]
        i=0
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        #stdin,stdout,stderr=ssh.exec_command('python3 refund_detail.py '+user_id)
        #time.sleep(8)
        sftp.get('/home/4105056023/user_cookie/'+user_id+'/refund_img.txt', 'refund_img2.txt')
        with open('refund_img2.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                print(line)
                refund_pic.append(line.rstrip('\n'))
        sftp.get('/home/4105056023/user_cookie/'+user_id+'/refund_time.txt', 'refund_time2.txt')
        with open('refund_time2.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                print(line)
                refund_time.append(line.rstrip('\n'))
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
            columns=[
            ImageCarouselColumn(
                image_url=refund_pic[i],
                action=PostbackTemplateAction(
                    label=str(refund_time[i]),
                    #text='',
                    data='a'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+1],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+1]),
                    #text='',
                    data='b'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+2],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+2]),
                    #text='',
                    data='c'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+3],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+3]),
                    #text='',
                    data='d'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+4],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+4]),
                    #text='',
                    data='e'
                )
            )
            ]
            )
            )
        line_bot_api.push_message(user_id, message)
        refund_pic.clear()
        refund_time.clear()
    elif action=='login':
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
@handler.add(PostbackEvent)
def handle_postback(event):
    global user_id
    user_id=event.source.user_id
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
    if (event.postback.data)=="帳號":
        message = TextSendMessage(text="請輸入帳號:")
        line_bot_api.push_message(user_id, message)
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message2(event):
            global user_id
            user_id = event.source.user_id
            ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python account.py '+str(event.message.text)+' '+str(user_id),get_pty=True)
    elif (event.postback.data)=="密碼":
        message = TextSendMessage(text="請輸入密碼:")
        line_bot_api.push_message(user_id, message)
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message3(event):
            ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python password.py '+str(event.message.text),get_pty=True)
    elif (event.postback.data)=="驗證碼":
        message = TextSendMessage(text="請輸入驗證碼:")
        line_bot_api.push_message(user_id, message)
        stdin,stdout,stderr=ssh.exec_command('python3 login.py '+str(user_id),get_pty = True)
        time.sleep(5)
        if os.path.isfile("image2.txt"):
            os.remove('image2.txt')
            os.mknod("image2.txt")
        else:
            os.mknod("image2.txt")
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.get("/home/4105056023/user_cookie/"+str(user_id)+"/image.txt", 'image2.txt')
        fp=open('image2.txt', 'r')
        url=fp.readline()
        fp.close()
        message = ImageSendMessage(original_content_url=str(url),preview_image_url=str(url))
        line_bot_api.push_message(user_id, message)
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message4(event):
            stdin.channel.send(str(event.message.text))
            stdin.channel.shutdown_write()
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
    elif(event.postback.data=="買東西" and user_id==event.source.user_id):
        user_id=event.source.user_id
        message = TextSendMessage(text="您要買甚麼呢?")
        line_bot_api.push_message(user_id, message) 
        i=0
        @handler.add(MessageEvent, message=TextMessage)
        def handle_message5(event):
            global user_id
            if event.message.text=="restart":
                message = TextSendMessage(text="需要甚麼服務呢?")
                line_bot_api.push_message(user_id, message) 
                return None
            prods_pic=[]
            prods_prices=[]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            sftp = ssh.open_sftp()
            fp = open("input.txt", "w")  
            fp.write(str(event.message.text))    
            fp.close()
            sftp.put('input.txt', '/home/4105056023/user_cookie/'+user_id+'/input.txt')
            stdin,stdout,stderr=ssh.exec_command('python3 money/money.py '+user_id)
            time.sleep(2)
            stdin,stdout,stderr=ssh.exec_command('python3 pb/predict.py '+user_id)
            print(stderr.readlines())
            time.sleep(3)
            #自訂資料夾名稱
            newdir = user_id+'/'
            #判斷資料夾是否存在
            if not os.path.exists(newdir):
            #建立資料夾
                os.makedirs(newdir)
            if os.path.isfile(user_id+"/prods_img2.txt"):
                os.remove(user_id+'/prods_img2.txt')
                os.mknod(user_id+"/prods_img2.txt")
            else:
                os.mknod(user_id+"/prods_img2.txt")
            sftp.get('/home/4105056023/user_cookie/'+user_id+'/prods_img.txt', user_id+'/prods_img2.txt')
            with open(user_id+'/prods_img2.txt', 'r', encoding='UTF-8') as file:
                for line in file:
                    print(line)
                    prods_pic.append(line.rstrip('\n'))
            if os.path.isfile(user_id+"/prods_price2.txt"):
                os.remove(user_id+'/prods_price2.txt')
                os.mknod(user_id+"/prods_price2.txt")
            else:
                os.mknod(user_id+"/prods_price2.txt")
            sftp.get('/home/4105056023/user_cookie/'+user_id+'/prods_price.txt', user_id+'/prods_price2.txt')
            with open(user_id+'/prods_price2.txt', 'r', encoding='UTF-8') as file:
                for line in file:
                    print(line)
                    prods_prices.append(line.rstrip('\n'))
            print("delet")
            message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
            columns=[
            ImageCarouselColumn(
                image_url=prods_pic[i],
                action=PostbackTemplateAction(
                    label="$"+str(prods_prices[i]),
                    #text='',
                    data=str(i)
                )
            ),
            ImageCarouselColumn(
                image_url=prods_pic[i+1],
                action=PostbackTemplateAction(
                    label="$"+str(prods_prices[i+1]),
                    #text='',
                    data=str(i+1)
                )
            ),
            ImageCarouselColumn(
                image_url=prods_pic[i+2],
                action=PostbackTemplateAction(
                    label="$"+str(prods_prices[i+2]),
                    #text='',
                    data=str(i+2)
                )
            )
            ]
            )
            )
            line_bot_api.reply_message(event.reply_token, message)
            prods_pic.clear()
            prods_prices.clear()
    elif (event.postback.data)=="0" or (event.postback.data)=="1" or (event.postback.data)=="2":
        prods_webs=[]
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        if os.path.isfile("prods_web2.txt"):
            os.remove('prods_web2.txt')
        else:
            os.mknod("prods_web2.txt")
        sftp.get('/home/4105056023/user_cookie/'+user_id+'/prods_web.txt', 'prods_web2.txt')
        z=0
        with open('prods_web2.txt', 'r') as file:
            for line in file:
                prods_webs.append(line.rstrip('\n'))
        for web in prods_webs:
            print(web)  
        message = TextSendMessage(text="成功")
        line_bot_api.push_message(user_id, message)
        url=str(prods_webs[int(event.postback.data)])
        ssh_stdin,ssh_stdout,ssh_stderr=ssh.exec_command('python3 purchase.py '+url+" "+str(user_id))
        print(prods_webs[int(event.postback.data)])
        print(ssh_stderr.readlines())
    elif (event.postback.data)=="取消訂單":
        refund_pic=[]
        refund_time=[]
        i=0
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        stdin,stdout,stderr=ssh.exec_command('python3 refund_detail.py '+user_id)
        print(stderr.readlines())
        time.sleep(8)
        sftp.get('/home/4105056023/user_cookie/'+user_id+'/refund_img.txt', 'refund_img2.txt')
        with open('refund_img2.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                print(line)
                refund_pic.append(line.rstrip('\n'))
        sftp.get('/home/4105056023/user_cookie/'+user_id+'/refund_time.txt', 'refund_time2.txt')
        with open('refund_time2.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                print(line)
                refund_time.append(line.rstrip('\n'))
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
            columns=[
            ImageCarouselColumn(
                image_url=refund_pic[i],
                action=PostbackTemplateAction(
                    label=str(refund_time[i]),
                    #text='',
                    data='a'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+1],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+1]),
                    #text='',
                    data='b'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+2],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+2]),
                    #text='',
                    data='c'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+3],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+3]),
                    #text='',
                    data='d'
                )
            ),
            ImageCarouselColumn(
                image_url=refund_pic[i+4],
                action=PostbackTemplateAction(
                    label=str(refund_time[i+4]),
                    #text='',
                    data='e'
                )
            )
            ]
            )
            )
        line_bot_api.push_message(user_id, message)
        refund_pic.clear()
        refund_time.clear()
    elif (event.postback.data)=='a' or (event.postback.data)=='b' or (event.postback.data)=='c' or (event.postback.data)=='d' or (event.postback.data)=='e':
        refund_id=[]
        if (event.postback.data)=='a':
            i=0
        elif (event.postback.data)=='b':
            i=1
        elif (event.postback.data)=='c':
            i=2
        elif (event.postback.data)=='d':
            i=3
        elif (event.postback.data)=='e':
            i=4        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("140.120.13.251",6023,"4105056023","4105056019")
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        sftp = ssh.open_sftp()
        sftp.get('/home/4105056023/user_cookie/'+user_id+'/refund_id.txt', 'refund_id2.txt')
        with open('refund_id2.txt', 'r', encoding='UTF-8') as file:
            for line in file:
                print(line)
                refund_id.append(line.rstrip('\n'))
        stdin,stdout,stderr=ssh.exec_command('python3 refund.py '+user_id+' '+str(refund_id[i]))
        output=str(stdout.readlines()[0].rstrip('\n'))
        message = TextSendMessage(text=output)
        line_bot_api.push_message(user_id, message) 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
