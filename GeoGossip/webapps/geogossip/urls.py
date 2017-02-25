from django.conf.urls import url
from geogossip import views

import django.contrib.auth.views

urlpatterns = [
    url(r'^create-group$', views.create_group, name='create-group'),
    url(r'^get-groups$', views.get_groups, name='get-groups'),
    url(r'^get-businesses$', views.get_businesses, name='get-businesses'),
    url(r'^create-group-with-latlon/(?P<lat>[-+]?\d*\.\d+|\d+)/(?P<lon>[-+]?\d*\.\d+|\d+)$',
        views.create_group_with_latlon, name='create-group-with-latlon'),
    url(r'^login$', django.contrib.auth.views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),
    url(r'^profile/edit-profile$', views.edit_profile, name='edit'),
    url(r'^avatar/(?P<user_id>\d+)$', views.get_avatar, name='avatar'),
    url(r'^group-chat/(?P<group_id>\d+)$', views.group_chat, name='group_chat'),
    url(r'^follow$', views.relationship, name='follow'),
    url(r'^follow/edit-follow/(?P<id>\d+)$', views.edit_relationship, name='edit_follow'),
    url(r'^search$', views.search, name='search')
]
