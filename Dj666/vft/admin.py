from django.contrib import admin
from .models import Dog,Panda
from django import  forms
from django.forms import  widgets
from django.db import models
from django.utils.html import format_html
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
    readonly_fields = ('age',) #添加和编辑都不可用
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
    search_fields = ('name',)

    #201712042250







