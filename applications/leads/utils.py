# Email sender
from django.conf import settings

from applications.utils.email.classes import TemplateEmail

from .constants import NEW_LEAD_CREATED_SUBJECT


def send_email_lead_created(validated_data):
    to = validated_data["email"]
    subject = NEW_LEAD_CREATED_SUBJECT

    created_lead_id = validated_data["id"]
    created_lead_urls = {"lead_url": f"{settings.DOMAIN}/leads/{created_lead_id}"}

    context = {"data": validated_data, "links": created_lead_urls}
    template = "new_lead_created"

    template = TemplateEmail(to=to, subject=subject, template=template, context=context)
    template.send()