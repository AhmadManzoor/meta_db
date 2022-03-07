import requests
from django.conf import settings


class MailchimpSugars(object):
    @staticmethod
    def update_mailchimp_subscriber(email, status):
        data = {
            "email": email,
            "status": status,
        }
        print("[update_mailchimp_subscriber] data (%s)" % str(data))

        url = "%s/subscriber-tasks/update-subscriber/" % settings.OS_TASK_URL
        try:
            requests.post(url, data=data)
        except requests.exceptions.RequestException as e:
            print("[update_mailchimp_subscriber] data (%s), Exception - %s (%s)" % (str(data), str(e), str(type(e))))
            pass
        except Exception as e:
            print("[update_mailchimp_subscriber] data (%s), Exception - %s (%s)" % (str(data), str(e), str(type(e))))
            pass
