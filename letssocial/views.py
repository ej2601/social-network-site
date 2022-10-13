import datetime
from django.shortcuts import redirect, render,HttpResponse,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
from .models import Replycomments, Savechats, Usercomments, Useruploadedimage,UserPosts, Userprofileimage,Userdescriptiondetails,Friendrequestbyuser
import re
from django.db.models import Q
from django.urls import reverse

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        usergallery=[]         
        usergallerydata=Useruploadedimage.objects.filter(imageusername=request.user.username)     
        for i in usergallerydata:
            usergallery.append(i.uploadedimage)
            
        listofuserposts=UserPosts.objects.filter(postuser=request.user.username)
        listofpostsdetails=[]
        for j in listofuserposts:
            postid=j.id
            postusername=j.postuser
            postimages=list(str(j.postimages).replace("[",'').replace("]",'').replace('http://127.0.0.1:8000/','').replace("'",'').split(sep=','))
            posttext=j.posttext
            # print(re.search("\S",posttext))
            if re.search("\S",j.posttext) == None :
                posttext='nocontent'
            commentscount=len(list(j.usercomments_set.all()))
            # print(commentscount)    
            tupleofpost=(postid,postusername,postimages,posttext,commentscount)  
            # print(tupleofpost)
            listofpostsdetails.append(tupleofpost)
        listofpostsdetails.sort(reverse=1)
        if listofpostsdetails == []:
            listofpostsdetails='nouserposts'

        acceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='accept'))]
        acceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='accept'))]
        friendlist=[]
        friendlist.extend(acceptedfriendrequestfilter)
        friendlist.extend(acceptfriendrequestfilter) 
        
        friendspostslist=[]
        for k in friendlist:       
            listofuserfriendsposts=UserPosts.objects.filter(postuser=k)
            listoffriendpostsdetails=[]
            for j in listofuserfriendsposts:
                postid=j.id
                postusername=j.postuser
                postuser=User.objects.get(username=j.postuser)
                postuserfname=postuser.first_name
                postuserlname=postuser.last_name
                postuserprofileimg=Userprofileimage.objects.get(profileimgusername=j.postuser)
                postimages=list(str(j.postimages).replace("[",'').replace("]",'').replace('http://127.0.0.1:8000/','').replace("'",'').split(sep=','))
                posttext=j.posttext
                friendpostcommentcount=len(list(j.usercomments_set.all()))
                # print(friendpostcommentcount)
                # print(re.search("\S",posttext))
                if re.search("\S",j.posttext) == None :
                    posttext='nocontent'
                tupleofpost=(postid,postimages,posttext,postusername,postuserfname,postuserlname,postuserprofileimg,friendpostcommentcount)  
                # print(tupleofpost)
                listoffriendpostsdetails.append(tupleofpost)
            friendspostslist.extend(listoffriendpostsdetails)   
        friendspostslist.sort(reverse=1)
        if friendspostslist == []:
                friendspostslist='nouserposts'
        profileimagelist=Userprofileimage.objects.filter(profileimgusername=request.user.username)
        profileimage=None    
        if list(profileimagelist) != []:
            profileimage=profileimagelist.latest("id")
        # print(profileimage, 'hello world')
        userdescriptionvalue=''
        if list(Userdescriptiondetails.objects.filter(username=request.user.username)) != []:
                userdescriptionvalue=Userdescriptiondetails.objects.get(username=request.user.username).userdesc
        
        friendlist=[]
        acceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='accept'))]
        acceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='accept'))]
        friendlist.extend(acceptedfriendrequestfilter)
        friendlist.extend(acceptfriendrequestfilter)
        friendscount=len(friendlist)
        
          
        context={'usergallery':usergallery, "postslist":listofpostsdetails,"profileimage":profileimage, "userdescription":userdescriptionvalue, "friendpostslist":friendspostslist,'friendscount': friendscount}      
        return render(request,'letsocial/index.html',context)  

