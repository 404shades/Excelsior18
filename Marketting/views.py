from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from django.views.generic import UpdateView, View
from .utils import MailChimp
from .mixins import CsrfExemptMixin
from django.conf import settings
from .forms import MarketingPreferenceForm
from .models import MarketingPreference


class MarketingPreferenceUpdateView(UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'Base/forms.html'
    success_url = '/settings/email/'

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView,self).get_context_data(**kwargs)
        context['title'] = "Update Email Preference"
        return context

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/accounts/login?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


class MailChimpWebHookView(CsrfExemptMixin,View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id}')
        if str(list_id) == str(settings.MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = MailChimp().check_sub_status(email)
            subs_status = response['status']
            is_subbed = None
            mailchip_suubed = None
            if subs_status == 'subscribed':
                mailchip_suubed, is_subbed = (True, True)
            elif subs_status == 'unsubscribed':
                mailchip_suubed, is_subbed = (False, False)
            if is_subbed is not None and mailchip_suubed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchip_suubed, mailchimp_msg=str(data))
            return HttpResponse("Thank You", status=200)


