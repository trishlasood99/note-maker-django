from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,UpdateView,ListView,DetailView, DeleteView
from .forms import SignUpForm,EditProfileForm,ForgotPasswordForm
from django.urls import reverse
from django.contrib.auth.views import LoginView,PasswordChangeView, PasswordChangeDoneView
from .models import user
from notes.models import Note, SharedNote
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from followers.models import FollowRequest,Follower
from django.contrib.auth.forms import PasswordResetForm
#from django.template import RequestContext
# Create your views here.
def signup_view(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            new_user.save()
            return HttpResponseRedirect(reverse("signup-success"))
    else:
        form=SignUpForm()
    return render(request,'signuppage.html',{'form':form,'user':request.user})

class SignUpSuccessView(TemplateView):
    template_name="signup_success.html"


class UserLoginView(LoginView):
    template_name="login.html"
    #authentication_form=UserLoginForm

def ForgotPasswordView(request):
    if request.method=="POST":
        form=ForgotPasswordForm(request.POST)
        if form.is_valid():
            query=Q(username__exact=form.cleaned_data['username'])
            old_user=user.objects.filter(query).first()
            if old_user is None:
                return HttpResponseRedirect(reverse("wrong_ans"))
            if old_user.security_question==form.fields['security_question'] and old_user.security_ans==form.fields['security_ans']:
                return HttpResponseRedirect(reverse("reset_password"))
            else:
                return HttpResponseRedirect(reverse("wrong_ans"))
    else:
        form=ForgotPasswordForm()
    return render(request,'forgot_password.html',{'form':form})

class PasswordResetView(PasswordChangeView):
    template_name="password_change.html"
    form_class=PasswordResetForm
    def get_success_url(self):
        return reverse("home")

class WrongAnswerView(TemplateView):
    template_name='wrong_answer.html'

class PasswordChangeSuccessView(PasswordChangeDoneView):
    template_name='password_change_success.html'

class EditProfileView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    template_name="edit_profile.html"
    form_class=EditProfileForm
    def test_func(self):
        if(self.request.user.pk==self.kwargs['pk']):
            return True
        else:
            return False
    def get_success_url(self):
        return reverse("edit-profile",kwargs={'pk':self.request.user.pk})
    def get_queryset(self):
        return user.objects.filter(username=self.request.user.username)

class DashboardView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    template_name="dashboard.html"
    paginate_by=10
    def test_func(self):
        if(self.request.user.pk==self.kwargs['pk']):
            return True
        else:
            return False
    def get_queryset(self):
        query_set=Note.objects.filter(user=self.request.user).order_by('-favourite','-last_modified')
        #list1=query_set.filter(favourite=True)
        #list2=query_set.filter(favourite=False)
        return query_set
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        cquery=Q(created_by=self.request.user)
        context['shared_notes']=list(SharedNote.objects.filter(cquery))
        for x in SharedNote.objects.all():
            if self.request.user in x.users.all():
                context['shared_notes'].append(x)
        return context

class ProfileDetailView(LoginRequiredMixin,DetailView):
    template_name="profile_detail.html"
    #model=user
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        viewed_user=user.objects.get(pk=self.kwargs['pk'])
        context['pk']=self.kwargs['pk']
        context['following']=0
        if(viewed_user.pk==self.request.user.pk):
            context['following']=100
            return context
        follower_obj=Follower.objects.filter(current_user=viewed_user).first() #if get was used exception would occur if viewed_user is not present in Follower
        if(follower_obj is not None):
            follower_list=follower_obj.followers.all()
            if self.request.user in follower_list:
                context['following']=1
                return context
        follow_requests_list=FollowRequest.objects.filter(from_user=viewed_user)
        for obj in follow_requests_list:
            if(obj.to_user==self.request.user):
                context['following']=2
                return context
        follow_requests_list=FollowRequest.objects.filter(from_user=self.request.user)
        for obj in follow_requests_list:
            if(obj.to_user==viewed_user):
                context['following']=3
                return context
        return context
    def get_object(self):
        return get_object_or_404(user,pk=self.kwargs['pk'])
# @login_required
# def search_user_view(request):
#     if request.method=="GET":
#         form=SearchForm(request.GET)
#         if form.is_valid():
#             return HttpResponseRedirect(reverse("search",kwargs={'query':form.search_query}))
#     else:
#         form=SearchForm()
#     return render(request,'search_results.html')

class SearchView(LoginRequiredMixin,ListView):
    template_name="search_results.html"
    def get_queryset(self):
        search_words=self.request.GET.get('search')
        if(search_words):
            query=Q(first_name__icontains=search_words)|Q(last_name__icontains=search_words)|Q(username__icontains=search_words)
            query_set=user.objects.filter(query)
        else:
            query_set=None
        return query_set
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['search_words']=self.request.GET.get('search')
        return context

@login_required
def AddFollower(request,pk):
    owner=request.user
    new_follower=user.objects.get(pk=pk)
    Follower.makeFollower(owner,new_follower)
    Follower.makeFollower(new_follower,owner)
    query=Q(from_user_pk=pk) & Q(to_user=request.user)
    FollowRequest.objects.filter(query).delete()
    return HttpResponseRedirect(reverse('dashboard',kwargs={'pk':request.user.pk}))

@login_required
def RemoveFollower(request,pk):
    owner=request.user
    new_follower=user.objects.get(pk=pk)
    Follower.deleteFollower(owner,new_follower)
    Follower.deleteFollower(new_follower,owner)
    return HttpResponseRedirect(reverse('dashboard',kwargs={'pk':request.user.pk}))

@login_required
def DeleteRequest(request,pk): #url should contain pk of follow request
    FollowRequest.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('dashboard',kwargs={'pk':request.user.pk}))

@login_required
def CreateRequest(request,pk):
    from_user=request.user
    from_user_pk=request.user.pk
    to_user=user.objects.get(pk=pk)
    new_request=FollowRequest.create(to_user,from_user,from_user_pk)
    new_request.save()
    return HttpResponseRedirect(reverse('dashboard',kwargs={'pk':request.user.pk}))
    #define function - pk of to_user

class NotificationsView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    template_name="notifications.html"
    def test_func(self):
        if(self.request.user.pk==self.kwargs['pk']):
            return True
        else:
            return False

    def get_queryset(self):
        return FollowRequest.objects.filter(to_user=self.request.user)

class DeactivateAccountView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=user
    template_name="user_confirm_delete.html"
    def test_func(self):
        if(self.request.user.pk==self.kwargs['pk']):
            return True
        else:
            return False
    def get_object(self):
        return get_object_or_404(user,pk=self.request.user.pk)
    def get_success_url(self):
        return reverse("home")
