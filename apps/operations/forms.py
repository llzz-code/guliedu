from django import forms
import re
from .models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'phone', 'course']

        # 除了add_time字段
        # exclude = ['add_time']
        # # 如果用所有字段
        # fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        com = re.compile(r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$')
        if com.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号码不合法')


class UserCommentForm(forms.Form):
    comment_course = forms.IntegerField(required=True)
    comment_content = forms.CharField(required=True, min_length=1, max_length=300)