def updateprofilephoto(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        if request.method == 'POST':
            uploadedprofileimage=request.FILES['imguploadbyuser']

            if list(Userprofileimage.objects.filter(profileimgusername=request.user.username)) != []:
                profileimage=Userprofileimage.objects.get(profileimgusername=request.user.username)
                profileimage.uploadedprofileimage=uploadedprofileimage
                profileimage.save()
            else:
                profileimage=Userprofileimage(profileimgusername=request.user.username,uploadedprofileimage=uploadedprofileimage)
                profileimage.save()
            # print(uploadedprofileimage) 
            return redirect('letsocial:index')

def deleteprofileimage(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        profileimg=Userprofileimage.objects.get(profileimgusername=request.user.username)
        profileimg.delete()
        return redirect('letsocial:index')

def updateuserdescription(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        if request.method == 'POST':
            userdesc=request.POST['userdescription']
            # print(list(Userdescriptiondetails.objects.filter(username=request.user.username)))
            if list(Userdescriptiondetails.objects.filter(username=request.user.username)) != []:
                updateuserdesc=Userdescriptiondetails.objects.get(username=request.user.username)
                updateuserdesc.userdesc=userdesc
                updateuserdesc.save()
            else:
                newuserdesc=Userdescriptiondetails.objects.create(username=request.user.username,userdesc=userdesc)
                newuserdesc.save()
            # print(userdesc)
            return redirect('letsocial:index')

def uploadimages(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        if request.method == 'POST':
           print(request.FILES.getlist('images'))
           if  request.FILES.getlist('images') != []:
                for i in request.FILES.getlist('images'):
                        imagedata= Useruploadedimage(imageusername=request.user.username,uploadedimage=i)
                        imagedata.save()
                # print(request.FILES, request.POST)
                return redirect('letsocial:index')

           elif  request.FILES.getlist('imagesfrompost') != []:
                for i in request.FILES.getlist('imagesfrompost'):
                        imagedata= Useruploadedimage(imageusername=request.user.username,uploadedimage=i)
                        imagedata.save()
                # print(request.FILES, request.POST)
                return redirect('letsocial:makepost')

def deleteimagesfromgallery(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        if request.method == 'POST':
            delimageslist=request.POST.getlist('images')
            for i in delimageslist:
                delimage=Useruploadedimage.objects.get(uploadedimage=i)
                delimage.delete()

        return redirect('letsocial:index')
         
def deletepost(request,postid):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        posttodelete=UserPosts.objects.get(id=postid)
        posttodelete.delete()
        return redirect('letsocial:index')
         
def makepost(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        usergallery=[]         
        usergallerydata=Useruploadedimage.objects.filter(imageusername=request.user.username)
        for i in usergallerydata:
            usergallery.append(i.uploadedimage)

        context={'usergallery':usergallery}  
        return render(request,'letsocial/makepost.html',context)        

def postcreated(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
         if request.method == 'POST':
             imagesforpost=list(request.POST.getlist('imagesforpost'))
             if imagesforpost == []:
                imagesforpost = 'norichcontent'


             textforpost=request.POST['posttext'].replace("  "," ")
             if re.search("\S",textforpost) == None and imagesforpost == 'norichcontent':
                # print(imagesforpost)
                return redirect('letsocial:makepost')
             else:   
                userpost=UserPosts(postuser=request.user.username,postimages=imagesforpost,posttext=textforpost)
                userpost.save()
                return redirect('letsocial:index')
         else:       
            return redirect('letsocial:index')

def viewgallery(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
         return render(request,'letsocial/gallerypage.html')     

def loginpage(request):
    return render(request,'letsocial/loginuser.html')

def loginuser(request):
      if request.method == "POST":
        username=request.POST['username']       
        password=request.POST['password']       
        user = authenticate(username=username, password=password)
        # print(username,password)
        if user is not None:
            login(request,user)
            return redirect('letsocial:index')
        else:
            return redirect('letsocial:loginpage')
      else:
        return redirect('letsocial:loginpage')

def logoutuser(request):
    logout(request)
    return redirect('letsocial:loginpage')
    
def registerpage(request):
    return render(request,'letsocial/registeruser.html')
    
def registeruser(request):
    if request.method == "POST":
        username=request.POST['username']       
        firstname=request.POST['firstname']       
        lastname=request.POST['lastname']       
        email=request.POST['email']       
        password=request.POST['password']       
        gender=request.POST['gender']
        # print(username,lastname,email,password,gender,firstname)

        user=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
        user.groups.set((int(gender),))
        user.save()

        return redirect('letsocial:loginpage')
    else:
        return redirect('letsocial:registerpage')

def profilepage(request):
        if request.user.is_anonymous:
            return redirect('letsocial:loginpage')
        else:
         return render(request,'letsocial/profile.html')

alert=None
def userpersonalinfo(request):
        global alert
        if request.user.is_anonymous:
            return redirect('letsocial:loginpage')
        else:
            context= {'alert':alert}
            alert=None  
            return render(request,'letsocial/personalinfopage.html',context)
       
def changepassword(request):
        global alert
        if request.user.is_anonymous:
            return redirect('letsocial:loginpage')
        else:
            if request.method == "POST":
                oldpass=request.POST['oldpass']
                newpass=request.POST['newpass']
                confirmpass=request.POST['confirmpass']
                user=User.objects.get(username=request.user.username)
                chkoldpass=authenticate(username=request.user.username,password=oldpass)

                if chkoldpass is not None:
                    if newpass == confirmpass:
                        user.set_password(newpass)
                        user.save()
                        login(request,user)
                        alert='passchanged'
                    else:
                        alert='confirmnotmatch'
                        # print('pass not same')
                else:
                    alert='oldiswrong'
                    # print('old is incorrect')    
                
            

            return redirect("letsocial:personalinfo")

def changeotherinfo(request):
        global alert
        if request.user.is_anonymous:
            return redirect('letsocial:loginpage')
        else:
            if request.method == "POST":
                alert='infosave'
                firstname=request.POST['firstname']
                lastname=request.POST['lastname']
                email=request.POST['email']
                user=User.objects.get(username=request.user.username)
                user.first_name=firstname
                user.last_name=lastname
                user.email=email
                user.save()
                # print(firstname)

        return redirect("letsocial:personalinfo")

def forgotpassfirststep(request):
     if request.user.is_anonymous:
            return render(request, 'letsocial/forgotpassworduser.html')
     else:
        return redirect("letsocial:personalinfo")

def forgotpasssecondstep(request):
     if request.user.is_anonymous:
             if request.method == "POST":
                username=request.POST['username']
                users=User.objects.all()
                userlist=[i.username for i in users]

                if username not in userlist:
                    # print('not ok')
                    return redirect("letsocial:forgotpassuser")
                else:
             
                    otp=random.randint(100000,999999)
                    request.session['otp']=otp
                    request.session['otpusername']=username
                    print(otp,dict(request.session))
                    return render(request, 'letsocial/forgotpasswordotp.html')
             else:
                    return redirect("letsocial:loginpage")

                
     else:
        return redirect("letsocial:personalinfo")

def forgotpassthirdstep(request):
     if request.user.is_anonymous:
             if request.method == "POST":
                userotp=request.POST['otp']
                if int(userotp) == int(request.session['otp']):
                    return render(request, 'letsocial/forgotpasswordchange.html')     
                else:
                    print("correct otp is" ,request.session['otp'])
                    return redirect("letsocial:forgotpassuser")
             else:
                    return redirect("letsocial:loginpage")              
     else:
        return redirect("letsocial:personalinfo")

def forgotpassfinish(request):
     if request.user.is_anonymous:
             if request.method == "POST":
                newpass=request.POST['newpassword']
                confirmpass=request.POST['confirmpassword']
                if newpass == confirmpass:
                    user=User.objects.get(username=request.session['otpusername'])
                    user.set_password(newpass)
                    user.save()
                    return redirect('letsocial:loginpage')
                    
                else:
                    return redirect("letsocial:forgotpasschange")
             else:
                    return redirect("letsocial:loginpage")         
     else:
        return redirect("letsocial:personalinfo")

def deleteaccount(request):
 if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
 else:
        user=User.objects.get(username=request.user.username)
        user.delete()
        # print(user)
        return redirect('letsocial:profilepage')

def forgotuserfirststep(request):
     if request.user.is_anonymous:
            return render(request, 'letsocial/forgotuser.html')
     else:
        return redirect("letsocial:personalinfo")

def forgotuserlaststep(request):
     if request.user.is_anonymous:
            if request.method == "POST":
                useremail=request.POST['email']
                users=User.objects.all()
                emaillist=[i.email for i in users]            
                if useremail in emaillist:
                    emailusers=User.objects.filter(email=useremail)
                    print([i.username for i in emailusers])
                    return redirect('letsocial:loginpage')
                else:
                    return redirect("letsocial:forgotuserfirst")
            else:
                    return redirect("letsocial:loginpage")         
     else:
        return redirect("letsocial:personalinfo")

def people(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        userslistindatabase=User.objects.all()
        userlist=[]
        if request.method == "POST":
             usernamesofsearchlistusers=[]
             postdata= request.POST.get('peoplesearch').split(" ")  
             firstnametosearch=postdata[0]
             lastnametosearch="samplelastname"
             if len(postdata) == 2:  
                lastnametosearch=postdata[1]   
             
             exactfilterlist=User.objects.filter(Q(first_name__iexact=firstnametosearch) & Q(last_name__iexact=lastnametosearch))
            #  containfilterlist=User.objects.filter(Q(first_name__icontains=firstnametosearch) & Q(last_name__icontains=lastnametosearch)) 
             firstnamefilterlist=User.objects.filter(first_name__iexact=firstnametosearch).exclude(last_name__iexact=lastnametosearch) 
             lastnamefilterlist=User.objects.exclude(first_name__iexact=firstnametosearch).filter(last_name__iexact=lastnametosearch) 
             
             usernamesofsearchlistusers.extend(exactfilterlist)
             usernamesofsearchlistusers.extend(lastnamefilterlist)
             usernamesofsearchlistusers.extend(firstnamefilterlist)
            #  usernamesofsearchlistusers.extend(containfilterlist)
             userslistindatabase=usernamesofsearchlistusers   
             print(usernamesofsearchlistusers)
                
      
        for i in userslistindatabase:
            if(i.username != request.user.username):
                otheruserprofileimgfilter=list(Userprofileimage.objects.filter(profileimgusername=i.username))
                if otheruserprofileimgfilter == []:
                    # print(otheruserprofileimgfilter)
                    otheruserprofileimg=None
                else:
                    # print(otheruserprofileimgfilter,'hello')
                    otheruserprofileimg=Userprofileimage.objects.get(profileimgusername=i.username)
                
                tupleofuserdetail=(i,otheruserprofileimg)
                userlist.append(tupleofuserdetail)
        norespondfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='norespond'))]
        rejectfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='reject'))]
        acceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='accept'))]
        acceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='accept'))]
        friendlist=[]
        friendlist.extend(acceptedfriendrequestfilter)
        friendlist.extend(acceptfriendrequestfilter)
        blockfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='block'))]
        cancelfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='cancel'))]
        friendrequeststatuslist=[norespondfriendrequestfilter,rejectfriendrequestfilter,friendlist,blockfriendrequestfilter,cancelfriendrequestfilter]
   
        print(friendrequeststatuslist)
            #  print(firstnametosearch,lastnametosearch)    
        context={"userlist":set(userlist),"frslist":friendrequeststatuslist}
       
        return render(request,'letsocial/peoplespage.html',context)        

