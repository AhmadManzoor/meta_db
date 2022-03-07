from project_d.utility.email_handlers import EmailUtil  # FIXME: remove dependency of project_d
from django.template.loader import render_to_string


class EmailSender(object):
    # send email directly via Mandrill
    @classmethod
    def send_html(cls, template_name, context, from_email, from_name, to_email, to_name, subject):
        email_body = render_to_string(template_name, {"context_data": context})
        result = EmailUtil.send_email(
            from_email=from_email,
            from_name=from_name,
            to_email=to_email,
            to_name=to_name,
            subject=subject,
            body=email_body,
            body_type='html'
        )
        return result
