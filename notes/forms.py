from django.forms import ModelForm,ModelMultipleChoiceField,CheckboxSelectMultiple
from .models import Note, SharedNote
from followers.models import Follower
from users.models import user

class CreateNoteForm(ModelForm):
    class Meta:
        model=Note
        fields=['contents','title','favourite']
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(CreateNoteForm,self).__init__(*args,**kwargs)
    def save(self,commit=True):
        obj = super(CreateNoteForm, self).save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        #return obj
class EditNoteForm(ModelForm):
    class Meta:
        model=Note
        fields=['contents','title','favourite']

class CreateSharedNoteForm(ModelForm):
    users=ModelMultipleChoiceField(queryset=user.objects.all(),required=False,widget=CheckboxSelectMultiple)
    #users=ModelMultipleChoiceField(queryset=user.objects.all(),required=False,widget=CheckboxSelectMultiple)
    class Meta:
        model=SharedNote
        fields=['users','contents','title']
    def __init__(self,*args,**kwargs):
        self.created_by=kwargs.pop('user',None)
        super(CreateSharedNoteForm, self).__init__(*args, **kwargs)
        if Follower.objects.filter(current_user=self.created_by).exists():
        #if follower_obj is not None:
            follower_obj=Follower.objects.filter(current_user=self.created_by).first()
            self.fields['users'].queryset=follower_obj.followers.all()
            #self.fields['users']=ModelMultipleChoiceField(queryset=follower_obj.objects.all(),required=False,widget=CheckboxSelectMultiple)
        else:
            #self.fields['users']=ModelMultipleChoiceField(queryset=None,required=False,widget=CheckboxSelectMultiple)
            self.fields['users'].queryset=None
        #super(CreateSharedNoteForm,self).__init__(*args,**kwargs)
    def save(self,commit=True):
        obj = super(CreateSharedNoteForm,self).save(commit=False)
        obj.created_by=self.created_by
        if commit:
            obj.save()

class EditSharedNoteForm(ModelForm):
    class Meta:
        model=SharedNote
        fields=['contents','title']
