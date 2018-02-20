"""Excelsior18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Participation.views import participate_detail_api_view
from Marketting.views import MarketingPreferenceUpdateView, MailChimpWebHookView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('Accounts.urls')),
    path('Events/', include('Events.urls')),
    path('participation/', include('Participation.urls')),
    path('api/participate', participate_detail_api_view, name='api-detail'),
    path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='MarketOpt'),
    path('webhooks/mailchimp/', MailChimpWebHookView.as_view(), name='webhooks_mailchimp'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
