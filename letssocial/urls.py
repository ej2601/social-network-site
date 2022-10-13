from django.contrib import admin
from django.urls import path
from . import views

app_name = 'letsocial'


urlpatterns = [
    path('', views.index, name='index' ), 
    path('updateprofilephoto', views.updateprofilephoto, name='updateprofilephoto' ),
    path('deleteprofileimage', views.deleteprofileimage, name='deleteprofileimage' ),
    path('updateuserdescription', views.updateuserdescription, name='updateuserdescription' ),
    path('uploadimages',views.uploadimages,name='uploadimages'),
    path('deleteimagesfromgallery',views.deleteimagesfromgallery,name='deleteuserimages'),
    path('<int:postid>/deletepost',views.deletepost,name='deletepost'),
    path('makepost', views.makepost, name='makepost' ), 
    path('postcreated', views.postcreated, name='postcreated' ),
    path('usergallery', views.viewgallery, name='usergallery' ),
    path('people', views.people, name='peoplepage' ),
    path('people/searchresult', views.people, name='peoplesearchpage' ),
    path('<int:id>/profileview', views.otherpersonprofileview, name='otherpersonprofileview' ),
    path('<int:id>/post', views.postcommentpage, name='postcommentpage' ),
    path('<int:id>/post/postcomment', views.postcomment, name='postcomment' ),
    path('<int:id>/post/<int:commentid>/replycomment', views.replycomment, name='replycomment' ),
    path('<int:id>/addfriend', views.addfriend, name='addfriend' ),
    path('<str:cancelrequesttouser>/cancelrequest', views.cancelfriendrequest, name='cancelfriendrequest' ),
    path('friends', views.friends, name='friendspage' ),
    path('<int:userid>/userfriendslist', views.userfriendslist, name='userfriendslist' ),
    path('chat/<str:username>and<str:otherusername>', views.chatpage, name='chatpage' ),
    path('friends/<str:username>/acceptrequest', views.acceptrequest, name='acceptrequest' ),
    path('friends/<str:username>/rejectrequest', views.rejectrequest, name='rejectrequest' ),
    path('login', views.loginpage, name='loginpage' ),
    path('register', views.registerpage, name='registerpage' ),
    path('registeruser', views.registeruser, name='registeruser' ),
    path('loginuser', views.loginuser, name='loginuser' ),
    path('profile', views.profilepage, name='profilepage' ),
    path('profile/logout', views.logoutuser, name='logoutuser' ),
    path('profile/personal-info', views.userpersonalinfo, name='personalinfo' ),
    path('profile/personal-info/changepassword', views.changepassword, name='changepassword' ),
    path('profile/personal-info/changeinfo', views.changeotherinfo, name='changeinfo' ),
    path('login/forgot-password/username', views.forgotpassfirststep, name='forgotpassuser' ),
    path('login/forgot-password/otp', views.forgotpasssecondstep, name='forgotpassotp' ),
    path('login/forgot-password/change', views.forgotpassthirdstep, name='forgotpasschange' ),
    path('login/forgot-password/passwordchanged', views.forgotpassfinish, name='forgotpassfinish' ),
    path('profile/delete-account', views.deleteaccount, name='deleteaccount' ),
    path('login/forgot-user', views.forgotuserfirststep, name='forgotuserfirst' ),
    path('login/forgot-user/getusername', views.forgotuserlaststep, name='forgotuserlast' ),
]
