import pytest
from django.template import TemplateDoesNotExist

from w.services.technical.pdf_service import PdfService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestPdfService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.filename = "test_pdf_service.pdf"

    def test_create_pdf_with_empty_content_return_none(self):
        """
        Ensure pdf service return None with empty content param
        """
        self.clean_sandbox()
        params = {
            "filename": self.get_sandbox_dir(filename=self.filename),
            "content": {},
        }
        pdf = PdfService.write_file(**params)
        assert pdf is None
        self.assert_file_not_exists(params["filename"])

    def test_create_pdf_with_unknown_template_raise_exception(self):
        """
        Ensure pdf service raise exception with unknown template path
        """
        self.clean_sandbox()
        params = {
            "filename": self.get_sandbox_dir(filename=self.filename),
            "content": {"template_name": "unknown_template.html", "context": ""},
        }
        match = "unknown_template.html"
        with pytest.raises(TemplateDoesNotExist, match=match):
            PdfService.write_file(**params)
        self.assert_file_not_exists(params["filename"])

    def test_create_pdf_with_full_template_file_return_bytes(self):
        """
        Ensure pdf service return a pdf with html template
        """
        self.clean_sandbox()
        pdf_context = {"name": "test_name"}
        params = {
            "filename": self.get_sandbox_dir(filename=self.filename),
            "content": {
                "template_name": "pdf/test_pdf_service.html",
                "context": pdf_context,
            },
        }
        pdf = PdfService.write_file(**params)
        assert pdf is not None and isinstance(pdf, bytes)
        self.assert_file_exists(params["filename"])

    def test_create_pdf_with_empty_context_return_bytes(self):
        """
        Ensure pdf service return a pdf with html template and empty context
        """
        self.clean_sandbox()
        params = {
            "filename": self.get_sandbox_dir(filename=self.filename),
            "content": {"template_name": "pdf/test_pdf_service.html", "context": {}},
        }
        pdf = PdfService.write_file(**params)
        assert pdf is not None and isinstance(pdf, bytes)
        self.assert_file_exists(params["filename"])

    def test_create_pdf_with_html_string_return_bytes(self):
        """
        Ensure pdf service return a pdf with html string
        """
        self.clean_sandbox()
        params = {
            "filename": self.get_sandbox_dir(filename=self.filename),
            "content": "<h1>test</h1>",
        }
        pdf = PdfService.write_file(**params)
        assert pdf is not None and isinstance(pdf, bytes)
        self.assert_file_exists(params["filename"])
