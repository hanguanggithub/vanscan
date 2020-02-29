"""webscan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cms import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('whatweb', views.Whatweb.as_view()),
    path('whatcms', views.Whatcms.as_view()),
    path('portscan', views.Portscan.as_view()),
    path('domain', views.Otherdomain.as_view()),
    path('fuckcms', views.Fuckcms.as_view()),
    path('api/cms', views.api_cms),

    path('awvs12', views.Awvs.as_view()),
    path('api/awvs12/delscan', views.awvs12.del_scan),
    path('api/awvs12/stopscan', views.awvs12.stop_scan),
    path('api/awvs12/addscan', views.awvs12.add_scan),
    path('api/awvs12/Presentation', views.awvs12.Presentation),
    path('api/awvs12/getvulns', views.awvs12.get_vluns),

    path('awvs13', views.Awvs13.as_view()),
    path('api/awvs13/delscan', views.awvs13.del_scan),
    path('api/awvs13/stopscan', views.awvs13.stop_scan),
    path('api/awvs13/addscan', views.awvs13.add_scan),
    path('api/awvs13/Presentation', views.awvs13.Presentation),
    path('api/awvs13/moreadd', views.awvs13.moreadd),
    path('api/awvs13/getvulns', views.awvs13.get_vluns),
]
