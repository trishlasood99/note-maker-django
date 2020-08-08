#from django.contrib.auth.forms import LoginForm
#from django.forms import ModelForm,Form
from django import forms
from .models import user
class SignUpForm(forms.ModelForm):
    #first_name=forms.CharField(label='First Name',max_length=50)
    #last_name=forms.CharField(label='Last Name',max_length=50)
    #user_name=forms.CharField(label='Enter the user name you would like to use',max_length=15)
    #email_id=forms.EmailField(label='Email ID')
    #SECURITY_QUESTION_CHOICES=[
    #    (1,"What primary school did you attend?"),
    #    (2,"In what town or city did your mother and father meet?"),
    #    (3,"What is your mother's maiden name?"),
    #    (4,"What was your childhood pet's name?"),]
    #security_question=forms.ChoiceField(label='Security Question',choices=SECURITY_QUESTION_CHOICES)
    #security_ans=forms.CharField(label='Answer to security question',max_length=15)
    password = forms.CharField(max_length=15, widget=forms.PasswordInput)
    class Meta:
        model=user
        fields=['first_name','last_name','username','password','email_id','security_question','security_ans']
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

#class UserLoginForm(ModelForm):
#    class Meta:
#        model=user
#        fields=['username','password']
#    def __init__(self, *args, **kwargs):   #has to be defined or an error occurs
#        self.request = kwargs.pop('request', None)
#        super(LoginForm, self).__init__(*args, **kwargs)

class ForgotPasswordForm(forms.Form):
    username=forms.CharField(label='Enter your user name:',max_length=15)
    SECURITY_QUESTION_CHOICES=[
       (1,"What primary school did you attend?"),
       (2,"In what town or city did your mother and father meet?"),
       (3,"What is your mother's maiden name?"),
       (4,"What was your childhood pet's name?"),]
    security_question=forms.ChoiceField(label='Security Question',choices=SECURITY_QUESTION_CHOICES)
    security_ans=forms.CharField(label='Answer to security question',max_length=15)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['first_name','last_name','username','email_id']
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(EditProfileForm,self).__init__(*args,**kwargs)

# class SearchForm(Form):
#     search_query=forms.CharField(max_length=50,initial='Search for users')
