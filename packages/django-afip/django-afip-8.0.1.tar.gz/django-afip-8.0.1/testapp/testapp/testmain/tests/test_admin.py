from unittest import mock

from django.contrib import messages
from django.contrib.admin import site
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.utils.translation import gettext as _
from factory.django import FileField

from django_afip import exceptions
from django_afip import factories
from django_afip import models
from django_afip.admin import catch_errors
from django_afip.admin import ReceiptAdmin


class TestCatchErrors(TestCase):
    def _get_test_instance(self, exception_type):
        class TestClass(mock.MagicMock):
            @catch_errors
            def action(self, request):
                raise exception_type

        return TestClass()

    def test_certificate_expired(self):
        obj = self._get_test_instance(exceptions.CertificateExpired)

        request = HttpRequest()
        obj.action(request)

        self.assertEqual(obj.message_user.call_count, 1)
        self.assertEqual(
            obj.message_user.call_args,
            mock.call(
                request,
                _("The AFIP Taxpayer certificate has expired."),
                messages.ERROR,
            ),
        )

    def test_certificate_untrusted_cert(self):
        obj = self._get_test_instance(exceptions.UntrustedCertificate)

        request = HttpRequest()
        obj.action(request)

        self.assertEqual(obj.message_user.call_count, 1)
        self.assertEqual(
            obj.message_user.call_args,
            mock.call(
                request,
                _("The AFIP Taxpayer certificate is untrusted."),
                messages.ERROR,
            ),
        )

    def test_certificate_auth_error(self):
        obj = self._get_test_instance(exceptions.AuthenticationError)

        request = HttpRequest()
        obj.action(request)

        self.assertEqual(obj.message_user.call_count, 1)
        self.assertEqual(
            obj.message_user.call_args,
            mock.call(
                request,
                _("An unknown authentication error has ocurred: "),
                messages.ERROR,
            ),
        )


