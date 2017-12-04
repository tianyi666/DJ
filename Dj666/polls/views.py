from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404,redirect
from django.http import  HttpResponseNotFound,JsonResponse,FileResponse
from polls.models import User,Car,Maker
from django.core.urlresolvers import  reverse
from django.views import generic
from datetime import datetime
from django.views.decorators.http import last_modified


def error(request):
    return render(request,'404.html')


def last_upd(request,id):
    return datetime.strptime('2017-01-01 01:01:01',"%Y-%m-%d %H:%M:%S")

##缓存控制
@last_modified(last_upd)
def getcar(request,id):
    car = Car.objects.first()
    return render(request, 'polls/car.html', {'car': car})


def index(request):
    # raise Http404('<h1>Page not found</h1>')
    # return HttpResponseNotFound('<h1>Page not found</h1>')

    # return HttpResponse('Hello World!')
    #返回Json对象
    # return JsonResponse({'foo':'bar'})
    # 返回文件流
    return FileResponse(open('d:/bo.gif','rb'), content_type='image/jpeg')
##重定向
    # return redirect('../polls/details/1')
    # return redirect('details/1')
    # return redirect('/')

    # return redirect('polls:details',args={1})
    # return redirect('polls:details', id=1)

    # return HttpResponseRedirect(reverse('polls:ls'))
    # return HttpResponseRedirect(reverse('polls:details',args={1}))

def newuser(request):
    user=User(name='tianyi',age=32)
    user.save()
    return render(request,'polls/hello.html',{'dt':user})

class IndexView(generic.ListView):
    template_name = 'polls/list.html'
    context_object_name = 'ls'
    model = User
    # def get_queryset(self):
    #     return User.objects.order_by('-id')[:5]
    def get_context_data(self, **kwargs):
        kwargs['exdata']='Hello Exdata!'
        return super(IndexView,self).get_context_data(**kwargs)


class DetailView(generic.DetailView):
    model = User
    template_name = 'polls/details.html'
    pk_url_kwarg = 'id'
    # pk_url_kwarg = 'pd'

    # def get_object(self, queryset=None):
    #     # return User(id=66,name='dir_data',age=666)
    #     query=self.get_queryset()
    #     # pki=int(self.kwargs.get('id',None))
    #     pki=int(self.kwargs.get(self.pk_url_kwarg,2))
    #     print(self.kwargs)  #{'id': '3', 'pd': '1'}
    #     # print(self.args)  (3,1)
    #     # # pki = int(self.kwargs['pd'])
    #     return query[pki]

def createcar(request):
    car=Car(name='速腾',maker_id=1)
    car.save()
    print(car.maker.car_set.all())
    car=Car.objects.first()
    return render(request,'polls/car.html',{'car':car})
