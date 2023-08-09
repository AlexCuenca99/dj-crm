from django.test import TestCase
from ..models import Lead


class LeadTest(TestCase):
    """Test module for Lead model"""

    def setUp(self) -> None:
        Lead.objects.create(
            address="Example street",
            phone="123456789",
            last_name="Scott",
            first_name="Henry",
            email="henry@crm.com",
            birth="1999-12-02",
            gender="M",
            agent=None,
        )

    def test_lead_name(self):
        """Test for get the full name of a created lead"""

        lead_henry = Lead.objects.get(email="henry@crm.com")
        self.assertEqual(lead_henry.get_full_name(), "Henry Scott")
