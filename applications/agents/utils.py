from django.conf import settings

from applications.utils.email.classes import TemplateEmail

from .constants import NEW_AGENT_CREATED_SUBJECT


def build_agent_email(agent_data):
    to = agent_data.user.email
    subject = NEW_AGENT_CREATED_SUBJECT
    template_content = {"main_content": NEW_AGENT_CREATED_SUBJECT}

    created_agent_id = agent_data.id

    created_agent_urls = {
        "lead_url": f"{'http' if settings.DEBUG else 'https'}://{settings.DOMAIN}/users/agents/{created_agent_id}"
    }
    context = {
        "data": agent_data.user,
        "links": created_agent_urls,
        "main_content": template_content,
    }
    template = "new_lead_created"

    send_email(to=to, subject=subject, template=template, context=context)


def send_email(to, subject, template, context):
    template = TemplateEmail(to=to, subject=subject, template=template, context=context)
    template.send()
