from django.conf import settings
import requests
import re
import hashlib
import json


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError('String passed is not a valid email address')
    return email


def get_subscriber_hash(member_email):
    check_email(email=member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()


class MailChimp(object):
    def __init__(self):
        super(MailChimp, self).__init__()
        self.key = settings.MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=settings.MAILCHIMP_DATA_CENTER)
        self.list_id = settings.MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(
            api_url=self.api_url,
            list_id=self.list_id
        )

    def change_subs_status(self, email, status):
        hashed_email = get_subscriber_hash(email)
        print(hashed_email)
        endpoint = self.list_endpoint + "/members/" + hashed_email
        data = {
            'status': self.check_valid_status(status)
        }
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        print(r.url)
        return r.status_code, r.json()

    def check_sub_status(self, email):
        hashed_email = get_subscriber_hash(email)
        print(hashed_email)
        endpoint = self.list_endpoint + "/members/" + hashed_email
        r = requests.get(endpoint, auth=("", self.key))
        print(r.url)
        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
        if status not in choices:
            raise ValueError('Not A Valid Choice')
        return status

    def add_email(self, email):
        status = "subscribed"
        self.check_valid_status(status)
        data = {
            'email_address': email,
            'status': status
        }
        endpoint = self.list_endpoint + "/members"
        r = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def unsubscribe(self, email):
        return self.change_subs_status(email, status='unsubscribed')

    def subscribe(self, email):
        return self.change_subs_status(email, status='subscribed')

    def pending(self, email):
        return self.change_subs_status(email, status='pending')