def otherpersonprofileview(request,id):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        userofprofileview=get_object_or_404(User,id=id)
        profileimagelist=Userprofileimage.objects.filter(profileimgusername=userofprofileview.username)
        profileimage=None    
        if list(profileimagelist) != []:
            profileimage=Userprofileimage.objects.get(profileimgusername=userofprofileview.username)
        
        otheruserdescriptionvalue=''
        if list(Userdescriptiondetails.objects.filter(username=userofprofileview.username)) != []:
                otheruserdescriptionvalue=Userdescriptiondetails.objects.get(username=userofprofileview.username).userdesc
        
      
        listofotheruserposts=UserPosts.objects.filter(postuser=userofprofileview.username)
        listofpostsdetails=[]
        for j in listofotheruserposts:
            postid=j.id
            postusername=j.postuser
            postimages=list(str(j.postimages).replace("[",'').replace("]",'').replace('http://127.0.0.1:8000/','').replace("'",'').split(sep=','))
            posttext=j.posttext
            commentscount=len(list(j.usercomments_set.all()))
            # print(re.search("\S",posttext))
            if re.search("\S",j.posttext) == None :
                posttext='nocontent'
            tupleofpost=(postid,postusername,postimages,posttext,commentscount)  
            # print(tupleofpost)
            listofpostsdetails.append(tupleofpost)
        listofpostsdetails.sort(reverse=1)
        if listofpostsdetails == []:
            listofpostsdetails='nouserposts'
       
        friendlist=[]
        acceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=userofprofileview.username,approvestatus='accept'))]
        acceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=userofprofileview.username,approvestatus='accept'))]
        friendlist.extend(acceptedfriendrequestfilter)
        friendlist.extend(acceptfriendrequestfilter)
        friendscount=len(friendlist)
        print(friendlist)
        
        context={"user":userofprofileview,'otheruserprofileimg':profileimage,'otheruserdesc':otheruserdescriptionvalue,'userpostlist':listofpostsdetails,"friendscount":friendscount}
        return render(request,'letsocial/otherpersonprofileview.html',context)        

