from django import forms

class RegisterForm(forms.Form):
    user_name = forms.CharField(label="Username", max_length=32)
    user_email = forms.EmailField(label="Email")
    user_password = forms.CharField(widget=forms.PasswordInput, label="Password")
    user_password_repeat = forms.CharField(widget=forms.PasswordInput, label="Repeat password")

class LoginForm(forms.Form):
    user_name = forms.CharField(label="Username", max_length=32)
    user_email = forms.EmailField(label="Email")
    user_password = forms.CharField(widget=forms.PasswordInput, label="Password")