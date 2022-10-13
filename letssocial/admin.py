from django.contrib import admin
from .models import Replycomments, Usercomments, Useruploadedimage,UserPosts,Userprofileimage,Userdescriptiondetails,Friendrequestbyuser, Savechats

# Register your models here.
admin.site.register(Useruploadedimage)
admin.site.register(UserPosts)
admin.site.register(Userprofileimage)
admin.site.register(Userdescriptiondetails)
admin.site.register(Friendrequestbyuser)
admin.site.register(Usercomments)
admin.site.register(Replycomments)
admin.site.register(Savechats)