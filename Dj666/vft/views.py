from django.shortcuts import render,HttpResponse,redirect
from django import forms

import gettext
_ = gettext.gettext

from .models import Dog
from django.forms import ValidationError
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.http.response import Http404



def index(request):
    #模版最原始的内部方法
    # t = loader.get_template('my_template_name.txt')
    # c = Context({
    #     'data': csv_data,
    # })
    # response.write(t.render(c))

    # return HttpResponse('<h1>Hello World!</h1>')
    ctx=[1,2,3,4]
    return render(request,"vft/cycle.html",{"ctx":ctx})


class DogForm(forms.Form):
    name=forms.CharField()
    headimg=forms.ImageField()


def register(request):
    if request.method=='POST':
        df=DogForm(request.POST,request.FILES)
        if df.is_valid():
            dog=Dog(name=df.cleaned_data['name'],headimg=df.cleaned_data['headimg'])
            dog.save()
            return HttpResponse('<h1>OK!</h1>')
    else:
        dog=Dog.objects.first()
        dog.name='贵宾'
        dog.headimg='bo.gif'#关键点
        df=DogForm()
    return render(request,'vft/FileUpd.html',{"df":df,"dog":dog})

class DogListView(ListView):
    model = Dog
    #head请求 询问是否有更新
    def head(self, *args, **kwargs):
        last_dog = self.get_queryset().latest('publication_date')
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_dog.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

class DogLsView(ListView):
    # 默认模版位置为  <app>/<model>_list.html
    template_name = 'vft/dog_list.html'

    # 常用写法
    model = Dog

    # #等价写法
    # queryset = Dog.objects.all()

    # #可以自己定义任意数据，改变默认行为
    # queryset = Dog.objects.order_by('-id')

    #如果需要获取请求参数等方面的信息 重写get_queryset
    # page_kwarg = 'page'   url中 页码匹配的参数名称
    # def get_queryset(self):
        # self.kwargs  self.args  可以获取 url参数信息
        # self.request 可以获取各种请求信息

    # context_object_name = 'mydog_list'
    def get_context_data(self, **kwargs):
        #写法一
        # kwargs['exdata']='I\'m exdata'
        # return super(DogLsView,self).get_context_data(**kwargs)

        # 写法一
        ctx = super(DogLsView, self).get_context_data(**kwargs)
        ctx['exdata']='I\'m exdata'
        return ctx

class DogDetailView(DetailView):
    model = Dog

    # pk_url_kwarg = 'sid' # url 用来匹配主键的 参数名称 默认是pk
    def get_object(self, queryset=None):
        object = super(DogDetailView,self).get_object()
        #处理数据
        # object.last_accessed = timezone.now()
        # object.save()
        return  object

class DogCreateView(CreateView):
    model = Dog
    fields = ['name','headimg']
    # success_url = reverse_lazy('vft:dogdetails',kwargs={'pk':self.pk}) 如果 Model中没有定义get_absolute_url 那么必须设置该字段

class DogUpdateView(UpdateView):
    model = Dog
    fields = ['name','headimg']

class DogMixView(SingleObjectMixin,ListView):
    pk_url_kwarg = 'id' #针对SingleObjectMixin
    # page_kwarg = 'p'#针对ListView
    context_object_name = 'obj'
    template_name = 'vft/dog_mix.html'
    # object=Dog.objects.first()

    #get 针对的是view 表示处理get请求的方法
    def get(self, request, *args, **kwargs):
        #get_object 来源于SingleObjectMixin 写在get方法中 可以获取pk等参数
        self.object=self.get_object(queryset=Dog.objects.all())
        return super(DogMixView,self).get(self, request, *args, **kwargs)

    # def get_object(self, queryset=None):
    #     return Dog.objects.first()
    #针对ListView
    def get_queryset(self):
        return Dog.objects.all()

    def get_context_data(self, **kwargs):

        kwargs['list']=self.object_list
        #get_queryset 获取的值即object_list
        #get方法self.object 赋值 获取的值为 object
        return super(DogMixView,self).get_context_data(**kwargs)


##############################-----------------------------------############

from  .forms import UserForm

def reg(request):
    if request.method=='GET':
        # data={'name':'abcabcabc','age':1}#,'msg':'happy'}
        # form = UserForm(data,auto_id=False) #auto_id='id_%s'

        form=UserForm(initial= {'name':'tianyi666','chk':'a', 'age':16},prefix='uf')

        # form=UserForm()

        return render(request,'vft/reg.html',{'form':form})
    else:
        form=UserForm(request.POST)

        if form.has_changed():
            return HttpResponse('<h1>表单变动了</h1>')

        if form.is_valid():
            return redirect('../')
        else:
            # raise Http404('数据验证失败！')
            form.add_error(None,'错了是错了，对了也是错了！')
            form.add_error('msg',ValidationError(_('错就是错，字段为 %(value)s'),code='768',params={'value':66}))
            e=form.errors.as_data()
            return render(request, 'vft/reg.html', {'form': form,'e':e})


def dogform(request):
    from  .forms import DogForm
    from  django.forms.models import modelform_factory
    from django.forms import Textarea


    # dog=Dog.objects.first()
    # form=DogForm(instance=dog)
    form=modelform_factory(Dog,exclude=('',),widgets={'name':Textarea})

    return render(request,'vft/dog_form.html',{'form':form})

from django.forms.formsets import BaseFormSet
class BaseUserFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(BaseUserFormSet, self).add_fields(form, index)
        form.fields["my_field"] = forms.CharField()



def formset(request):
    from django.forms.formsets import formset_factory

    UserFormSet = formset_factory(UserForm,BaseUserFormSet)

    # UserFormSet = formset_factory(UserForm, extra=2,can_delete=True)  # extra 只除了初始数据额外显示的条目
    if request.method=='GET':

        formset=UserFormSet(initial=[{'name':'tianyi1','age':11},{'name':'tianyi2','age':22}],prefix='pre666')
        # formset = UserFormSet(prefix='pre666')
        print(formset.empty_form.prefix)
        return  render(request,'vft/commform.html',{'formset':formset})
    else:
        data = {
        'form-TOTAL_FORMS': '2',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '1000',
        }
        formset= UserFormSet(data)
        if formset.has_changed():
            return HttpResponse("改变了")
        else:
            return HttpResponse("没有改变")





