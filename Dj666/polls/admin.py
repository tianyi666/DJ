from django.contrib import admin
from django.contrib.admin import AdminSite
from polls.models import User

admin.site.register(User)

class MyAdminSite(AdminSite):
    site_title = 'tianyi666site'

admin_site=MyAdminSite(name='tianyi666')
admin_site.register(User)
