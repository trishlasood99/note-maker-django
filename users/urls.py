from django.urls import path
from .views import DeactivateAccountView,signup_view,EditProfileView,SignUpSuccessView,UserLoginView,DashboardView,ProfileDetailView,SearchView,AddFollower,RemoveFollower,DeleteRequest,NotificationsView,CreateRequest,PasswordResetView,ForgotPasswordView,PasswordChangeSuccessView,WrongAnswerView
from django.contrib.auth.views import LogoutView
from notes.views import NoteCreateView,NoteEditView,SharedNoteCreateView, SharedNoteEditView, SharedNoteDeleteView, NoteDeleteView, generate_pdf, generate_shared_pdf

urlpatterns =[
    path('sign_up',signup_view,name='signup'),
    path('register_success',SignUpSuccessView.as_view(),name='signup-success'),
    path('login',UserLoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('edit-profile/<int:pk>',EditProfileView.as_view(),name='edit-profile'),
    path('dashboard/<int:pk>',DashboardView.as_view(),name='dashboard'),
    path('dashboard/<int:pk>/create_note',NoteCreateView,name='create_note'),
    path('dashboard/<int:pk1>/edit_note/<int:pk2>',NoteEditView.as_view(),name='edit-note'),
    path('profile_view/<int:pk>',ProfileDetailView.as_view(),name='view-profile'),
    path('search',SearchView.as_view(),name='search'),
    path('add_follower/<int:pk>',AddFollower,name='add-follower'), #to add followers pk is of the user who sent request
    path('remove_follower/<int:pk>',RemoveFollower,name='remove-follower'), #to remove follower pk is of follower being removed
    path('delete_request/<int:pk>',DeleteRequest,name='delete-request'), #to delete the sent request ,pk is of the followrequest object
    path('dashboard/<int:pk>/notifications',NotificationsView.as_view(),name='notifications'),
    path('create_request/<int:pk>',CreateRequest,name='create-request'),
    path('dashboard/<int:pk>/create_shared_note',SharedNoteCreateView,name='create-shared-note'),
    path('dashboard/<int:pk1>/edit_shared_note/<int:pk2>',SharedNoteEditView.as_view(),name='edit-shared-note'),
    #url( r'^run/(?P<pk>\d+)/$', views.PerfRunView.as_view( ))
    path('forgot_password',ForgotPasswordView,name='forgot_password'),
    path('password_changed',PasswordChangeSuccessView.as_view(),name='password-change-success'),
    path('wrong_ans',WrongAnswerView.as_view(),name='wrong_ans'),
    path('change_password',PasswordResetView.as_view(),name="password_reset"),
    path('dashboard/<int:pk1>/delete_shared_note/<int:pk2>',SharedNoteDeleteView.as_view(),name='delete-shared-note'),
    path('dashboard/<int:pk1>/delete_note/<int:pk2>',NoteDeleteView.as_view(),name='delete-note'),
    path('delete_user/<int:pk>',DeactivateAccountView.as_view(),name='delete-account'),
    path('get_note_pdf/<int:pk>',generate_pdf,name='get-pdf'),
    path('get_shared_note_pdf/<int:pk>',generate_shared_pdf,name='get-shared-pdf'),
]