def addfriend(request,id):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        friendrequesttouser=get_object_or_404(User,id=id)
        print(friendrequesttouser)
        requesteduser=Friendrequestbyuser(userwhorequest=request.user.username,approvername=friendrequesttouser.username)
        requesteduser.save()
        return redirect('letsocial:peoplepage')

def cancelfriendrequest(request,cancelrequesttouser):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        canceltouser=Friendrequestbyuser.objects.filter(approvername=cancelrequesttouser).latest('id')
        canceltouser.approvestatus='cancel'
        canceltouser.save()
        return redirect('letsocial:peoplepage')

def friends(request):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        userslistindatabase=User.objects.all()
        userlist=[]
      
        for i in userslistindatabase:
            if(i.username != request.user.username):
                otheruserprofileimgfilter=list(Userprofileimage.objects.filter(profileimgusername=i.username))
                if otheruserprofileimgfilter == []:
                    # print(otheruserprofileimgfilter)
                    otheruserprofileimg=None
                else:
                    # print(otheruserprofileimgfilter,'hello')
                    otheruserprofileimg=Userprofileimage.objects.get(profileimgusername=i.username)
                
                tupleofuserdetail=(i,otheruserprofileimg)
                userlist.append(tupleofuserdetail)
        
        friendlist=[]
        sendfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='norespond'))]
        recievefriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='norespond'))]
        acceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='accept'))]
        acceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='accept'))]
        friendlist.extend(acceptedfriendrequestfilter)
        friendlist.extend(acceptfriendrequestfilter)
        blockfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='block'))]
        cancelfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='cancel'))]
        
        chatslistwithdate=[]
        msgasotheruser=[(datetime.datetime.strftime(i.messagetime,"%j-%H-%M-%S"), i.userwhomessage) for i in list(Savechats.objects.filter(otheruser=request.user.username))]
        msgasuser=[(datetime.datetime.strftime(i.messagetime,"%j-%H-%M-%S"), i.otheruser) for i in list(Savechats.objects.filter(userwhomessage=request.user.username))]
        
        chatslistwithdate.extend(msgasotheruser)
        chatslistwithdate.extend(msgasuser)
        chatslistwithdate.sort(reverse=1)
        chatslist=[i[1] for i in chatslistwithdate]
        # print(chatslist,friendlist)
        
        chatwithfriend=[]
        for i in chatslist:
            chatwithuser=User.objects.get(username=i)
            chatwithuserprofileimg=Userprofileimage.objects.get(profileimgusername=chatwithuser.username)
            chatwithfriendmsg=Savechats.objects.filter(Q(userwhomessage=request.user.username) & Q(otheruser=chatwithuser.username) | Q(userwhomessage=chatwithuser.username) & Q(otheruser=request.user.username)).latest("messagetime")
            tupleofchatwithuserdetail=(chatwithuser,chatwithuserprofileimg,chatwithfriendmsg)
            print(chatwithfriendmsg)
            if tupleofchatwithuserdetail not in chatwithfriend:
                chatwithfriend.append(tupleofchatwithuserdetail)
                
        
        # print(chatwithfriend)      
        
        if sendfriendrequestfilter == []:
            sendfriendrequestfilter=None
            
        if chatslist == []:
            chatslist=None
            
        if chatwithfriend == []:
            chatwithfriend=None
            
        if recievefriendrequestfilter == []:
            recievefriendrequestfilter=None
        
        if friendlist == []:
            friendlist=None
        
        friendrequeststatuslist=[sendfriendrequestfilter,recievefriendrequestfilter,friendlist,blockfriendrequestfilter,cancelfriendrequestfilter,chatslist, chatwithfriend]
        # print(friendrequeststatuslist)
        context={"userlist":set(userlist),"frslist":friendrequeststatuslist}
        return render(request,'letsocial/friendspage.html',context)        

