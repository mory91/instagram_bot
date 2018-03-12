from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login', views.login_user, name='login'),
    path('createbot', views.create_bot, name='create_bot'),
    path('<int:bot_id>/deletetarget/<int:id>', views.delete_target, name='delete_target'),
    path('<int:bot_id>/dashboard', views.dashboard, name='dashboard'),
    path('<int:bot_id>/addtarget', views.add_target, name='add_target'),
    path('<int:bot_id>/addpagegroup', views.add_page_group, name='add_page_group'),
    path('<int:bot_id>/changefollowsstate', views.change_follows_state, name='change_follows_state'),
    path('<int:bot_id>/setconfig', views.set_config, name='set_config'),

]