from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext

from notification import backends

from twilio.rest import TwilioRestClient


TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
TWILIO_FROM_NUMBER = getattr(settings, 'TWILIO_FROM_NUMBER', None)
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class SMSBackend(backends.BaseBackend):
    spam_sensitivity = 2

    def can_send(self, user, notice_type):
        can_send = super(SMSBackend, self).can_send(user, notice_type)
        if can_send and user.profile.phone:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            "sms.txt",
        ), notice_type.label, context)

        message = render_to_string("notification/sms_body.txt", {
            "message": messages["sms.txt"],
        }, context)

        sms = client.messages.create(
            to=recipient.profile.phone,
            from_=TWILIO_FROM_NUMBER,
            body=message
        )

        return True
