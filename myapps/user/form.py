from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="账号", max_length=20,
            widget=forms.TextInput(attrs={'size':30})
        )
    password = forms.CharField(label="密码", max_length=20,
            widget=forms.PasswordInput(attrs={'size':30})
        )

class RegisterForm(LoginForm):
    email = forms.CharField(label="Email", max_length=30,
            widget=forms.TextInput(attrs={'size':30})
        )
    phone = forms.CharField(label="手机号码", max_length=20,
            widget=forms.TextInput(attrs={'size':30})
        )