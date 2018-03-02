from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', views.login_user, name='login'),
    path('deletetarget/<int:id>', views.delete_target, name='delete_target'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('addtarget', views.add_target, name='add_target'),
    path('addpagegroup', views.add_page_group, name='add_page_group'),
    path('changefollowsstate', views.change_follows_state, name='change_follows_state'),

]