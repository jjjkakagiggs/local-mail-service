import pika
import json
import threading
credentials = pika.PlainCredentials('test','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='mail_balance',durable=True)# 声明queue
sem=threading.Semaphore(100)

def send_async_email(FROM,TO,SUBJECT,TEXT):
    # SERVER = 'localhost'
    # msg = MIMEMultipart('alternative')
    # # 包含了非ASCII字符，需要使用unicode
    # msg['Subject'] = SUBJECT
    # msg['From'] = FROM
    # msg['To'] = ', '.join(TO)
    # part = MIMEText(TEXT, 'plain', 'utf-8')
    # msg.attach(part)
    # server = smtplib.SMTP(SERVER)
    # server.sendmail(FROM, TO, msg.as_string().encode('ascii'))
    # server.quit()
    print(FROM, TO, SUBJECT, TEXT)


def send_mail_fuc(FROM,TO,SUBJECT,TEXT):
    with  sem:
        s=threading.Thread(target=send_async_email,args=[FROM,TO,SUBJECT,TEXT])
        s.start()
       

def read_callback(ch, method, properties, body):
    info_dict=json.loads(body)
    FROM, TO, SUBJECT, TEXT=info_dict['FROM'],info_dict['TO'],info_dict['SUBJECT'],info_dict['TEXT']
    send_mail_fuc(FROM,TO,SUBJECT,TEXT)

channel.basic_consume(read_callback,
                      queue='mail_balance',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()