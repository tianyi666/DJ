from django.contrib import admin
from .models import Dog,Panda,School,Student,Sub,Teach
from django import  forms
from django.forms import  widgets
from django.db import models
from django.utils.html import format_html
from django.shortcuts import HttpResponse
import gettext
_=gettext.gettext

# admin.site.register(Dog); #最简单的注册


# admin.site.register(Dog,DogAdmin) #加入自定义
# class DogAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Dog)       #第三种写法
# class DogAdmin(admin.ModelAdmin):
#     fields = ('name',)  #选择显示的列
#     # exclude = ('name',)
#     actions_on_top = True
#     actions_on_bottom = True
#     actions_selection_counter = True

# @admin.register(Dog)
# class FlatPageAdmin(admin.ModelAdmin):
#     fields = (('name','headimg'), ) #要在同一行显示的 用括号括起来

##————————————————————————————————————————————————————————————————————————————————

class PandaForm(forms.ModelForm):
    class Meta:
        model=Panda
        fields='__all__'
        labels = {
            'name': _('名称'),
        }




class PandaListFilter(admin.SimpleListFilter):
    title = '熊猫名字'
    parameter_name = 'qname'
    # template = 'mytemplate.html'

    def lookups(self, request, model_admin):
        # qs = model_admin.get_queryset(request) 获取查询集
        return (('pp','盼盼'),('npp', '不盼盼'),)

    def queryset(self, request, queryset):
        # if request.user.is_superuser 获取request信息
        if self.value()=='pp':
            return queryset.filter(name='盼盼')
        if self.value()=='npp':
            return queryset.exclude(name='盼盼')





def funprename(obj):
    return 'pre' + obj.name
funprename.short_description = 'fun别名'

@admin.register(Panda)
class PandaAdmin(admin.ModelAdmin):

    #定义自己的Form两种方式
    # form = PandaForm

    # def get_form(self, request, obj=None, **kwargs):
    #     # if condition
    #     kwargs['form']=PandaForm
    #     return super(PandaAdmin,self).get_form(request, obj, **kwargs)