def acceptrequest(request,username):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        friendrequeststatus=Friendrequestbyuser.objects.filter(approvername=request.user.username,userwhorequest=username).latest("id")
        friendrequeststatus.approvestatus='accept'
        friendrequeststatus.save()

      
    return redirect('letsocial:friendspage')        

def rejectrequest(request,username):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        
        friendrequeststatus=Friendrequestbyuser.objects.filter(approvername=request.user.username,userwhorequest=username).latest("id")
        friendrequeststatus.approvestatus='reject'
        friendrequeststatus.save()

    return redirect('letsocial:friendspage')        
        
def postcommentpage(request,id):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        commentedpost=UserPosts.objects.get(id=id)
        userofpost=User.objects.get(username=commentedpost.postuser)
        postuserprofileimgfilter=list(Userprofileimage.objects.filter(profileimgusername=commentedpost.postuser))
        
        postid=commentedpost.id
        postusername=commentedpost.postuser
        postimages=list(str(commentedpost.postimages).replace("[",'').replace("]",'').replace('http://127.0.0.1:8000/','').replace("'",'').split(sep=','))
        posttext=commentedpost.posttext
        # print(re.search("\S",posttext))
        if re.search("\S",commentedpost.posttext) == None :
            posttext='nocontent'
        tupleofpost=(postid,postusername,postimages,posttext)  
             
        if postuserprofileimgfilter == []:
            postuserprofileimg=None
        else:
            postuserprofileimg=postuserprofileimgfilter[0]
        # print(postuserprofileimg)
        postcomments=[]
        
        # print(list(commentedpost.usercomments_set.all()))
        if list(commentedpost.usercomments_set.all()) != []:
            for i in commentedpost.usercomments_set.all(): 
                commenterprofileimgfilter=Userprofileimage.objects.filter(profileimgusername=i.personwhocomment)
                commentdetail=User.objects.get(username=i.personwhocomment)
                replycommentonthiscommentlist=i.replycomments_set.all()
                replieslist=[]
                if list(replycommentonthiscommentlist) == []:
                    replieslist="noreply"
                    print(replieslist)
                else:
                    for j in replycommentonthiscommentlist:
                        replycommenterprofileimgfilter=Userprofileimage.objects.filter(profileimgusername=j.personwhoreply)
                        replycommentuserdetail=User.objects.get(username=j.personwhoreply)
                        
                        if list(commenterprofileimgfilter) == []:
                            replycommenterprofileimg=None
                        else:
                            replycommenterprofileimg=Userprofileimage.objects.get(profileimgusername=j.personwhoreply)
                        replycommentsonthiscomment=(j.id, j, replycommenterprofileimg,replycommentuserdetail) 
                        replieslist.append(replycommentsonthiscomment)
                        
                    replieslist.sort(reverse=1)
                    
                    
                if list(commenterprofileimgfilter) == []:
                        commenterprofileimg=None
                else:
                        commenterprofileimg=Userprofileimage.objects.get(profileimgusername=i.personwhocomment)
                
                postcomments.append((i.id,i,commenterprofileimg,commentdetail,replieslist))
        
        if postcomments == []:
            postcomments = 'nocomment'
        
          
        # print(postcomments[0][1].replycomments_set.all())
        # postcomments=commentedpost.usercomments_set.all()
        context={"postdetail":(tupleofpost,userofpost,postuserprofileimg),"postcomments":postcomments}
        return render(request,"letsocial/postcomment.html",context)    

