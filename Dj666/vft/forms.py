from  django import  forms
from  django.forms import ModelForm
from  .models import Dog
import gettext
_=gettext.gettext


class UserForm(forms.Form):
    name=forms.CharField(label='姓名', max_length=6,initial='tianyi')
    age=forms.IntegerField(label='年龄')
    chk=forms.ChoiceField(label='选择',choices=[('b', '----'),('a', 'ddd')])
    # chk = forms.ModelChoiceField(label='选择', queryset=..., to_field_name="id")
    msg=forms.CharField(widget=forms.Textarea(attrs={'class':'txa'}), label='信息',required=False)

#验证任何内容
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        age = cleaned_data.get("age")
        pass#不用 return data

    # 验证字段内容
    def clean_age(self):
        data = self.cleaned_data['']
        # self.add_error('age', 'xxxxxx')
        return data


class DogForm(ModelForm):
    # name=forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Dog
        fields = '__all__' #表示表单包含所有字段
        # exclude = ['headimg']#标识可以表单中不包含的字段

        # 重新定义表单信息
        labels = {
            'name': _('名字'),
        }

        # error_messages={}

# dog = dogform.save(commit=False) 保存但不提交
# dog.title = 'Mr'
# dog.save() 保存并提交
# dog_m2m.save_m2m()