# 覆盖字段类型显示（全部类型），也可以在表单类中改（单个字段）
#     formfield_overrides = {
#         models.CharField: {'widget': widgets.Textarea, 'max_length':3},
#     }
#     fields = (('name', 'age'),)  # 要在同一行显示的 用括号括起来


    #在增加修改页面中显示的内字段
    fieldsets = (
        (None,{'fields':(('name','age'),)}),
        ('高级选项',{
            'fields':('sex','desc','country'),
            'classes': ('wide',),  #:('collapse',), #wede 缩进
            'description':'<h1>说明介绍</h1>'
        }),
    )
    # readonly_fields = ('age',) #添加和编辑都不可用
    #在列表页面中显示的字段
    # list_display=('id','name','age') #方式一

    def formprename(self, obj):
        return 'pre' + obj.name
        formprename.short_description = '别名'

    def htmlcol(self,obj):
        return format_html('<span style="color: #F00;">{}</span>',obj.name)
    htmlcol.allow_tags=False
    htmlcol.short_description = 'html列'
    # htmlcol.boolean = True

    def funsex(self,obj):
        return obj.sex==1
    funsex.short_description = 'funsex'
    funsex.boolean = True

    ordering = ['-age']
    list_display = ('__str__','formprename','modelprename',funprename,'htmlcol','funsex','age','sex') #方式二、三、四
    list_display_links = ('__str__','formprename')    #None #添加链接

    list_editable = ('age',)

    # list_filter = (('sex',admin.AllValuesFieldListFilter),) #可以设置关联查找,但必须是Model属性， e.g: company__name
    # list_filter = (('sex',admin.ChoicesFieldListFilter),)
    list_filter = (('sex', admin.ChoicesFieldListFilter),
                   (PandaListFilter), #自定义筛选选项
                   )
    # list_per_page = 1 #每页显示的结果条数
    list_max_show_all=3 #显示全部按钮  只有条目放得开的情况下才会有效 999肯定有效
    list_select_related = True #减少数据库查询 如果设置为True则始终调用 False则需要时调用
    # list_select_related=('Bear','Cat') #更细粒度的控制

    preserve_filters=False  #保存之后 是否保留过滤器
    radio_fields = {'sex':admin.HORIZONTAL} #编辑页面使用单选按钮
    # raw_id_fields = ('fk') # 外键 或者 多对多的时候 数值列表
    search_fields = ('name',) #'^name'

    # 自定义查询集合
    # model/?q=all|b=1  get 查询 记住链接格式即可
    def get_search_results(self, request, queryset, search_term):
        # print(search_term)
        # print(self.get_urls() )
        if 'b=1'in search_term:
            return self.model.objects.all() , True
        else:
            queryset , use_distinct=super(PandaAdmin,self).get_search_results( request, queryset, search_term)
            return queryset , use_distinct

    # 添加模块需要的urls  /admin/myapp/mymodel/my_view/url/
    def get_urls(self):
        from django.conf.urls import url
        from django.views.generic import RedirectView
        urls=super(PandaAdmin,self).get_urls()
        new_urls=[
            url(r'^bd/bd', RedirectView.as_view(url='http://127.0.0.1:8000/')),
            url(r'^bd/dir', self.my_view),
            url(r'bd/admindir',self.admin_site.admin_view(self.my_view,cacheable=True))
        ]
        return urls+new_urls

    def my_view(self,request):
        return HttpResponse('模版自定义页面')

    # 重新定义外键数据源   formfield_for_choice_field：kwargs['choices']
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "status":
    #         kwargs["queryset"] = Dog.objects.filter(name='盼盼')
    #     return super(PandaAdmin,self).formfield_for_foreignkey(db_field, request, **kwargs)
    #

    # 返回更改页面form类，本例默认为PandaForm
    def get_changelist_form(self, request, **kwargs):
        # print(super(PandaAdmin,self).get_changelist_form(request, **kwargs))
        return super(PandaAdmin,self).get_changelist_form(request, **kwargs)


    def response_add(self, request, obj, post_url_continue=None):
        from django.shortcuts import redirect
        return redirect('https://www.baidu.com/')

    def save_model(self, request, obj, form, change):
        # print(form.cleaned_data['name'])
        print(obj.age)
        obj.save()


    def get_changeform_initial_data(self, request):
        return {'name':'默认姓名'}

    def add_view(self, request, form_url='', extra_context=None):
        extra_context=extra_context or {}
        extra_context['exdata']='exdata'
        # form_url='/bd' #form action
        # print(form_url,extra_context)
        return super(PandaAdmin,self).add_view(request, form_url, extra_context)

    def upd_action(self,request,queryset):

        # rows_updated=queryset.update(age=6)
        # message_bit = "%s 调数据更新成功" % rows_updated
        # self.message_user(request,message_bit)

        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(queryset.model)
        print(ct.pk)
        return HttpResponse('<h1>%s</h1>' % ','.join(selected))


    upd_action.short_description ='更新年龄'
    # actions=None #删除所有action
    actions = ['upd_action',]
    # 全局添加action
    # admin.site.add_action(upd_action, 'action_name')


#-----------------------------------------------------

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1
    max_num = 5
    #多个外键的时候需要指定
    # fk_name = 'school'

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    inlines = [StudentInline,]

class MembershipInline(admin.TabularInline):
    model = Teach.members.through

@admin.register(Sub)
class SubAdmin(admin.ModelAdmin):
    inlines = [MembershipInline,]

@admin.register(Teach)
class TeachAdmin(admin.ModelAdmin):
    inlines = [MembershipInline,]
    exclude = ('members',) #这个是重点
    list_display = ('name','mycol',)

    #多对多的列无法显示，只能通过自定义函数实现，外键的可以通过 _ _ 查询到
    def mycol(self,obj):
        return obj.members.first().name
    mycol.short_description = '学科'





