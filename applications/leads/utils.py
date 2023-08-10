# Email sender
from django.conf import settings

from applications.utils.email.classes import TemplateEmail

from .constants import NEW_LEAD_CREATED_SUBJECT, NEW_LEAD_CREATED_AND_ASSIGNED_SUBJECT


def build_lead_email(lead_data):
    if lead_data.agent:
        to = lead_data.agent.email
        subject = NEW_LEAD_CREATED_AND_ASSIGNED_SUBJECT
        template_content = {"main_content": NEW_LEAD_CREATED_AND_ASSIGNED_SUBJECT}
    else:
        to = "alextester1999@gmail.com"
        subject = NEW_LEAD_CREATED_SUBJECT
        template_content = {"main_content": NEW_LEAD_CREATED_SUBJECT}

    created_lead_id = lead_data.id
    created_lead_urls = {
        "lead_url": f"{'http'if settings.DEBUG else 'https'}://{settings.DOMAIN}/users/leads/{created_lead_id}"
    }
    context = {
        "data": lead_data,
        "links": created_lead_urls,
        "main_content": template_content,
    }
    template = "new_lead_created"

    send_email(to=to, subject=subject, template=template, context=context)


def send_email(to, subject, template, context):
    template = TemplateEmail(to=to, subject=subject, template=template, context=context)
    template.send()
