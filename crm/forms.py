import hashlib

from django import forms
from crm import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class BSForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields.values():
            if not isinstance(filed, forms.BooleanField):
                filed.widget.attrs.update({'class': "form-control"})

class RegForm(BSForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='密码')
    re_pwd = forms.CharField(widget=forms.PasswordInput, label='确认密码')

    class Meta:
        model = models.UserProfile
        fields = '__all__'  # ['username','password']
        exclude = ['memo', 'is_active']
        labels = {
            'username': '用户名'
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'class': "form-control", 'k1': 'v1'}),
        }
        error_messages = {
            'password': {
                'required': '必填的'
            }
        }

    def clean(self):
        pwd = self.cleaned_data.get('password', '')
        re_pwd = self.cleaned_data.get('re_pwd', '')
        if pwd == re_pwd:
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            pwd = md5.hexdigest()
            self.cleaned_data['password'] = pwd
            return self.cleaned_data
        self.add_error('re_pwd', '两次密码不一致')

        raise ValidationError('两次密码不一直')

class CustomerForm(BSForm):

    class Meta:
        model = models.Customer
        fileds = "__all__"
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].widget.attrs.pop('class')


class ConsultForm(BSForm):

    class Meta:
        model = models.ConsultRecord
        fileds = "__all__"
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # print(list(self.fields['customer'].choices))
        # print(self.fields['customer'].choices)
        # self.fields['customer'].choices =

        # print(self.instance)  # obj = models.ConsultRecord(consultant=request.uer_obj)
        # print(self.instance.consultant.customers.all())
        customer_chioices = [(customer.pk, str(customer)) for customer in self.instance.consultant.customers.all()]
        customer_chioices.insert(0, ('', '----------'))
        self.fields['customer'].choices = customer_chioices

        self.fields['consultant'].choices = [(self.instance.consultant.pk, self.instance.consultant), ]


class EnrollmentForm(BSForm):

    class Meta:
        model = models.Enrollment
        fields = '__all__'
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['customer'].choices = [(self.instance.customer.pk, self.instance.customer)]

        self.fields['enrolment_class'].choices = [(i.pk, str(i)) for i in self.instance.customer.class_list.all()]