class TestTaxPayerAdminKeyGeneration(TestCase):
    def setUp(self):
        self.user = factories.SuperUserFactory()

    def test_without_key(self):
        taxpayer = factories.TaxPayerFactory(key=None)
        client = Client()
        client.force_login(self.user)

        response = client.post(
            "/admin/afip/taxpayer/",
            data={"_selected_action": [taxpayer.id], "action": "generate_key"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Key generated successfully.")

        taxpayer.refresh_from_db()
        self.assertIn(
            "-----BEGIN PRIVATE KEY-----",
            taxpayer.key.file.read().decode(),
        )

    def test_with_key(self):
        taxpayer = factories.TaxPayerFactory(key=FileField(data=b"Blah"))
        client = Client()
        client.force_login(self.user)

        response = client.post(
            "/admin/afip/taxpayer/",
            data={"_selected_action": [taxpayer.id], "action": "generate_key"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No keys generated; Taxpayers already had keys.",
        )

        taxpayer.refresh_from_db()
        self.assertEqual("Blah", taxpayer.key.file.read().decode())


class TestTaxPayerAdminRequestGeneration(TestCase):
    def setUp(self):
        self.user = factories.SuperUserFactory()

    def test_with_csr(self):
        taxpayer = factories.TaxPayerFactory(key=None)
        taxpayer.generate_key()
        client = Client()
        client.force_login(self.user)

        response = client.post(
            "/admin/afip/taxpayer/",
            data={"_selected_action": [taxpayer.id], "action": "generate_csr"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Content-Type: application/pkcs10",
            response.serialize_headers().splitlines(),
        )
        self.assertContains(
            response,
            "-----BEGIN CERTIFICATE REQUEST-----",
        )

    def test_without_key(self):
        taxpayer = factories.TaxPayerFactory(key=None)
        taxpayer.generate_key()
        client = Client()
        client.force_login(self.user)

        response = client.post(
            "/admin/afip/taxpayer/",
            data={"_selected_action": [taxpayer.id], "action": "generate_csr"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Content-Type: application/pkcs10",
            response.serialize_headers().splitlines(),
        )
        self.assertContains(
            response,
            "-----BEGIN CERTIFICATE REQUEST-----",
        )

    def test_multiple_taxpayers(self):
        taxpayer1 = factories.TaxPayerFactory(key__data=b"Blah")
        taxpayer2 = factories.TaxPayerFactory(key__data=b"Blah")
        client = Client()
        client.force_login(self.user)

        response = client.post(
            "/admin/afip/taxpayer/",
            data={
                "_selected_action": [taxpayer1.id, taxpayer2.id],
                "action": "generate_csr",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Can only generate CSR for one taxpayer at a time",
        )


class ReceiptFiltersAdminTestCase(TestCase):
    """Test ReceiptAdmin methods."""

    def setUp(self):
        factories.SuperUserFactory()

    def test_validation_filters(self):
        """
        Test the admin validation filters.

        This filters receipts by the validation status.
        """
        validated_receipt = factories.ReceiptFactory()
        failed_validation_receipt = factories.ReceiptFactory()
        not_validated_receipt = factories.ReceiptFactory()

        factories.ReceiptValidationFactory(receipt=validated_receipt)
        factories.ReceiptValidationFactory(
            result=models.ReceiptValidation.RESULT_REJECTED,
            receipt=failed_validation_receipt,
        )

        client = Client()
        client.force_login(User.objects.first())

        response = client.get("/admin/afip/receipt/?status=validated")
        self.assertContains(
            response,
            '<input class="action-select" name="_selected_action" value="{}" '
            'type="checkbox">'.format(validated_receipt.pk),
            html=True,
        )
        self.assertNotContains(
            response,
            '<input class="action-select" name="_selected_action" value="{}" '
            'type="checkbox">'.format(not_validated_receipt.pk),
            html=True,
        )
        self.assertNotContains(
            response,
            '<input class="action-select" name="_selected_action" value="{}" '
            'type="checkbox">'.format(failed_validation_receipt.pk),
            html=True,
        )

        response = client.get("/admin/afip/receipt/?status=not_validated")
        self.assertNotContains(
            response,
            '<input class="action-select" name="_selected_action" value="{}" '
            'type="checkbox">'.format(validated_receipt.pk),
            html=True,
        )
        self.assertContains(
            response,
            '<input class="action-select" name="_selected_action" value="{}" '
            'type="checkbox">'.format(not_validated_receipt.pk),
            html=True,
        )
        self.assertContains(
            response,
            '<input class="action-select" name="_selected_action" value="{}" '
            'type="checkbox">'.format(failed_validation_receipt.pk),
            html=True,
        )


class ReceiptAdminGetExcludeTestCase(TestCase):
    def test_django_111(self):
        admin = ReceiptAdmin(models.Receipt, site)
        request = RequestFactory().get("/admin/afip/receipt")
        request.user = factories.UserFactory()

        with mock.patch("django.VERSION", (1, 11, 7)):
            self.assertNotIn("related_receipts", admin.get_fields(request))

    def test_django_200(self):
        admin = ReceiptAdmin(models.Receipt, site)
        request = RequestFactory().get("/admin/afip/receipt")
        request.user = factories.UserFactory()

        with mock.patch("django.VERSION", (2, 0, 0)):
            self.assertIn("related_receipts", admin.get_fields(request))


class ReceiptHasFileFilterTestCase(TestCase):
    """Check that the has_file filter applies properly

    In order to confirm that it's working, we check that the link to the
    object's change page is present, since no matter how we reformat the rows,
    this will always be present as long as the object is listed.
    """

    def setUp(self):
        self.user = factories.SuperUserFactory()

        validation = factories.ReceiptValidationFactory()
        self.with_file = factories.ReceiptPDFFactory(
            receipt=validation.receipt,
        )
        self.without_file = factories.ReceiptPDFFactory()

        self.assertFalse(self.without_file.pdf_file)
        self.assertTrue(self.with_file.pdf_file)

        self.client = Client()
        self.client.force_login(User.objects.first())

    def test_filter_all(self):
        response = self.client.get("/admin/afip/receiptpdf/")
        self.assertContains(
            response, f"/admin/afip/receiptpdf/{self.with_file.pk}/change/"
        )
        self.assertContains(
            response, f"/admin/afip/receiptpdf/{self.without_file.pk}/change/"
        )

    def test_filter_with_file(self):
        response = self.client.get("/admin/afip/receiptpdf/?has_file=yes")
        self.assertContains(
            response, f"/admin/afip/receiptpdf/{self.with_file.pk}/change/"
        )
        self.assertNotContains(
            response, f"/admin/afip/receiptpdf/{self.without_file.pk}/change/"
        )

    def test_filter_without_file(self):
        response = self.client.get("/admin/afip/receiptpdf/?has_file=no")
        self.assertNotContains(
            response, f"/admin/afip/receiptpdf/{self.with_file.pk}/change/"
        )
        self.assertContains(
            response, f"/admin/afip/receiptpdf/{self.without_file.pk}/change/"
        )
