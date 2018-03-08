from django.views.generic import TemplateView


class BaseView(TemplateView):
    template_name = 'launcher.html'


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class ContactUsView(TemplateView):
    template_name = 'contact.html'
