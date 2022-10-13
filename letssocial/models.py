from django.db import models
from django.utils import timezone
from datetime import date
from datetime import datetime

# Create your models here.

class Useruploadedimage(models.Model):
    imageusername=models.CharField(max_length=100, default='')
    uploadedimage=models.ImageField(upload_to=f'letsocial/usersgallery/')
    def __str__(self):
        return self.imageusername+ '-' + str(self.uploadedimage)

class Userprofileimage(models.Model):
    profileimgusername=models.CharField(max_length=100, default='')
    uploadedprofileimage=models.ImageField(upload_to=f'letsocial/userprofileimages/')
    def __str__(self):
        return self.profileimgusername+ '-' + str(self.uploadedprofileimage)

class UserPosts(models.Model):
    postuser=models.CharField(default='',max_length=100)
    posttext=models.CharField(default='',max_length=1000)
    postimages=models.CharField(default='',max_length=5000)

class Userdescriptiondetails(models.Model):
    username=models.CharField(default='',max_length=100)
    userdesc=models.CharField(default='',max_length=300)
    def __str__(self):
        return self.username+ '-description'

class Friendrequestbyuser(models.Model):
    statuschoices=[
    ('norespond','No Respond'),
    ('reject','Rejected'),
    ('accept','Accepted'),
    ('block','Blocked'),
    ('cancel','Cancel Request'),
   ]
    userwhorequest=models.CharField(default='',max_length=300)
    approvername=models.CharField(default='',max_length=300)
    approvestatus=models.CharField(default='norespond',max_length=300,choices=statuschoices)
    def __str__ (self):
        return self.userwhorequest+"-"+self.approvername+", "+self.approvestatus

class Usercomments(models.Model):
    commentonpost=models.ForeignKey(UserPosts, on_delete=models.CASCADE)
    personwhocomment=models.CharField(default="", max_length=100)
    commenttext=models.CharField(default='', max_length=500)
    pub_date=models.DateField(default=timezone.datetime.now)
 
    def __str__(self):
        return str(self.commentonpost) + '-' + str(self.personwhocomment) + '-' + str(self.pub_date)

class Replycomments(models.Model):
    replyoncomment=models.ForeignKey(Usercomments, on_delete=models.CASCADE)
    personwhoreply=models.CharField(default="", max_length=100)
    replycommenttext=models.CharField(default='', max_length=500)
    pub_date=models.DateField(default=timezone.datetime.now)
    
    def __str__(self):
        return str(self.replyoncomment) + '-' + str(self.personwhoreply) + '-' + str(self.pub_date)

class Savechats(models.Model):
    
    cgroupname=models.CharField(default='',max_length=100)
    userwhomessage=models.CharField(default='',max_length=100)
    otheruser=models.CharField(default='',max_length=100)
    message=models.CharField(default='',max_length=1000)
    messagetime=models.DateTimeField(default=timezone.datetime.now)
    messagedate=models.DateField(default=date.today)
    messagett=models.TimeField(default=datetime.now)
    
    def __str__(self):
        return self.cgroupname+"-"+str(self.messagetime.date())+"-"+str(self.messagetime.time().hour)+":"+str(self.messagetime.time().minute)
        
