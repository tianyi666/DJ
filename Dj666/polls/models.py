from django.db import models
from django.db.models import Count
from django.db.models import F
from collections import OrderedDict
class Maker(models.Model):
    FNAME=(
        ('大众','vv'),
        ('丰田', 'toyota'),
    )
    name=models.CharField(max_length=20,choices=FNAME)


class Car(models.Model):
    name=models.CharField(max_length=20)
    # maker = models.ForeignKey(Maker)
    maker=models.ForeignKey(Maker,related_name='mk' ,on_delete=models.SET_NULL,null=True)
    ##related_name（反向名称） 用于反向查询 名字用于替换 xxx_set
    ## on_delete 默认为CASCADE 级联删除，还有SET_NULL、SET_DEFAULT 可选


# Maker.objects.filter(car__id__gt=4)[1].name
# Car.objects.filter(maker_id=1).count() #模型中定义的外键字段是单下划线
# Car.objects.filter(maker__name='丰田').count()#反查的是双下划线
# Car.objects.filter(maker__name__contains='大').count()#不区分大小写查询   前面+i  icontains
# Car.objects.filter(maker__name__startswith='丰').count()
# Car.objects.filter(maker__name__in=['丰田','大众']).count()
# Car.objects.exclude(maker_id=1).count()
# Car.objects.exclude(maker__name__contains='大').count()
# Maker.objects.first().car_set.count()

##自关联  此时没有xx_set
class Person(models.Model):
    name = models.CharField(max_length=20)
    friends = models.ManyToManyField("self")

##p1=Person(name='p1')
## p1.save()
## p2=Person(name='p2')
## p2.save()
## p3=Person(name='p3')
## p3.save()
## p1.friends.add(p2,p3)

## 一对一关联
class Stu(models.Model):
    name = models.CharField(max_length=20)

class StuInfo(models.Model):
    code = models.OneToOneField(Stu,primary_key=True)
    age=models.IntegerField()

##s=Stu(name='Jim') ; s.save()
##si=StuInfo(code=s,age=32) ; si.save()
##s.stuinfo.age
##si.stu.name

##多对多
class Sub(models.Model):
    name = models.CharField(max_length=20)

class Teach(models.Model):
    name = models.CharField(max_length=20)
    members=models.ManyToManyField(Sub)

# s=Sub(name='语文') ; s.save()
# t=Teach(name='Tom');t.members.add(s) 多对多中必须先保存实体最后增加关系
# m=s.teach__set.create(name='张老师')  返回关系对象
# s.teach__set=[t1,t2,t3]  返回关系对象

##多对对附加关系类
class Sub1(models.Model):
    name = models.CharField(max_length=20)

class Teach1(models.Model):
    name = models.CharField(max_length=20)
    members=models.ManyToManyField(Sub1,through='Membership')

class Membership(models.Model):
    sub1=models.ForeignKey(Sub1)
    teach1 = models.ForeignKey(Teach1)
    mdesc = models.CharField(max_length=20)

## s=Sub1(name='物理') ; s.save() ; t=Teach1(name='韩老师') ; t.save()
## Membership.objects.create(sub1=s,teach1=t,mdesc='初中物理老师')
## t.membership_set.first().mdesc 或者 s.membership_set.first().mdesc
## 所有类型都有membership_set属性 只有通过这个属性才能获取到关系中的字段
## Sub1.objects.filter(membership__teach1__name='韩老师') 两个对象关系对等 访问方式一样

## isnull各种为空的情况 Blog.objects.filter(entry__authors__isnull=False,entry__authors__name__isnull=True)
##两个filter 并且 或者   对于无关联的模型 是并且  但是对于关联模型 是 或者（想并且的话写到一个filter里面）
##Blog.objects.filter(entry__headline__contains='Lennon',entry__pub_date__year=2008) # 并且
##Blog.objects.filter(entry__headline__contains='Lennon').filter(entry__pub_date__year=2008) #注意 这里是或者

##from django.db.models import F
##Entry.objects.filter(col1__gt=F('col2')+F('col3')) F表达式 一个字段与同一个模型的另外一个字段进行比较
##Entry.objects.filter(col1__gt=F('blog__col6') F表达式 可以跨模型

class Cat(models.Model):
    age=models.IntegerField()
    height=models.IntegerField()
##Cat.objects.filter(age=F('height')*2)

##Q对象
##Q 一定要在普通条件之前，     Q可以用|表示OR      逗号隔开的Q对象 相当于 AND  ~Q表示非
##News.objects.get(Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),question__startswith='Who')



##拷贝模型实例
##c=Cat(age=1,height=2) ; c.save()
##c.pk=None ;c.save()
##如果使用了继承 需要同时设置 pk 和 id  c.pk=None c.id=None

##延迟加载字段  生成的sql语句不包括该字段， 但是代码中可以访问该字段对应的属性  only 反之

##c=Cat.objects.defer('age')
##c=Cat.objects.only('age')


##改变sql语句
#c=Cat.objects.extra(select={'isbig':'age > 5'});
#Cat.objects.extra(select=OrderedDict([('mycol','%s')]),select_params=(5,)) 注意最后的逗号 一定要有不然会报错
#extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
#extra(order_by = ['-is_recent'])
#Cat.objects.extra(select=OrderedDict([('mycol','%s')]),select_params=(5,) ,where=['mycol= %s','age = 10 '],params=[5,])


##批量创建 bulk_create
##Cat.objects.bulk_create([Cat(age=1,height=1),Cat(age=2,height=2),Cat(age=3,height=3),])
##以id为字典返回对象
##Cat.objects.in_bulk([3,4,5])   #返回一个字典对象 key 分别为 3 4 5  对应的值为 id为 3 4 5的对象
## 聚合函数
##Cat.objects.aggregate(Count('age'));Cat.objects.aggregate(Sum('age'))

##只更新某个字段
##cat.save(update_fields=['age'])

## Entry.objects.update(blog__name='foo') 无效  update 只能更新主表 不能更新关联表


class ProxyCat(Cat):
    class Meta:
        proxy = True

class SonCat(Cat):
    pass

# Cat(id=1)==ProxyCat(id=1)  True
# Cat(id=1)==SonCat(id=1)    False

## 减少查询数据库  select_related 对于一对一，外键     prefetch_related 对 多对多 多对一 的关联查询起作用，
## 如果不用这个属性 则每次取关联类的值都会查询数据库
##位置无关  ## 取消 传none参数  qs.prefetch_related(None)
##.select_related('model1', 'model2')

#to_attr 定义新属性   queryset定义属性来源
##q = Pizza.objects.filter(vegetarian=True)
##Restaurant.objects.prefetch_related(
##        Prefetch('pizzas', to_attr='colname1'),
##        Prefetch('pizzas', queryset=q, to_attr='colname2'))



##检测是否存在
##filter(pk=1).exists():
## Cat.objects.exists()





##直接SQL
##name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
##Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)
##first_person = Person.objects.raw('SELECT * FROM myapp_person')[0] 可以用索引

##抛开模型执行SQL
##from django.db import connection
##cursor = connection.cursor()
##cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", ['baz1'])
##cursor.fetchall()  cursor.fetchone()

##或者用下面的写法 等价于 try finally
##with connection.cursor() as c:
##  c.execute(...)

class User(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()

    def __str__(self):
        return self.name
    class Meta:
        ordering=['-id']
        db_table='puser'



