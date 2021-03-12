from django.urls import path
from . import views
from users import views as users_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required(views.Home.as_view()),name="home"),
    path('send-invite',views.send_invitation,name='sendinvite'),
    path('remove-friend',views.remove_from_friends,name='removeinvite'),
    path('send-invites/accept/',users_views.accept_invitation,name='acceptinvite'),
    path('send-invites/reject/',users_views.reject_invitation,name='rejectinvite'),

]
