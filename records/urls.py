from django.conf.urls import patterns, url

from records import views
from django.views.generic import TemplateView
import django.contrib.auth.views

urlpatterns = patterns('',
                       # /
                       url(r'^$',
                           views.ListLatest.as_view(),
                           name='index'),

                       # /submit/
                       url(r'^submit/$',
                           views.SubmitView.as_view(),
                           name='submit'),

                       url(r'^submit/(?P<game>[^/]+)/(?P<category>[^/]+)/$',
                           views.SubmitView.as_view(),
                           name='submit'),

                       # /pending/
                       url(r'^pending/$',
                           views.PendingView.as_view(),
                           name='pending'),

                       # /login/
                       url(r'^login/$',
                           django.contrib.auth.views.login,
                           name='login'),

                       # /logout/
                       url(r'^logout/$',
                           django.contrib.auth.views.logout,
                           name='logout'),

                       # ex: /latest/2/
                       url(r'^latest/(?P<page>[1-9]\d*)/$',
                           views.ListLatest.as_view(),
                           name='page'),

                       # ex: /game/Rockman 2/
                       url(r'^game/(?P<game_name>[^/]+)/$',
                           views.record,
                           name='record'),

                       # ex: /game/Rockman 2/Any%/
                       url(r'^game/(?P<game_name>[^/]+)/(?P<category>[^/]+)/$', 
                           views.record,
                           name='record'),

                       # /ajax/autocomplete/game/
                       url(r'^ajax/autocomplete/game/$',
                           views.ajax_game_autocomplete,
                           name='game_autocomplete'),

                       # /ajax/autocomplete/category
                       url(r'^ajax/autocomplete/category/$',
                           views.ajax_category_autocomplete,
                           name='category_autocomplete'),

                       # ex: /browse/c/2
                       url(r'^browse/(?P<letter>[a-zA-Z]|num)/(?P<page>[1-9]\d*)/*$',
                           views.BrowseView.as_view(),
                           name='browse'),

                       # ex: /browse/2/
                       url(r'^browse/(?P<letter>[a-zA-Z]|num)/$',
                           views.BrowseView.as_view(),
                           name='browse'),

                       # /browse/
                       url(r'^browse/$',
                           views.BrowseView.as_view(),
                           name='browse'),

                       # /submit/success
                       url(r'^submit/success/$',
                           TemplateView.as_view(template_name='success.html'),
                           name='success')
                       )
