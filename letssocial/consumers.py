import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Savechats
from django.utils import timezone
import datetime
from django.db.models import Q

class MyChatConsumer(WebsocketConsumer):
    def connect(self):
        self.username=self.scope['url_route']['kwargs']['username']
        self.otherusername=self.scope['url_route']['kwargs']['otherusername']
        self.roomname=self.username+self.otherusername
        namelist=[self.username,self.otherusername]
        namelist.sort()
        # print(namelist)
        self.groupname=f'chat_{namelist[0]}{namelist[1]}'
        
        # print(self.groupname,self.username,self.otherusername)
        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
        )
      
        self.accept()
        print("connect")
    
    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.groupname,
            self.channel_name
        )
      
        # self.disconnect()
    
    def receive(self, text_data):
        jsondata=json.loads(text_data)
        wsmsg=jsondata['chatmsg']
        personname=jsondata['person']
        otherpersonname=jsondata['otherperson']
        msgtime=timezone.datetime.now()
        print(self.groupname, personname, wsmsg, otherpersonname)
        chatobj=Savechats(cgroupname=self.groupname,userwhomessage=personname,otheruser=otherpersonname,message=wsmsg)
        chatobj.save()
         
        async_to_sync(self.channel_layer.group_send)(
            self.groupname,
            {
                'type':'groupchatmessage',
                'groupnamemsg':wsmsg,
                'personname':personname,
                'otherpersonname': otherpersonname,
                'msgtime':str(msgtime.strftime("%H:%M"))
            }
        )
        
    def groupchatmessage(self,event):
        sendwsmsg=event['groupnamemsg']    
        sendername=event['personname']    
        recievername=event['otherpersonname']    
        msgtime=event['msgtime']
        # print(msgtime)
        # print(event)
        
        chatdatecheck=Savechats.objects.filter(Q(messagedate=str(datetime.date.today())) & Q(userwhomessage=str(sendername)) & Q(otheruser=str(recievername)))
        chatmsgcheck=Savechats.objects.filter(Q(message=str(sendwsmsg)) & Q(userwhomessage=str(sendername)) & Q(otheruser=str(recievername))).latest("id")
        
        newmsgdate=None        
        if chatdatecheck[0].message == sendwsmsg and str(chatdatecheck[0].id) == str(chatmsgcheck.id) :
            newmsgdate="Today"
            
        print(chatdatecheck[0].id,chatmsgcheck.id)
        self.send(text_data=json.dumps({
            "newmsg":sendwsmsg,
            "personname":sendername,
            'messagetime':msgtime,
            'newmsgdate':newmsgdate
        }))     
       