def postcomment(request,id):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        if request.method == "POST":
            commenttext=request.POST['usercommenttext']
            commentedpost=UserPosts.objects.get(id=id)
            commentuser=request.user.username
            print(commenttext,commentedpost,commentuser)
            newcomment=Usercomments(commentonpost=commentedpost,personwhocomment=commentuser,commenttext=commenttext)
            newcomment.save()
        
        return HttpResponseRedirect(reverse(f'letsocial:postcommentpage',args=(commentedpost.id,)))  

def replycomment(request,id,commentid):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        if request.method == "POST":
            replycommenttext=request.POST['replycommenttext']
            commentedpost=UserPosts.objects.get(id=id)
            replycommentuser=request.user.username
            replyoncomment=Usercomments.objects.get(id=commentid)
            
            newreplycomment=Replycomments(replyoncomment=replyoncomment,personwhoreply=replycommentuser,replycommenttext=replycommenttext)
            newreplycomment.save()
            
            print(replycommenttext,commentedpost,replycommentuser,replyoncomment)
            
            
        return HttpResponseRedirect(reverse(f'letsocial:postcommentpage',args=(commentedpost.id,)))  
    
def userfriendslist(request,userid):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        userslistindatabase=User.objects.all()
        userlist=[]
      
        for i in userslistindatabase:
            
                otheruserprofileimgfilter=list(Userprofileimage.objects.filter(profileimgusername=i.username))
                if otheruserprofileimgfilter == []:
                    otheruserprofileimg=None
                else:
                    otheruserprofileimg=Userprofileimage.objects.get(profileimgusername=i.username)
                
                tupleofuserdetail=(i,otheruserprofileimg)
                userlist.append(tupleofuserdetail)
        friendlist=[]
        userfriendlist=[]
        userobject=User.objects.get(id=userid)
        norespondfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='norespond'))]
        sendfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='norespond'))]
        recievefriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='norespond'))]
        acceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=userobject.username,approvestatus='accept'))]
        acceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=userobject.username,approvestatus='accept'))]
        friendlist.extend(acceptedfriendrequestfilter)
        friendlist.extend(acceptfriendrequestfilter)
        
        useracceptfriendrequestfilter=[i.userwhorequest for i in list(Friendrequestbyuser.objects.filter(approvername=request.user.username,approvestatus='accept'))]
        useracceptedfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='accept'))]
        userfriendlist.extend(useracceptedfriendrequestfilter)
        userfriendlist.extend(useracceptfriendrequestfilter)
        
        blockfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='block'))]
        cancelfriendrequestfilter=[i.approvername for i in list(Friendrequestbyuser.objects.filter(userwhorequest=request.user.username,approvestatus='cancel'))]
        
        if sendfriendrequestfilter == []:
            sendfriendrequestfilter=None
            
        if recievefriendrequestfilter == []:
            recievefriendrequestfilter=None
            
        if friendlist == []:
            friendlist=None
        
        context={"userlist":set(userlist),"friendslist":friendlist, "people_who_are_not_friend_of_user":[sendfriendrequestfilter,recievefriendrequestfilter,norespondfriendrequestfilter,userfriendlist]}
        return render(request,'letsocial/userfriendslist.html',context)        

def chatpage(request,username,otherusername):
    if request.user.is_anonymous:
        return redirect('letsocial:loginpage')
    else:
        userobject=User.objects.get(username=username)
        otheruserobject=User.objects.get(username=otherusername)
        usernamelist=[username,otherusername]
        usernamelist.sort()
        
        savedchatsfilter=Savechats.objects.filter(cgroupname=f"chat_{usernamelist[0]}{usernamelist[1]}").order_by("messagetime")
        
        savedchats=[]
        
        chatdates=list(set([(i.messagedate) for i in savedchatsfilter]))
        chatdates.sort()
        # print(chatdates)
        
        for j in chatdates:
            chatbydate=savedchatsfilter.filter(messagedate=j)
            tupleofchats=(j,chatbydate)
            savedchats.append(tupleofchats)
                
        # print(savedchats)
        todaydate=datetime.date.today()
        print(todaydate)
        context={"chatbetween":f'{username}and{otherusername}', 'otherusername':otherusername, 'otheruser':otheruserobject, 'savedchats':savedchats, 'today':todaydate}
        print(username,otherusername)
        return render(request,'letsocial/chatpage.html',context)