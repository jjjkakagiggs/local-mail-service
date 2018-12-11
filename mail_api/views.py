from django.shortcuts import render
from rest_framework.decorators import api_view
from function.utils import send_mail_fuc,mq_write
from django.http import HttpResponse,JsonResponse
import json,pika,threading
# Create your views here.

credentials = pika.PlainCredentials('test','123456')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '127.0.0.1',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='mail_balance',durable=True)# 声明queue


@api_view(['GET','POST','DELETE'])
def mail_service(request):
    if request.method=='GET':
        print("121")
        return HttpResponse('sss')
    elif request.method=='POST':
        pass
    elif request.method=='DELETE':
        pass

@api_view(['GET','POST','DELETE'])
def domain_management(request):
    if request.method=='GET':
        print("121")
        return HttpResponse('sss')
    elif request.method=='POST':
        pass
    elif request.method=='DELETE':
        pass
    

@api_view(['POST'])
def send_mail(request):
    if request.method=='POST':
        FROM=request.POST.get('From')
        TO=request.POST.get('To')
        SUBJECT=request.POST.get('Subject')
        TEXT=request.POST.get('Text')
        
        mq_write(channel,FROM,TO,SUBJECT,TEXT)
        return HttpResponse('success')